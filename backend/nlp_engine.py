import pandas as pd
import risk_model
import data_profiler
from data_loader import load_and_prep_data

def process_query(query: str):
    """
    Parses a natural language query and returns a structured data response.
    """
    query = query.lower()
    
    # Intent 1: Feature Importance / Influence
    if "influence" in query or "important" in query or "factors" in query:
        model = risk_model.load_model()
        if not model:
            return {"answer": "Model not trained yet. Cannot determine feature importance."}
        
        # Get feature names from data loader (need a way to get them, recreating here for simplicity or we export it)
        # Using a helper to get feature names
        X, _ = load_and_prep_data()
        feature_names = X.columns.tolist()
        importances = model.feature_importances_
        
        # Zip and sort
        feats = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
        
        top_3 = feats[:3]
        text_response = "The top 3 factors influencing loan risk are: " + ", ".join([f"{f[0]} ({f[1]*100:.1f}%)" for f in top_3])
        
        return {
            "type": "feature_importance",
            "text": text_response,
            "data": [{"feature": f, "importance": i} for f, i in feats]
        }
        
    # Intent 2: Outliers / Anomalies
    if "anomalies" in query or "outlier" in query or "weird" in query:
        profile = data_profiler.generate_profile()
        outliers = profile.get("outliers", [])
        
        if not outliers:
            return {"text": "No significant outliers detected in the dataset."}
            
        summary = ", ".join([f"{o['column']} ({o['count']} records)" for o in outliers])
        return {
            "type": "outliers",
            "text": f"Found statistical anomalies in: {summary}.",
            "data": outliers
        }
    
    # Intent 3: Data Quality
    if "quality" in query or "missing" in query or "clean" in query:
        profile = data_profiler.generate_profile()
        issues = profile.get("quality_issues", {})
        missing = issues.get("missing_values_count", 0)
        dupes = issues.get("duplicate_rows", 0)
        
        return {
            "type": "data_quality",
            "text": f"Data Health Report: Found {missing} missing values and {dupes} duplicate rows.",
            "data": issues
        }

    # Intent 4: General Stats / Distribution
    if "distribution" in query or "breakdown" in query:
        # Check for specific columns
        # Mocking generic response for now
        return {
            "type": "distribution",
            "text": "Distribution analysis requires a specific column name (e.g., 'distribution of Income'). Showing general Property Area breakdown.",
            # We could parse column names dynamically here
        }

    return {
        "text": "I didn't understand that query. Try asking about 'influential factors', 'outliers', or 'data quality'."
    }
