def check_fraud_rules(application_data: dict, history_df=None):
    """
    Runs rule-based fraud detection.
    Returns: (is_fraud, reason)
    """
    # 1. Check for Duplicate/Suspicious IDs (if present in input)
    # Note: Dataset ID (LP...) is generated, so we might simulate this check 
    # or check against a blacklist if 'name' was passed.
    
    # 2. Loan to Income Ratio
    # High Income Ratio: Loan > 5x Annual Income (Assuming Applicant+Coapp)
    # Income in dataset is monthly usually? Wait, let's assume monthly based on values (~5000). 
    # Annual = (App + Coapp) * 12
    monthly_income = application_data.get('applicant_income', 0) + application_data.get('coapplicant_income', 0)
    annual_income = monthly_income * 12
    loan_amount_raw = application_data.get('loan_amount', 0) 
    
    # In this dataset, LoanAmount is in Thousands?
    # Example: Income 5849, LoanAmount NaN (or 128). 
    # If 128 is 128,000, then 128000 / (5849*12) ~ 1.8. Reasonable.
    # If 128 is 128, that's tiny. Data dictionary usually says 'in thousands'.
    # So Actual Loan = loan_amount * 1000
    
    actual_loan = loan_amount_raw * 1000
    
    if annual_income > 0:
        ratio = actual_loan / annual_income
        if ratio > 6.0:  # Suspiciously high loan for income
            return True, f"High Loan-to-Income Ratio ({ratio:.1f}x)"
    
    # 3. Inconsistent Data
    if application_data.get('credit_history') == 0 and application_data.get('self_employed') == 'Yes' and annual_income > 200000:
       # Verify income source for high-income defaults
       return True, "High Income with Default History requires manual verification"

    return False, None
