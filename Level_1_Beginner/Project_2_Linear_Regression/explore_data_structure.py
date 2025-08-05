#!/usr/bin/env python
# coding: utf-8

"""
Data Structure Explorer
Explores all CSV files in the dataset to understand their structure and data types
Author: Ammar Siregar
Coding Samurai Internship
"""

import pandas as pd
import os
import numpy as np

def explore_csv_structure(file_path, file_name):
    """
    Explore the structure of a CSV file
    """
    print("="*80)
    print(f"EXPLORING: {file_name}")
    print("="*80)
    
    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                print(f"✅ Successfully loaded with encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            print("❌ Failed to load file with any encoding")
            return
        
        # Basic info
        print(f"\n📊 BASIC INFORMATION:")
        print(f"Shape: {df.shape}")
        print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Column information
        print(f"\n📋 COLUMNS AND DATA TYPES:")
        print("-" * 60)
        for i, (col, dtype) in enumerate(zip(df.columns, df.dtypes), 1):
            null_count = df[col].isnull().sum()
            null_pct = (null_count / len(df)) * 100
            unique_count = df[col].nunique()
            
            print(f"{i:2d}. {col:<25} | {str(dtype):<12} | Nulls: {null_count:>6} ({null_pct:5.1f}%) | Unique: {unique_count:>6}")
        
        # Sample data
        print(f"\n👀 FIRST 3 ROWS:")
        print("-" * 80)
        print(df.head(3).to_string())
        
        # Data summary for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(f"\n📈 NUMERIC COLUMNS SUMMARY:")
            print("-" * 80)
            print(df[numeric_cols].describe())
        
        # Categorical columns info
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            print(f"\n📝 CATEGORICAL COLUMNS INFO:")
            print("-" * 80)
            for col in categorical_cols[:5]:  # Show first 5 categorical columns
                unique_vals = df[col].unique()
                print(f"{col}: {len(unique_vals)} unique values")
                if len(unique_vals) <= 10:
                    print(f"  Values: {list(unique_vals)}")
                else:
                    print(f"  Sample values: {list(unique_vals[:10])}")
                print()
        
        print("\n" + "="*80 + "\n")
        
    except Exception as e:
        print(f"❌ Error loading {file_name}: {str(e)}")
        print("="*80 + "\n")

def main():
    """
    Main function to explore all CSV files
    """
    print("🔍 DATA STRUCTURE EXPLORER")
    print("="*80)
    
    # Define paths to explore
    raw_data_path = "data/raw"
    processed_data_path = "data/processed"
    
    # Explore raw data files
    print("\n🗂️  EXPLORING RAW DATA FILES")
    print("="*80)
    
    raw_files = [
        "Customers.csv",
        "Products.csv", 
        "Sales.csv",
        "Stores.csv",
        "Exchange_Rates.csv",
        "Data_Dictionary.csv"
    ]
    
    for file_name in raw_files:
        file_path = os.path.join(raw_data_path, file_name)
        if os.path.exists(file_path):
            explore_csv_structure(file_path, f"RAW: {file_name}")
        else:
            print(f"⚠️  File not found: {file_path}")
    
    # Explore processed data files
    print("\n🗂️  EXPLORING PROCESSED DATA FILES")
    print("="*80)
    
    if os.path.exists(processed_data_path):
        processed_files = [f for f in os.listdir(processed_data_path) if f.endswith('.csv')]
        
        for file_name in processed_files:
            file_path = os.path.join(processed_data_path, file_name)
            explore_csv_structure(file_path, f"PROCESSED: {file_name}")
    else:
        print("⚠️  Processed data directory not found")
    
    print("\n✅ DATA EXPLORATION COMPLETE!")
    print("="*80)

if __name__ == "__main__":
    main()
