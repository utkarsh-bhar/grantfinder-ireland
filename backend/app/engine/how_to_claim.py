"""
Revenue myAccount step-by-step claiming instructions for each tax credit/relief.

These are included in the scan results and the PDF report to help users
actually claim what they're entitled to.
"""

HOW_TO_CLAIM: dict[str, str] = {
    "personal-tax-credit": (
        "This credit is automatically applied to all taxpayers. "
        "Check your Tax Credit Certificate on Revenue myAccount "
        "(myAccount → Review your tax → Statement of Liability) to confirm it's applied."
    ),

    "paye-tax-credit": (
        "Automatically applied if you're a PAYE employee. "
        "Verify on myAccount → Manage Your Tax → Tax Credits & Reliefs → "
        "check 'Employee Tax Credit' is listed."
    ),

    "earned-income-tax-credit": (
        "Claim when filing your annual tax return (Form 11). "
        "Go to ROS.ie → File a Return → Income Tax Return (Form 11) → "
        "the Earned Income Credit will be calculated automatically."
    ),

    "rent-tax-credit": (
        "1. Log in to Revenue myAccount at revenue.ie\n"
        "2. Go to 'Manage Your Tax 2024' (or current year)\n"
        "3. Select 'Claim Tax Credits'\n"
        "4. Select 'Rent Tax Credit' from the list\n"
        "5. Enter your landlord's name, address, and PPSN/Tax Reference (if known)\n"
        "6. Enter the total rent paid during the year\n"
        "7. Submit — the credit will be applied to your next payslip or as a refund"
    ),

    "home-carer-tax-credit": (
        "1. Log in to Revenue myAccount\n"
        "2. Go to 'Manage Your Tax' → 'Tax Credits & Reliefs'\n"
        "3. Select 'Home Carer Tax Credit'\n"
        "4. Enter the carer's income details (must be under €7,200 for full credit)\n"
        "5. Submit — credit will be applied to jointly assessed couple's tax"
    ),

    "single-person-child-carer-credit": (
        "1. Log in to Revenue myAccount\n"
        "2. Go to 'Manage Your Tax' → 'Tax Credits & Reliefs'\n"
        "3. Select 'Single Person Child Carer Credit'\n"
        "4. Enter your qualifying child's details\n"
        "5. Confirm you are the primary claimant and the child lives with you\n"
        "6. Submit — your tax band will also increase by €4,000"
    ),

    "dependent-relative-tax-credit": (
        "1. Log in to Revenue myAccount\n"
        "2. Go to 'Manage Your Tax' → 'Tax Credits & Reliefs'\n"
        "3. Select 'Dependent Relative Tax Credit'\n"
        "4. Enter your relative's name, relationship, and income details\n"
        "5. Confirm their income is below €18,028\n"
        "6. Submit — you can also backdate this for up to 4 previous years"
    ),

    "age-tax-credit": (
        "Usually applied automatically once Revenue has your date of birth. "
        "If not applied, log in to myAccount → Manage Your Tax → Tax Credits & Reliefs → "
        "check for 'Age Tax Credit'. Contact Revenue if missing."
    ),

    "blind-persons-tax-credit": (
        "1. Get a certificate from your ophthalmologist confirming your visual impairment\n"
        "2. Log in to Revenue myAccount\n"
        "3. Go to 'Manage Your Tax' → 'Tax Credits & Reliefs'\n"
        "4. Select 'Blind Person's Tax Credit'\n"
        "5. Upload or post the medical certificate to Revenue\n"
        "6. Also claim the Guide Dog Allowance of €825 if applicable"
    ),

    "widowed-person-tax-credit": (
        "1. Notify Revenue of your bereavement via myAccount or by phone\n"
        "2. Revenue will update your tax credits automatically\n"
        "3. Check myAccount → Tax Credits & Reliefs to confirm the credit is applied\n"
        "4. In the year of bereavement, you keep the full Married Person's Tax Credit"
    ),

    "widowed-parent-tax-credit": (
        "1. Notify Revenue of your bereavement and confirm you have dependent children\n"
        "2. Go to myAccount → Manage Your Tax → Tax Credits & Reliefs\n"
        "3. The Widowed Parent Tax Credit will be applied for 5 years\n"
        "4. It decreases each year: €3,600 → €3,150 → €2,700 → €2,250 → €1,800"
    ),

    "incapacitated-child-tax-credit": (
        "1. Download Form IC1 from revenue.ie\n"
        "2. Have your child's doctor complete Section B of the form\n"
        "3. Complete Section A yourself with your details\n"
        "4. Submit the form to Revenue via myAccount or by post\n"
        "5. Revenue will review and apply the credit if approved"
    ),

    "medical-expenses-tax-relief": (
        "1. Log in to Revenue myAccount\n"
        "2. Go to 'Review Your Tax' → select the tax year\n"
        "3. Click 'Complete Return' → go to 'Health' section\n"
        "4. Enter your total medical expenses for the year\n"
        "5. Subtract any insurance reimbursements\n"
        "6. Enter the net amount — Revenue calculates 20% relief automatically\n"
        "7. Keep all receipts for 6 years in case of audit"
    ),

    "nursing-home-expenses-tax-relief": (
        "1. Log in to Revenue myAccount\n"
        "2. Go to 'Review Your Tax' → select the tax year\n"
        "3. Under 'Health Expenses', select 'Nursing Home'\n"
        "4. Enter the total nursing home fees paid\n"
        "5. Relief is given at your highest rate of tax (20% or 40%)\n"
        "6. You can claim for fees paid for yourself, spouse, or dependent relative"
    ),

    "remote-working-tax-relief": (
        "1. Log in to Revenue myAccount\n"
        "2. Go to 'Review Your Tax' → select the tax year\n"
        "3. Under 'Employment' section, look for 'Remote Working Relief'\n"
        "4. Enter the number of days worked from home\n"
        "5. Enter your electricity and heating costs for the year\n"
        "6. Relief is 30% of vouched utility costs proportional to WFH days"
    ),

    "mortgage-interest-tax-credit": (
        "1. Get your annual mortgage interest statement from your lender\n"
        "2. Log in to Revenue myAccount\n"
        "3. Go to 'Review Your Tax' → select the claim year\n"
        "4. Go to 'Tax Credits & Reliefs' → 'Mortgage Interest Relief'\n"
        "5. Enter your interest paid for 2022 and the current year\n"
        "6. Revenue will calculate 20% of the increase as your credit\n"
        "7. Maximum credit is €1,250 per property"
    ),

    "tuition-fees-tax-relief": (
        "1. Log in to Revenue myAccount\n"
        "2. Go to 'Review Your Tax' → select the tax year\n"
        "3. Under 'Education', enter the tuition fees paid\n"
        "4. Note: first €3,000 is disregarded for full-time (€1,500 part-time)\n"
        "5. Relief at 20% on the qualifying amount above the disregard"
    ),

    "cycle-to-work-scheme": (
        "1. Ask your employer if they participate in the Cycle to Work Scheme\n"
        "2. Choose a bicycle and safety equipment from an approved retailer\n"
        "3. Your employer purchases it and you repay via salary sacrifice\n"
        "4. You save income tax, PRSI, and USC on the cost\n"
        "5. Limit: €1,250 for standard bikes, €3,500 for e-bikes"
    ),
}
