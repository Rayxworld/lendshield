import pandas as pd
import numpy as np
import os

# Define path relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'train_u6lujuX_CVtuZ9i.csv')

def load_and_prep_data():
    """
    Loads the training data, handles missing values, and encodes features.
    Returns: X (features), y (target), preprocessor (encoders if needed)
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # 1. Handle Missing Values
    # Categorical: Fill with Mode
    for col in ['Gender', 'Married', 'Dependents', 'Self_Employed']:
        df[col] = df[col].fillna(df[col].mode()[0])
    
    # Numerical: Fill with Median
    df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].median())
    df['Loan_Amount_Term'] = df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].median())
    df['Credit_History'] = df['Credit_History'].fillna(0) # Assume 0 if unknown (conservative risk)

    # 2. Feature Engineering
    # 'Dependents': '3+' -> 3
    df['Dependents'] = df['Dependents'].replace('3+', 3).astype(int)

    # 3. Encoding
    # Target: Y -> 1, N -> 0
    df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})

    # Features
    # We will use simple numeric mapping for simplicity and consistency with input JSON
    # Male:1, Female:0
    df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})
    # Yes:1, No:0
    df['Married'] = df['Married'].map({'Yes': 1, 'No': 0})
    # Graduate:1, Not Graduate:0
    df['Education'] = df['Education'].map({'Graduate': 1, 'Not Graduate': 0})
    # Yes:1, No:0
    df['Self_Employed'] = df['Self_Employed'].map({'Yes': 1, 'No': 0})
    
    # Property Area: Urban:2, Semiurban:1, Rural:0 (Ordinal assumption)
    df['Property_Area'] = df['Property_Area'].map({'Urban': 2, 'Semiurban': 1, 'Rural': 0})

    # Drop ID
    df = df.drop(columns=['Loan_ID'])

    X = df.drop(columns=['Loan_Status'])
    y = df['Loan_Status']

    return X, y

def process_input_json(input_data: dict):
    """
    Converts API input JSON into the same format/order as training data X.
    """
    # Default mappings
    # Note: Input names might differ, need to map carefully
    # Expected Input: 
    # { "gender": "Male", "married": "Yes", "dependents": 0, "education": "Graduate",
    #   "self_employed": "No", "applicant_income": 5000, "coapplicant_income": 0,
    #   "loan_amount": 100, "loan_term": 360, "credit_history": 1, "property_area": "Urban" }
    
    row = [
        1 if input_data.get('gender') == 'Male' else 0,
        1 if input_data.get('married') == 'Yes' else 0,
        int(str(input_data.get('dependents', 0)).replace('3+', '3')),
        1 if input_data.get('education') == 'Graduate' else 0,
        1 if input_data.get('self_employed') == 'Yes' else 0,
        float(input_data.get('applicant_income', 0)),
        float(input_data.get('coapplicant_income', 0)),
        float(input_data.get('loan_amount', 0)),
        float(input_data.get('loan_term', 360)),
        float(input_data.get('credit_history', 0)),
        {'Urban': 2, 'Semiurban': 1, 'Rural': 0}.get(input_data.get('property_area', 'Urban'), 1)
    ]
    
    # Return as list of list (single sample)
    return [row]
