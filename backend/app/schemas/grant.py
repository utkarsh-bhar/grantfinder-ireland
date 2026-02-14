"""Grant request/response schemas."""

from __future__ import annotations
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel


class GrantBase(BaseModel):
    name: str
    slug: str
    short_description: str
    long_description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    max_amount: Optional[float] = None
    amount_description: Optional[str] = None
    amount_type: str
    is_means_tested: bool = False
    source_organisation: str
    source_url: str
    application_url: Optional[str] = None
    application_method: Optional[str] = None
    is_always_open: bool = True
    opening_date: Optional[date] = None
    closing_date: Optional[date] = None
    typical_processing: Optional[str] = None


class GrantCreate(GrantBase):
    pass


class GrantUpdate(BaseModel):
    name: Optional[str] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    category: Optional[str] = None
    max_amount: Optional[float] = None
    amount_description: Optional[str] = None
    is_means_tested: Optional[bool] = None
    source_url: Optional[str] = None
    application_url: Optional[str] = None
    is_always_open: Optional[bool] = None
    closing_date: Optional[date] = None
    is_active: Optional[bool] = None


class GrantResponse(GrantBase):
    id: str
    is_active: bool
    last_verified_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class GrantListResponse(BaseModel):
    grants: list[GrantResponse]
    total: int
    page: int
    per_page: int


class GrantDocumentResponse(BaseModel):
    id: str
    document_name: str
    description: Optional[str] = None
    is_required: bool = True
    sort_order: int = 0

    model_config = {"from_attributes": True}


class GrantStepResponse(BaseModel):
    id: str
    step_number: int
    title: str
    description: str
    url: Optional[str] = None

    model_config = {"from_attributes": True}


class CategoryCount(BaseModel):
    category: str
    label: str
    count: int


class EligibilityRuleCreate(BaseModel):
    rule_group: int = 0
    field: str
    operator: str
    value: str
    description: Optional[str] = None
    is_mandatory: bool = True
    sort_order: int = 0


class EligibilityRuleResponse(EligibilityRuleCreate):
    id: str
    grant_id: str

    model_config = {"from_attributes": True}
