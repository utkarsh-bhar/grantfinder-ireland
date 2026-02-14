"""Scan request/response schemas."""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class AnonymousScanRequest(BaseModel):
    """Minimal fields for running a scan without an account."""
    age: Optional[int] = None
    county: Optional[str] = None
    home_status: Optional[str] = None
    home_type: Optional[str] = None
    home_year_built: Optional[int] = None
    ber_rating: Optional[str] = None
    has_solar_pv: Optional[bool] = None
    has_heat_pump: Optional[bool] = None
    is_first_time_buyer: Optional[bool] = None
    has_mortgage: Optional[bool] = None
    pays_rent: Optional[bool] = None
    has_children: Optional[bool] = None
    num_children: Optional[int] = None
    youngest_child_age: Optional[int] = None
    is_lone_parent: Optional[bool] = None
    is_carer: Optional[bool] = None
    has_dependent_relatives: Optional[bool] = None
    num_dependent_relatives: Optional[int] = None
    has_incapacitated_child: Optional[bool] = None
    employment_status: Optional[str] = None
    income_bracket: Optional[str] = None
    is_freelancer: Optional[bool] = None
    works_from_home: Optional[bool] = None
    welfare_payments: Optional[list[str]] = None
    has_medical_card: Optional[bool] = None
    has_disability: Optional[bool] = None
    household_disability: Optional[bool] = None
    has_medical_expenses: Optional[bool] = None
    is_visually_impaired: Optional[bool] = None
    has_nursing_home_expenses: Optional[bool] = None
    is_expecting_or_new_parent: Optional[bool] = None
    has_home_carer_spouse: Optional[bool] = None
    is_student: Optional[bool] = None
    planning_education: Optional[bool] = None
    owns_business: Optional[bool] = None
    planning_business: Optional[bool] = None
    num_employees: Optional[int] = None
    owns_vehicle: Optional[bool] = None
    vehicle_type: Optional[str] = None
    planning_ev_purchase: Optional[bool] = None
    is_farmer: Optional[bool] = None
    is_landlord: Optional[bool] = None
    marital_status: Optional[str] = None


class GrantMatchResponse(BaseModel):
    grant_id: str
    name: str
    slug: str
    short_description: str
    match_type: str  # eligible, likely, possible
    match_score: float
    max_amount: Optional[float] = None
    amount_description: Optional[str] = None
    source_organisation: str = ""
    source_url: str = ""
    application_url: Optional[str] = None
    notes: str = ""
    is_locked: bool = False
    category: str = ""
    # Savings estimates
    estimated_annual_saving: Optional[float] = None
    estimated_backdated_saving: Optional[float] = None
    savings_note: str = ""
    how_to_claim: str = ""


class CategoryResult(BaseModel):
    category: str
    label: str
    count: int
    total_value: float
    grants: list[GrantMatchResponse]


class ScanResponse(BaseModel):
    scan_id: Optional[str] = None
    total_grants_found: int
    total_potential_value: float
    categories: list[CategoryResult]
    summary: str = ""
    generated_at: str


class ScanHistoryItem(BaseModel):
    id: str
    total_grants: int
    total_value: Optional[float]
    created_at: str

    model_config = {"from_attributes": True}
