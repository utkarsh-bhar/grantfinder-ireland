"""
Precise savings calculator for Irish tax credits and grants.

Calculates actual estimated annual savings and backdated claim amounts
based on the user's income bracket and tax rate.
"""

from __future__ import annotations
from typing import Any, Optional


# Irish tax bands 2025/2026
# Single: 20% on first €42,000, 40% on the rest
# Married (one earner): 20% on first €51,000, 40% on the rest
INCOME_TAX_RATES = {
    "<20k": {"marginal_rate": 0.20, "effective_rate": 0.20},
    "20-40k": {"marginal_rate": 0.20, "effective_rate": 0.20},
    "40-60k": {"marginal_rate": 0.40, "effective_rate": 0.30},
    "60-80k": {"marginal_rate": 0.40, "effective_rate": 0.35},
    "80k+": {"marginal_rate": 0.40, "effective_rate": 0.38},
}

# Grants that can be backdated (up to 4 years)
BACKDATABLE_SLUGS = {
    "dependent-relative-tax-credit": 4,
    "age-tax-credit": 4,
    "blind-persons-tax-credit": 4,
    "widowed-person-tax-credit": 4,
    "widowed-parent-tax-credit": 4,  # 5 years but decreasing
    "incapacitated-child-tax-credit": 4,
    "paye-tax-credit": 4,
    "earned-income-tax-credit": 4,
    "rent-tax-credit": 4,  # available 2022-2028
    "home-carer-tax-credit": 4,
    "single-person-child-carer-credit": 4,
    "medical-expenses-tax-relief": 4,
    "nursing-home-expenses-tax-relief": 4,
    "remote-working-tax-relief": 4,
    "mortgage-interest-tax-credit": 3,  # 2023-2026 only
}

# Tax credits where saving = credit amount (direct reduction)
# vs. tax reliefs where saving depends on tax rate
RELIEF_AT_RATE_SLUGS = {
    "medical-expenses-tax-relief": 0.20,  # Always at standard rate
    "nursing-home-expenses-tax-relief": "marginal",  # At marginal rate
    "remote-working-tax-relief": 0.30,  # 30% of costs
    "tuition-fees-tax-relief": 0.20,  # At standard rate
}


def calculate_savings(
    slug: str,
    max_amount: Optional[float],
    amount_description: str,
    income_bracket: Optional[str],
    profile: dict[str, Any],
) -> dict:
    """
    Calculate estimated annual and backdated savings for a grant.

    Returns dict with:
    - estimated_annual_saving: float or None
    - estimated_backdated_saving: float or None
    - savings_note: str explaining the calculation
    """
    rates = INCOME_TAX_RATES.get(income_bracket or "40-60k", INCOME_TAX_RATES["40-60k"])
    annual_saving: Optional[float] = None
    backdated_saving: Optional[float] = None
    savings_note = ""

    # For dependent relative credit, multiply by number of relatives
    if slug == "dependent-relative-tax-credit":
        num_relatives = profile.get("num_dependent_relatives", 1) or 1
        annual_saving = 305.0 * num_relatives
        savings_note = f"€305 x {num_relatives} dependent relative{'s' if num_relatives > 1 else ''} = €{annual_saving:,.0f}/year"

    # For personal tax credit — married couples get double
    elif slug == "personal-tax-credit":
        marital = profile.get("marital_status", "single")
        if marital == "married":
            annual_saving = 4000.0
            savings_note = "€4,000/year (married couple)"
        else:
            annual_saving = 2000.0
            savings_note = "€2,000/year"

    # Age tax credit — married couples get double
    elif slug == "age-tax-credit":
        marital = profile.get("marital_status", "single")
        if marital == "married":
            annual_saving = 490.0
            savings_note = "€490/year (married couple)"
        else:
            annual_saving = 245.0
            savings_note = "€245/year"

    # Blind person's credit
    elif slug == "blind-persons-tax-credit":
        annual_saving = 1950.0
        savings_note = "€1,950/year direct tax reduction"

    # Rent tax credit — couples get double
    elif slug == "rent-tax-credit":
        marital = profile.get("marital_status", "single")
        if marital == "married":
            annual_saving = 2000.0
            savings_note = "€2,000/year (jointly assessed couple)"
        else:
            annual_saving = 1000.0
            savings_note = "€1,000/year (20% of rent up to this max)"

    # Child benefit — per child
    elif slug == "child-benefit":
        num = profile.get("num_children", 1) or 1
        annual_saving = 1680.0 * num
        savings_note = f"€140/month x {num} child{'ren' if num > 1 else ''} = €{annual_saving:,.0f}/year"

    # Incapacitated child — per child
    elif slug == "incapacitated-child-tax-credit":
        annual_saving = 3800.0
        savings_note = "€3,800/year per qualifying child"

    # Reliefs where the amount depends on spending
    elif slug in RELIEF_AT_RATE_SLUGS:
        rate = RELIEF_AT_RATE_SLUGS[slug]
        if rate == "marginal":
            rate_val = rates["marginal_rate"]
            savings_note = f"Tax relief at your marginal rate ({rate_val:.0%}) on qualifying expenses"
        else:
            savings_note = f"Tax relief at {rate:.0%} on qualifying expenses"
        # Can't calculate exact amount without expense figures
        annual_saving = None

    # Fixed-amount tax credits — saving = credit amount
    elif max_amount and max_amount < 10000:
        # Likely a tax credit — direct reduction
        annual_saving = max_amount
        savings_note = f"€{max_amount:,.0f}/year direct tax reduction"

    # For grants (not tax credits) — the grant amount itself
    elif max_amount:
        annual_saving = max_amount
        savings_note = amount_description or f"Up to €{max_amount:,.0f}"

    # Calculate backdated amount
    backdate_years = BACKDATABLE_SLUGS.get(slug)
    if backdate_years and annual_saving:
        backdated_saving = annual_saving * backdate_years
        savings_note += f" — can be backdated {backdate_years} years (up to €{backdated_saving:,.0f} total)"

    return {
        "estimated_annual_saving": annual_saving,
        "estimated_backdated_saving": backdated_saving,
        "savings_note": savings_note,
    }
