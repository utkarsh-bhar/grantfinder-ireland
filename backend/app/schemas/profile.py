"""Profile (questionnaire) request/response schemas."""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class ProfileRequest(BaseModel):
    """Full questionnaire submission. All fields optional for partial saves."""

    # Step 1: About You
    age: Optional[int] = Field(None, ge=16, le=120)
    county: Optional[str] = None
    marital_status: Optional[str] = None
    nationality: Optional[str] = None
    residency_status: Optional[str] = None

    # Step 2: Your Home
    home_status: Optional[str] = None
    home_type: Optional[str] = None
    home_year_built: Optional[int] = Field(None, ge=1700, le=2030)
    ber_rating: Optional[str] = None
    has_solar_pv: Optional[bool] = None
    has_heat_pump: Optional[bool] = None
    property_value: Optional[float] = None
    mortgage_status: Optional[str] = None
    is_first_time_buyer: Optional[bool] = None

    # Step 3: Family
    has_children: Optional[bool] = None
    num_children: Optional[int] = Field(None, ge=0, le=20)
    youngest_child_age: Optional[int] = Field(None, ge=0)
    oldest_child_age: Optional[int] = Field(None, ge=0)
    is_lone_parent: Optional[bool] = None
    is_carer: Optional[bool] = None
    caring_for_relationship: Optional[str] = None

    # Step 4: Work & Income
    employment_status: Optional[str] = None
    is_freelancer: Optional[bool] = None
    has_side_income: Optional[bool] = None
    annual_income: Optional[float] = None
    income_bracket: Optional[str] = None

    # Step 5: Welfare & Health
    welfare_payments: Optional[list[str]] = None
    has_medical_card: Optional[bool] = None
    has_gp_visit_card: Optional[bool] = None
    has_disability: Optional[bool] = None
    disability_type: Optional[str] = None
    household_disability: Optional[bool] = None

    # Step 6: Education & Business
    is_student: Optional[bool] = None
    education_level: Optional[str] = None
    planning_education: Optional[bool] = None
    owns_business: Optional[bool] = None
    business_type: Optional[str] = None
    business_age_months: Optional[int] = None
    num_employees: Optional[int] = Field(None, ge=0)
    business_sector: Optional[str] = None
    planning_business: Optional[bool] = None

    # Step 7: Transport & Other
    owns_vehicle: Optional[bool] = None
    vehicle_type: Optional[str] = None
    planning_ev_purchase: Optional[bool] = None
    is_farmer: Optional[bool] = None
    farm_size_hectares: Optional[float] = None
    farm_type: Optional[str] = None
    is_landlord: Optional[bool] = None
    num_rental_properties: Optional[int] = Field(None, ge=0)


class ProfileResponse(ProfileRequest):
    """Same as request but with id and timestamps."""
    id: str
    user_id: str
    is_over_66: bool = False
    is_over_70: bool = False
    has_child_under_7: bool = False

    model_config = {"from_attributes": True}
