import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from data_loader import load_and_prep_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'risk_model.pkl')

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

def train_and_save_model():
    print("Loading data...")
    X, y = load_and_prep_data()
    
    print("Training Random Forest Classifier...")
    # Using class_weight='balanced' to handle potential skew
    clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight='balanced')
    clf.fit(X, y)
    
    print(f"Model Accuracy: {clf.score(X, y):.2f}")
    
    print(f"Saving model to {MODEL_PATH}...")
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(clf, f)
    
    return clf

def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    train_and_save_model()
