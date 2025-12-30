import pandas as pd
import numpy as np
from data_loader import load_and_prep_data, DATA_PATH

def generate_profile():
    """
    Analyzes the loaded dataset and returns a comprehensive data quality report.
    """
    try:
        # Load Raw Data (to see missing values before they are filled)
        df_raw = pd.read_csv(DATA_PATH)
    except Exception as e:
        return {"error": str(e)}

    profile = {
        "dataset_name": "Loan Applications (Training Data)",
        "total_rows": len(df_raw),
        "total_columns": len(df_raw.columns),
        "columns": [],
        "quality_issues": {
            "missing_values_count": 0,
            "duplicate_rows": df_raw.duplicated().sum(),
        },
        "outliers": []
    }

    # Column Analysis
    for col in df_raw.columns:
        col_data = df_raw[col]
        col_type = str(col_data.dtype)
        missing = col_data.isnull().sum()
        
        profile["quality_issues"]["missing_values_count"] += int(missing)
        
        col_stats = {
            "name": col,
            "type": col_type,
            "missing": int(missing),
            "missing_pct": round((missing / len(df_raw)) * 100, 1),
            "unique_values": col_data.nunique()
        }

        # Numeric Stats
        if pd.api.types.is_numeric_dtype(col_data):
            col_stats["min"] = float(col_data.min()) if not col_data.empty else 0
            col_stats["max"] = float(col_data.max()) if not col_data.empty else 0
            col_stats["mean"] = float(col_data.mean()) if not col_data.empty else 0
            col_stats["median"] = float(col_data.median()) if not col_data.empty else 0
            
            # Outlier Detection (IQR)
            q1 = col_data.quantile(0.25)
            q3 = col_data.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            outliers = df_raw[(col_data < lower_bound) | (col_data > upper_bound)][col]
            if not outliers.empty:
               profile["outliers"].append({
                   "column": col,
                   "count": len(outliers),
                   "thresholds": {"low": float(lower_bound), "high": float(upper_bound)}
               })
        
        else:
            # Categorical Stats
            if col_data.nunique() < 10:
                col_stats["distribution"] = col_data.value_counts().to_dict()
        
        profile["columns"].append(col_stats)

    return profile
