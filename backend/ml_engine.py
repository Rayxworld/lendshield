import random
import pandas as pd
import numpy as np
import pickle
import os

# Mock Fraud Database
BLACKLISTED_NAMES = ["John Doe", "Jane Smith", "Fraudster X"]

# Load Model if exists
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'risk_model.pkl')
try:
    with open(MODEL_PATH, 'rb') as f:
        RISK_MODEL = pickle.load(f)
        print("Scikit-learn model loaded successfully.")
except:
    print("Warning: Model not found. Using fallback logic.")
    RISK_MODEL = None

def calculate_risk_score(application_data: dict):
    """
    Uses trained Random Forest model if available, else fallback logic.
    """
    score = 0
    risk_level = "Medium"
    reasoning = []
    
    credit_score = application_data.get("credit_score", 0)
    income = application_data.get("annual_income", 0)
    loan = application_data.get("loan_amount", 0)

    # Use ML Model
    if RISK_MODEL:
        # Predict probability of being High Risk (1)
        # We want a "Safety Score" (0-100), so we take prob of class 0 (Low Risk) * 100
        input_data = pd.DataFrame([[credit_score, income, loan]], 
                                columns=['credit_score', 'annual_income', 'loan_amount'])
        
        # Prob of class 1 (Risk)
        risk_prob = RISK_MODEL.predict_proba(input_data)[0][1]
        
        # UI Score: 100 = Safe, 0 = Risky
        score = int((1 - risk_prob) * 100)
        
        if score >= 80:
            risk_level = "Low"
        elif score >= 50:
            risk_level = "Medium"
        else:
            risk_level = "High"
            
        # Generate dynamic reasoning based on feature importance (simplified)
        if credit_score < 600:
            reasoning.append("Credit score is a significant risk factor.")
        if loan > (income * 0.5):
            reasoning.append("Loan amount is high relative to income.")
        if not reasoning:
            reasoning.append("AI analysis indicates a stable profile.")
            
    else:
        # FALLBACK LOGIC (Original)
        base = 700
        if credit_score < 600: base -= 100
        elif credit_score > 750: base += 50
        
        dti = loan / (income + 1)
        if dti > 0.5: base -= 150
        
        score = max(0, min(100, int((base - 300) / 8.5 * 2)))
        
        if score >= 80: risk_level = "Low"
        elif score >= 50: risk_level = "Medium"
        else: risk_level = "High"
        reasoning.append("Rule-based fallback estimate.")

    return {
        "score": score,
        "risk_level": risk_level,
        "reasoning": "; ".join(reasoning)
    }

def detect_fraud(application_data: dict):
    alerts = []
    is_fraud = False
    
    name = application_data.get("name", "")
    if any(b.lower() in name.lower() for b in BLACKLISTED_NAMES):
        alerts.append("Name found in fraud blacklist.")
        is_fraud = True
        
    if application_data.get("doc_id_match") is False:
        alerts.append("Document ID does not match provided details.")
        is_fraud = True

    return {
        "is_fraud": is_fraud,
        "alerts": alerts
    }

def generate_sample_data(num_samples=20):
    samples = []
    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace"]
    last_names = ["Brown", "White", "Green", "Black", "Blue", "Red", "Yellow"]
    
    for i in range(num_samples):
        item = {
            "name": f"{random.choice(names)} {random.choice(last_names)}",
            "credit_score": random.randint(500, 850),
            "annual_income": random.randint(30000, 150000),
            "loan_amount": random.randint(5000, 50000),
            "doc_id_match": random.choice([True, True, True, False])
        }
        # pre-calculate
        risk = calculate_risk_score(item)
        fraud = detect_fraud(item)
        
        item.update(risk)
        item.update(fraud)
        samples.append(item)
    return samples
