"""Profile endpoints: create/update/get user questionnaire answers."""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.profile import UserProfile
from app.models.scan_result import ScanResult
from app.models.alert import GrantAlert
from app.schemas.profile import ProfileRequest, ProfileResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/profile", tags=["Profile"])


def _get_or_create_profile(user: User, db: Session) -> UserProfile:
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user.id)
        .order_by(UserProfile.updated_at.desc())
        .first()
    )
    if not profile:
        profile = UserProfile(user_id=user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


@router.post("", response_model=ProfileResponse, status_code=200)
def create_or_update_profile(
    body: ProfileRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create or fully update user profile (questionnaire answers)."""
    profile = _get_or_create_profile(user, db)

    update_data = body.model_dump(exclude_unset=True)
    for field_name, value in update_data.items():
        if hasattr(profile, field_name):
            setattr(profile, field_name, value)

    # Compute convenience flags
    if profile.age is not None:
        profile.is_over_66 = profile.age >= 66
        profile.is_over_70 = profile.age >= 70
    if profile.youngest_child_age is not None:
        profile.has_child_under_7 = profile.youngest_child_age < 7

    db.commit()
    db.refresh(profile)

    return _profile_to_response(profile)


@router.get("", response_model=ProfileResponse)
def get_profile(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get the current user's latest profile."""
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user.id)
        .order_by(UserProfile.updated_at.desc())
        .first()
    )
    if not profile:
        raise HTTPException(404, "No profile found. Please complete the questionnaire.")
    return _profile_to_response(profile)


@router.patch("", response_model=ProfileResponse)
def update_profile_partial(
    body: ProfileRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Partially update specific profile fields."""
    profile = _get_or_create_profile(user, db)

    update_data = body.model_dump(exclude_unset=True)
    for field_name, value in update_data.items():
        if hasattr(profile, field_name):
            setattr(profile, field_name, value)

    # Recompute flags
    if profile.age is not None:
        profile.is_over_66 = profile.age >= 66
        profile.is_over_70 = profile.age >= 70
    if profile.youngest_child_age is not None:
        profile.has_child_under_7 = profile.youngest_child_age < 7

    db.commit()
    db.refresh(profile)
    return _profile_to_response(profile)


def _profile_to_response(profile: UserProfile) -> ProfileResponse:
    return ProfileResponse(
        id=str(profile.id),
        user_id=str(profile.user_id),
        age=profile.age,
        county=profile.county,
        marital_status=profile.marital_status,
        nationality=profile.nationality,
        residency_status=profile.residency_status,
        home_status=profile.home_status,
        home_type=profile.home_type,
        home_year_built=profile.home_year_built,
        ber_rating=profile.ber_rating,
        has_solar_pv=profile.has_solar_pv,
        has_heat_pump=profile.has_heat_pump,
        property_value=float(profile.property_value) if profile.property_value else None,
        mortgage_status=profile.mortgage_status,
        is_first_time_buyer=profile.is_first_time_buyer,
        has_children=profile.has_children,
        num_children=profile.num_children,
        youngest_child_age=profile.youngest_child_age,
        oldest_child_age=profile.oldest_child_age,
        is_lone_parent=profile.is_lone_parent,
        is_carer=profile.is_carer,
        caring_for_relationship=profile.caring_for_relationship,
        employment_status=profile.employment_status,
        is_freelancer=profile.is_freelancer,
        has_side_income=profile.has_side_income,
        annual_income=float(profile.annual_income) if profile.annual_income else None,
        income_bracket=profile.income_bracket,
        welfare_payments=profile.welfare_payments,
        has_medical_card=profile.has_medical_card,
        has_gp_visit_card=profile.has_gp_visit_card,
        has_disability=profile.has_disability,
        disability_type=profile.disability_type,
        household_disability=profile.household_disability,
        is_student=profile.is_student,
        education_level=profile.education_level,
        planning_education=profile.planning_education,
        owns_business=profile.owns_business,
        business_type=profile.business_type,
        business_age_months=profile.business_age_months,
        num_employees=profile.num_employees,
        business_sector=profile.business_sector,
        planning_business=profile.planning_business,
        owns_vehicle=profile.owns_vehicle,
        vehicle_type=profile.vehicle_type,
        planning_ev_purchase=profile.planning_ev_purchase,
        is_farmer=profile.is_farmer,
        farm_size_hectares=float(profile.farm_size_hectares) if profile.farm_size_hectares else None,
        farm_type=profile.farm_type,
        is_landlord=profile.is_landlord,
        num_rental_properties=profile.num_rental_properties,
        is_over_66=profile.is_over_66,
        is_over_70=profile.is_over_70,
        has_child_under_7=profile.has_child_under_7,
    )


@router.delete("/account", status_code=204)
def delete_account(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete the user's account and all associated data (GDPR Article 17 - Right to Erasure)."""
    db.delete(user)
    db.commit()
    return None


@router.get("/export")
def export_user_data(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Export all user data as JSON (GDPR Article 20 - Right to Data Portability)."""
    profiles = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user.id)
        .order_by(UserProfile.updated_at.desc())
        .all()
    )
    scan_results = db.query(ScanResult).filter(ScanResult.user_id == user.id).all()
    alerts = db.query(GrantAlert).filter(GrantAlert.user_id == user.id).all()

    profile_data = []
    for p in profiles:
        profile_data.append(_profile_to_response(p).model_dump())

    scan_data = []
    for sr in scan_results:
        matched = [
            {
                "grant_id": str(mg.grant_id),
                "match_score": float(mg.match_score) if mg.match_score else None,
                "match_type": mg.match_type,
                "notes": mg.notes,
            }
            for mg in sr.matched_grants
        ]
        scan_data.append({
            "id": str(sr.id),
            "total_grants": sr.total_grants,
            "total_value": float(sr.total_value) if sr.total_value else None,
            "summary": sr.summary,
            "created_at": sr.created_at.isoformat() if sr.created_at else None,
            "matched_grants": matched,
        })

    alert_data = [
        {
            "id": str(a.id),
            "grant_id": str(a.grant_id) if a.grant_id else None,
            "alert_type": a.alert_type,
            "channel": a.channel,
            "is_active": a.is_active,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in alerts
    ]

    return {
        "exported_at": datetime.utcnow().isoformat(),
        "user": {
            "id": str(user.id),
            "email": user.email,
            "plan": user.plan,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        },
        "profiles": profile_data,
        "scan_results": scan_data,
        "alerts": alert_data,
    }
