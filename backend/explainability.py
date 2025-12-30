def explain_prediction(input_data: dict, model):
    """
    Generates a plain-English narrative explaining the risk score.
    Uses input data context combined with model heuristics.
    """
    reasons = []
    narrative = []
    
    # Extract key values
    credit_hist = input_data.get('credit_history', 0)
    income = (input_data.get('applicant_income', 0) + input_data.get('coapplicant_income', 0))
    loan_amount = input_data.get('loan_amount', 0) * 1000
    term = input_data.get('loan_term', 360)
    
    # 1. Credit History Context (The Heavy Hitter)
    if credit_hist == 0:
        narrative.append("The primary driver is the lack of verifiable credit history.")
    else:
        narrative.append("Credit history verifies positively.")

    # 2. Financial Strain (Debt-to-Income Proxy)
    if income > 0 and term > 0:
        monthly_payment = loan_amount / term
        dti = monthly_payment / income
        
        if dti > 0.4:
            narrative.append(f"The loan amount (${loan_amount:,.0f}) is high relative to reported income, causing significant monthly repayment strain.")
        elif dti < 0.2:
            narrative.append("The requested loan amount is comfortably within the applicant's income capacity.")
    
    # 3. Stability Indicators
    stability_points = 0
    if input_data.get('married') == 'Yes': stability_points += 1
    if input_data.get('education') == 'Graduate': stability_points += 1
    if input_data.get('property_area') != 'Rural': stability_points += 1
    
    if stability_points >= 2:
        narrative.append("Applicant demonstrates strong demographic stability factors.")
    elif stability_points == 0:
         narrative.append("The profile lacks typical stability indicators (e.g., Education, Property Area).")

    # Combine into a cohesive story
    full_text = " ".join(narrative)
    
    # Fallback if text is too short
    if len(full_text) < 20:
        return "Risk score calculated based on standard underwriting criteria including credit history and income ratios."
        
    return full_text
