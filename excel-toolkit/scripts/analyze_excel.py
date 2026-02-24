#!/usr/bin/env python3
"""
Analyze Excel data and produce statistical summary as JSON.
Usage: python analyze_excel.py <file.xlsx> [--sheet SheetName] [--correlations] [--top N]
"""
import json, sys, argparse
from pathlib import Path

def analyze(filepath, sheet_name=None, correlations=False, top_n=10):
    import pandas as pd
    import numpy as np
    
    kwargs = {"sheet_name": sheet_name} if sheet_name else {"sheet_name": 0}
    df = pd.read_excel(filepath, **kwargs)
    
    result = {
        "file": str(filepath),
        "shape": {"rows": df.shape[0], "columns": df.shape[1]},
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isnull().sum().to_dict(),
        "missing_pct": (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
    }
    
    # Numeric summary
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        desc = df[numeric_cols].describe().round(4)
        result["numeric_summary"] = desc.to_dict()
        
        # Top/bottom values
        result["extremes"] = {}
        for col in numeric_cols[:top_n]:
            result["extremes"][col] = {
                "min": float(df[col].min()) if pd.notna(df[col].min()) else None,
                "max": float(df[col].max()) if pd.notna(df[col].max()) else None,
                "median": float(df[col].median()) if pd.notna(df[col].median()) else None,
            }
        
        if correlations and len(numeric_cols) > 1:
            corr = df[numeric_cols].corr().round(4)
            result["correlations"] = corr.to_dict()
    
    # Categorical summary
    cat_cols = df.select_dtypes(include=["object", "category", "str"]).columns.tolist()
    if cat_cols:
        result["categorical_summary"] = {}
        for col in cat_cols[:top_n]:
            vc = df[col].value_counts().head(10)
            result["categorical_summary"][col] = {
                "unique_count": int(df[col].nunique()),
                "top_values": vc.to_dict(),
            }
    
    # Date columns
    date_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()
    if date_cols:
        result["date_summary"] = {}
        for col in date_cols:
            result["date_summary"][col] = {
                "min": str(df[col].min()),
                "max": str(df[col].max()),
                "range_days": (df[col].max() - df[col].min()).days if pd.notna(df[col].min()) else None,
            }
    
    # Duplicate detection
    dup_count = df.duplicated().sum()
    result["duplicates"] = {"count": int(dup_count), "pct": round(dup_count / len(df) * 100, 2) if len(df) > 0 else 0}
    
    return result

def main():
    parser = argparse.ArgumentParser(description="Analyze Excel data")
    parser.add_argument("file", help="Excel file path")
    parser.add_argument("--sheet", help="Sheet name (default: first sheet)")
    parser.add_argument("--correlations", action="store_true", help="Include correlation matrix")
    parser.add_argument("--top", type=int, default=10, help="Top N columns for detailed analysis")
    args = parser.parse_args()
    
    if not Path(args.file).exists():
        print(json.dumps({"error": f"File not found: {args.file}"}))
        sys.exit(1)
    
    result = analyze(args.file, args.sheet, args.correlations, args.top)
    print(json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    main()
