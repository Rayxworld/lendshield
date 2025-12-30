import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os

# 1. Generate Synthetic Training Data
# Simulating a dataset of historical loan applications
def generate_training_data(n_samples=1000):
    np.random.seed(42)
    
    # Features
    credit_scores = np.random.randint(300, 850, n_samples)
    incomes = np.random.randint(20000, 200000, n_samples)
    loan_amounts = np.random.randint(1000, 50000, n_samples)
    
    # Target variable logic (simulated ground truth)
    # Risk factor calculation
    risk_factors = (
        (850 - credit_scores) / 550 * 0.5 +  # Lower credit score -> higher risk
        (loan_amounts / (incomes + 1)) * 2.0  # Higher DTI -> higher risk
    )
    
    # Add some noise
    risk_factors += np.random.normal(0, 0.1, n_samples)
    
    # Assign labels: 0 = Low Risk (Approved), 1 = High Risk (Rejected)
    labels = (risk_factors > 0.6).astype(int)
    
    df = pd.DataFrame({
        'credit_score': credit_scores,
        'annual_income': incomes,
        'loan_amount': loan_amounts,
        'risk_label': labels
    })
    
    return df

def train():
    print("Generating training data...")
    df = generate_training_data()
    
    X = df[['credit_score', 'annual_income', 'loan_amount']]
    y = df['risk_label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {acc:.2f}")
    
    # Save Model
    with open('risk_model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    print("Model saved to risk_model.pkl")

if __name__ == "__main__":
    train()
