"""Irish-specific validators and constants."""

# All 26 counties of the Republic of Ireland
IRISH_COUNTIES = [
    "Carlow", "Cavan", "Clare", "Cork", "Donegal", "Dublin",
    "Galway", "Kerry", "Kildare", "Kilkenny", "Laois", "Leitrim",
    "Limerick", "Longford", "Louth", "Mayo", "Meath", "Monaghan",
    "Offaly", "Roscommon", "Sligo", "Tipperary", "Waterford",
    "Westmeath", "Wexford", "Wicklow",
]

BER_RATINGS = [
    "A1", "A2", "A3",
    "B1", "B2", "B3",
    "C1", "C2", "C3",
    "D1", "D2",
    "E1", "E2",
    "F",
    "G",
]

GRANT_CATEGORIES = [
    ("home_energy", "Home Energy"),
    ("housing", "Housing"),
    ("housing_support", "Housing Support"),
    ("welfare", "Welfare & Social"),
    ("business", "Business"),
    ("education", "Education"),
    ("health", "Health"),
    ("family", "Family"),
    ("disability", "Disability"),
    ("carers", "Carers"),
    ("transport", "Transport"),
    ("farming", "Farming"),
    ("community", "Community"),
    ("tax_relief", "Tax Relief"),
    ("employment", "Employment"),
]

WELFARE_PAYMENT_OPTIONS = [
    ("fuel_allowance", "Fuel Allowance"),
    ("disability_allowance", "Disability Allowance"),
    ("jobseekers_allowance", "Jobseeker's Allowance"),
    ("working_family_payment", "Working Family Payment"),
    ("carers_allowance", "Carer's Allowance"),
    ("one_parent_family_payment", "One Parent Family Payment"),
    ("domiciliary_care_allowance", "Domiciliary Care Allowance"),
    ("state_pension", "State Pension"),
    ("invalidity_pension", "Invalidity Pension"),
]


def validate_county(county: str) -> bool:
    return county in IRISH_COUNTIES


def validate_ber_rating(rating: str) -> bool:
    return rating.upper() in BER_RATINGS
