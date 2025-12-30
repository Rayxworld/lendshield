from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
import os
import pandas as pd
import numpy as np

# Import new modules
import data_loader
import risk_model
import fraud_detector
import explainability
import data_profiler
import nlp_engine
import database

# Ensure DB is init
database.init_db()

app = FastAPI(title="LendShield API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model Globally
RISK_MODEL = risk_model.load_model()
if not RISK_MODEL:
    print("WARNING: Model not found. Training now...")
    RISK_MODEL = risk_model.train_and_save_model()

class LoanApplication(BaseModel):
    name: str = "Applicant"
    # Mapping to CSV feature set
    gender: str = "Male"
    married: str = "No"
    dependents: int = 0
    education: str = "Graduate"
    self_employed: str = "No"
    applicant_income: float
    coapplicant_income: float = 0
    loan_amount: float
    loan_term: float = 360
    credit_history: float = 1.0 # 1.0 or 0.0
    property_area: str = "Urban"
    
    # Extra for UI
    doc_id_match: Optional[bool] = True

class UpdateStatusRequest(BaseModel):
    status: str

@app.get("/loans")
def get_loans():
    return database.get_all_loans()

@app.post("/analyze")
def analyze_loan(application: LoanApplication):
    data = application.dict()
    
    # 1. Prepare Data for Model
    X_input = data_loader.process_input_json(data)
    
    # 2. Predict Risk
    if RISK_MODEL:
        # Prob of class 1 (Yes/Approved)
        approval_prob = RISK_MODEL.predict_proba(X_input)[0][1] 
        # Risk is probability of Default, i.e., 1 - Approval
        risk_prob = 1 - approval_prob
        
        risk_score = int(risk_prob * 100)
        
        if risk_prob <= 0.3:
            risk_level = "Low"
        elif risk_prob <= 0.6:
            risk_level = "Medium"
        else:
            risk_level = "High"
    else:
        # Fallback if model training failed widely
        risk_score = 50
        risk_level = "Medium"

    # 3. Detect Fraud
    is_fraud, fraud_reason = fraud_detector.check_fraud_rules(data)
    
    # 4. Explainability
    reasoning = explainability.explain_prediction(data, RISK_MODEL)
    if is_fraud:
        reasoning = f"FRAUD ALERT: {fraud_reason}. " + reasoning
        risk_level = "Critical" # Override
        risk_score = 99

    # 5. Save Record
    result = {
        "name": data['name'],
        "credit_score": int(data['credit_history'] * 700) + 100, # Mock mapping for UI compatibility (1->800, 0->100)
        "annual_income": (data['applicant_income'] + data['coapplicant_income']) * 12, # Convert monthly to annual for old UI stats
        "loan_amount": data['loan_amount'] * 1000, # Convert 'thousands' to raw for old UI
        "doc_id_match": data['doc_id_match'],
        "score": 100 - risk_score, # Old UI expected 'Safety Score' (100 = Good), logic here calculated Risk (100 = Bad)
        "risk_level": risk_level,
        "reasoning": reasoning,
        "is_fraud": is_fraud,
        "alerts": [fraud_reason] if fraud_reason else [],
        "status": "Rejected" if is_fraud else "Pending"
    }
    
    try:
        new_id = database.add_loan(result)
        result['id'] = new_id
    except Exception as e:
        print(f"DB Error: {e}")
        result['id'] = 9999
        
    return result

@app.put("/loans/{loan_id}")
def update_loan_status(loan_id: int, request: UpdateStatusRequest):
    database.update_loan_status(loan_id, request.status)
    return {"id": loan_id, "status": request.status}

@app.get("/portfolio")
def get_portfolio_stats():
    loans = database.get_all_loans()
    df = pd.DataFrame(loans)
    if df.empty:
        return {
            "total_loans": 0,
            "total_exposure": 0,
            "risk_distribution": {"Low": 0, "Medium": 0, "High": 0},
            "fraud_cases": 0,
            "status_distribution": {}
        }
    
    return {
        "total_loans": len(df),
        "total_exposure": int(df['loan_amount'].sum()),
        "risk_distribution": df['risk_level'].value_counts().to_dict(),
        "fraud_cases": int(df['is_fraud'].sum()),
        "status_distribution": df['status'].value_counts().to_dict()
    }

# --- Intelligence Layer Endpoints ---

@app.get("/data-profile")
def get_data_profile():
    return data_profiler.generate_profile()

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask_data(request: QueryRequest):
    return nlp_engine.process_query(request.query)

# ------------------------------------

@app.delete("/loans")
def clear_db():
    database.clear_all_loans()
    return {"status": "cleared"}

if __name__ == "__main__":
    import uvicorn
    # Train on startup if needed
    if not os.path.exists(risk_model.MODEL_PATH):
        risk_model.train_and_save_model()
        
    print("Starting LendShield Intelligence Engine...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
