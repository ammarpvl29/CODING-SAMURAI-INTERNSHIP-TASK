"""
Data Cleaning Module for Sales Analysis
Author: Ammar Siregar
Purpose: Centralized data cleaning functions for the sales analysis project
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_customers_data(file_path):
    """
    Load and perform basic cleaning on customers data
    """
    try:
        customers = pd.read_csv(file_path, encoding='latin-1')
        print(f"✓ Loaded {len(customers)} customer records")
        return customers
    except Exception as e:
        print(f"Error loading customers data: {e}")
        return None

def load_products_data(file_path):
    """
    Load and perform basic cleaning on products data
    """
    try:
        products = pd.read_csv(file_path)
        print(f"✓ Loaded {len(products)} product records")
        return products
    except Exception as e:
        print(f"Error loading products data: {e}")
        return None

def load_sales_data(file_path):
    """
    Load and perform basic cleaning on sales data
    """
    try:
        sales = pd.read_csv(file_path)
        print(f"✓ Loaded {len(sales)} sales records")
        return sales
    except Exception as e:
        print(f"Error loading sales data: {e}")
        return None

def load_stores_data(file_path):
    """
    Load and perform basic cleaning on stores data
    """
    try:
        stores = pd.read_csv(file_path)
        print(f"✓ Loaded {len(stores)} store records")
        return stores
    except Exception as e:
        print(f"Error loading stores data: {e}")
        return None

def load_exchange_rates_data(file_path):
    """
    Load and perform basic cleaning on exchange rates data
    """
    try:
        exchange_rates = pd.read_csv(file_path)
        print(f"✓ Loaded {len(exchange_rates)} exchange rate records")
        return exchange_rates
    except Exception as e:
        print(f"Error loading exchange rates data: {e}")
        return None

def clean_date_columns(sales_df):
    """
    Clean and convert date columns in sales data
    """
    sales = sales_df.copy()
    
    # Convert date columns to datetime
    date_columns = ['Order Date', 'Delivery Date']
    for col in date_columns:
        if col in sales.columns:
            sales[col] = pd.to_datetime(sales[col], errors='coerce')
    
    return sales

def clean_customer_dates(customers_df):
    """
    Clean date columns in customers data
    """
    customers = customers_df.copy()
    
    if 'Birthday' in customers.columns:
        customers['Birthday'] = pd.to_datetime(customers['Birthday'], errors='coerce')
    
    return customers

def clean_store_dates(stores_df):
    """
    Clean date columns in stores data
    """
    stores = stores_df.copy()
    
    if 'Open Date' in stores.columns:
        stores['Open Date'] = pd.to_datetime(stores['Open Date'], errors='coerce')
    
    return stores

def clean_exchange_dates(exchange_rates_df):
    """
    Clean date columns in exchange rates data
    """
    exchange_rates = exchange_rates_df.copy()
    
    if 'Date' in exchange_rates.columns:
        exchange_rates['Date'] = pd.to_datetime(exchange_rates['Date'], errors='coerce')
    
    return exchange_rates

def clean_price_columns(products_df):
    """
    Clean and convert price columns to numeric values
    """
    products = products_df.copy()
    
    price_columns = ['Unit Cost USD', 'Unit Price USD']
    
    for col in price_columns:
        if col in products.columns:
            # Remove dollar signs, commas, and whitespace, then convert to float
            products[col] = pd.to_numeric(
                products[col].astype(str)
                .str.replace('$', '', regex=False)
                .str.replace(',', '', regex=False)
                .str.strip(),
                errors='coerce'
            )
    
    return products

def handle_missing_values(df):
    """
    Handle missing values in dataset based on column types and business logic
    """
    df_clean = df.copy()
    
    # For numeric columns, we generally keep NaN for now
    # For categorical columns, we might fill with 'Unknown' if appropriate
    # For dates, we keep NaT (Not a Time) values as they might be meaningful
    
    # Specific handling based on common patterns
    if 'Delivery Date' in df_clean.columns:
        # Missing delivery dates are common for recent orders or returns
        pass  # Keep as NaT
    
    if 'Square Meters' in df_clean.columns:
        # Fill missing store sizes with median
        median_size = df_clean['Square Meters'].median()
        df_clean['Square Meters'].fillna(median_size, inplace=True)
    
    return df_clean

def validate_cleaned_data(sales, products, customers, stores):
    """
    Validate the cleaned data for common issues
    """
    validation_results = {}
    
    # Check for required columns
    validation_results['Sales has required columns'] = all(
        col in sales.columns for col in ['Order Number', 'CustomerKey', 'ProductKey', 'StoreKey']
    )
    
    validation_results['Products has required columns'] = all(
        col in products.columns for col in ['ProductKey', 'Unit Cost USD', 'Unit Price USD']
    )
    
    validation_results['Customers has required columns'] = all(
        col in customers.columns for col in ['CustomerKey', 'Name']
    )
    
    validation_results['Stores has required columns'] = all(
        col in stores.columns for col in ['StoreKey', 'Country']
    )
    
    # Check for negative values in price columns
    if 'Unit Cost USD' in products.columns and 'Unit Price USD' in products.columns:
        validation_results['No negative prices'] = (
            (products['Unit Cost USD'] >= 0).all() and 
            (products['Unit Price USD'] >= 0).all()
        )
    
    # Check for reasonable date ranges
    if 'Order Date' in sales.columns:
        min_date = sales['Order Date'].min()
        max_date = sales['Order Date'].max()
        validation_results['Reasonable date range'] = (
            min_date >= pd.Timestamp('2000-01-01') and 
            max_date <= pd.Timestamp('2030-01-01')
        )
    
    # Check for duplicate keys
    validation_results['No duplicate ProductKeys'] = not products['ProductKey'].duplicated().any()
    validation_results['No duplicate CustomerKeys'] = not customers['CustomerKey'].duplicated().any()
    validation_results['No duplicate StoreKeys'] = not stores['StoreKey'].duplicated().any()
    
    return validation_results

def create_analysis_features(sales_analysis_df):
    """
    Create additional features for analysis
    """
    df = sales_analysis_df.copy()
    
    # Calculate revenue, cost, and profit
    if all(col in df.columns for col in ['Quantity', 'Unit Price USD', 'Unit Cost USD']):
        df['Revenue'] = df['Quantity'] * df['Unit Price USD']
        df['Cost'] = df['Quantity'] * df['Unit Cost USD']
        df['Profit'] = df['Revenue'] - df['Cost']
        df['Profit Margin'] = (df['Profit'] / df['Revenue']) * 100
    
    # Extract date features
    if 'Order Date' in df.columns:
        df['Year'] = df['Order Date'].dt.year
        df['Month'] = df['Order Date'].dt.month
        df['Quarter'] = df['Order Date'].dt.quarter
        df['Day of Week'] = df['Order Date'].dt.day_name()
        df['Month Name'] = df['Order Date'].dt.month_name()
        df['Week of Year'] = df['Order Date'].dt.isocalendar().week
    
    # Customer age calculation
    if all(col in df.columns for col in ['Order Date', 'Birthday']):
        df['Customer Age'] = (df['Order Date'] - df['Birthday']).dt.days / 365.25
        df['Age Group'] = pd.cut(df['Customer Age'], 
                               bins=[0, 25, 35, 45, 55, 65, 100], 
                               labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
    
    # Delivery time analysis
    if all(col in df.columns for col in ['Delivery Date', 'Order Date']):
        df['Delivery Days'] = (df['Delivery Date'] - df['Order Date']).dt.days
    
    return df

def generate_data_quality_report(df, dataset_name):
    """
    Generate a comprehensive data quality report
    """
    report = {
        'Dataset': dataset_name,
        'Total Records': len(df),
        'Total Columns': len(df.columns),
        'Missing Values': df.isnull().sum().sum(),
        'Duplicate Rows': df.duplicated().sum(),
        'Data Types': df.dtypes.value_counts().to_dict(),
        'Memory Usage (MB)': df.memory_usage(deep=True).sum() / 1024**2
    }
    
    # Add column-specific information
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    datetime_columns = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    report['Numeric Columns'] = len(numeric_columns)
    report['Categorical Columns'] = len(categorical_columns)
    report['Datetime Columns'] = len(datetime_columns)
    
    return report

if __name__ == "__main__":
    # Test the cleaning functions if run directly
    print("Data Cleaning Module")
    print("===================")
    print("This module contains functions for cleaning the sales analysis data.")
    print("Import this module in your notebooks to use the cleaning functions.")
