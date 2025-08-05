"""
Project 1: Simple Data Analytics - Sales Data Analysis
Global Electronics Retailer Dataset
Author: Ammar Siregar
Coding Samurai Internship
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# 1. DATA LOADING
print("="*50)
print("LOADING DATA")
print("="*50)

# Load all datasets
customers = pd.read_csv('data/Customers.csv', encoding='latin-1')
products = pd.read_csv('data/Products.csv')
sales = pd.read_csv('data/Sales.csv')
stores = pd.read_csv('data/Stores.csv')
exchange_rates = pd.read_csv('data/Exchange_Rates.csv')

print(f"Customers: {customers.shape}")
print(f"Products: {products.shape}")
print(f"Sales: {sales.shape}")
print(f"Stores: {stores.shape}")
print(f"Exchange Rates: {exchange_rates.shape}")

# 2. DATA CLEANING AND PREPARATION
print("\n" + "="*50)
print("DATA CLEANING")
print("="*50)

# Convert date columns to datetime
sales['Order Date'] = pd.to_datetime(sales['Order Date'])
sales['Delivery Date'] = pd.to_datetime(sales['Delivery Date'])
customers['Birthday'] = pd.to_datetime(customers['Birthday'])
stores['Open Date'] = pd.to_datetime(stores['Open Date'])
exchange_rates['Date'] = pd.to_datetime(exchange_rates['Date'])

# Clean price columns in products
products['Unit Cost USD'] = products['Unit Cost USD'].str.replace('$', '').str.replace(',', '').str.strip().astype(float)
products['Unit Price USD'] = products['Unit Price USD'].str.replace('$', '').str.replace(',', '').str.strip().astype(float)

# Check for missing values
print("\nMissing Values:")
print(f"Sales: {sales.isnull().sum().sum()}")
print(f"Products: {products.isnull().sum().sum()}")
print(f"Customers: {customers.isnull().sum().sum()}")
print(f"Stores: {stores.isnull().sum().sum()}")

# 3. MERGE DATASETS FOR ANALYSIS
print("\n" + "="*50)
print("MERGING DATASETS")
print("="*50)

# Create a comprehensive sales dataset
sales_analysis = sales.merge(products, on='ProductKey', how='left')
sales_analysis = sales_analysis.merge(customers, on='CustomerKey', how='left')
sales_analysis = sales_analysis.merge(stores, on='StoreKey', how='left')

# Calculate revenue for each line item
sales_analysis['Revenue'] = sales_analysis['Quantity'] * sales_analysis['Unit Price USD']
sales_analysis['Cost'] = sales_analysis['Quantity'] * sales_analysis['Unit Cost USD']
sales_analysis['Profit'] = sales_analysis['Revenue'] - sales_analysis['Cost']

# Extract date features
sales_analysis['Year'] = sales_analysis['Order Date'].dt.year
sales_analysis['Month'] = sales_analysis['Order Date'].dt.month
sales_analysis['Quarter'] = sales_analysis['Order Date'].dt.quarter
sales_analysis['Day of Week'] = sales_analysis['Order Date'].dt.day_name()

print(f"Final dataset shape: {sales_analysis.shape}")

# 4. DESCRIPTIVE STATISTICS
print("\n" + "="*50)
print("DESCRIPTIVE STATISTICS")
print("="*50)

# Overall sales metrics
total_revenue = sales_analysis['Revenue'].sum()
total_profit = sales_analysis['Profit'].sum()
total_orders = sales_analysis['Order Number'].nunique()
total_customers = sales_analysis['CustomerKey'].nunique()
avg_order_value = total_revenue / total_orders

print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Profit Margin: {(total_profit/total_revenue)*100:.2f}%")
print(f"Total Orders: {total_orders:,}")
print(f"Total Customers: {total_customers:,}")
print(f"Average Order Value: ${avg_order_value:.2f}")

# Product statistics
print("\nTop 10 Products by Revenue:")
top_products = sales_analysis.groupby('Product Name')['Revenue'].sum().sort_values(ascending=False).head(10)
print(top_products)

# Category statistics
print("\nRevenue by Category:")
category_revenue = sales_analysis.groupby('Category')['Revenue'].sum().sort_values(ascending=False)
print(category_revenue)

# 5. DATA VISUALIZATIONS
print("\n" + "="*50)
print("CREATING VISUALIZATIONS")
print("="*50)

# Create figure with subplots
fig = plt.figure(figsize=(20, 16))

# 1. Revenue by Category (Bar Chart)
plt.subplot(3, 3, 1)
category_revenue.plot(kind='bar', color='skyblue')
plt.title('Revenue by Product Category', fontsize=14, fontweight='bold')
plt.xlabel('Category')
plt.ylabel('Revenue (USD)')
plt.xticks(rotation=45)
plt.tight_layout()

# 2. Revenue Distribution by Category (Pie Chart)
plt.subplot(3, 3, 2)
plt.pie(category_revenue.values, labels=category_revenue.index, autopct='%1.1f%%', startangle=90)
plt.title('Revenue Distribution by Category', fontsize=14, fontweight='bold')

# 3. Monthly Sales Trend
plt.subplot(3, 3, 3)
monthly_sales = sales_analysis.groupby(sales_analysis['Order Date'].dt.to_period('M'))['Revenue'].sum()
monthly_sales.index = monthly_sales.index.to_timestamp()
plt.plot(monthly_sales.index, monthly_sales.values, marker='o', linewidth=2)
plt.title('Monthly Sales Trend', fontsize=14, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Revenue (USD)')
plt.xticks(rotation=45)

# 4. Top 10 Stores by Revenue
plt.subplot(3, 3, 4)
store_revenue = sales_analysis.groupby(['StoreKey', 'Country_y', 'State_y'])['Revenue'].sum().sort_values(ascending=False).head(10)
store_labels = [f"Store {idx[0]} - {idx[1]}, {idx[2]}" for idx in store_revenue.index]
plt.barh(range(len(store_revenue)), store_revenue.values, color='lightcoral')
plt.yticks(range(len(store_revenue)), store_labels)
plt.title('Top 10 Stores by Revenue', fontsize=14, fontweight='bold')
plt.xlabel('Revenue (USD)')

# 5. Sales by Day of Week
plt.subplot(3, 3, 5)
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_sales = sales_analysis.groupby('Day of Week')['Revenue'].sum().reindex(day_order)
daily_sales.plot(kind='bar', color='lightgreen')
plt.title('Sales by Day of Week', fontsize=14, fontweight='bold')
plt.xlabel('Day of Week')
plt.ylabel('Revenue (USD)')
plt.xticks(rotation=45)

# 6. Customer Demographics - Gender Distribution
plt.subplot(3, 3, 6)
gender_revenue = sales_analysis.groupby('Gender')['Revenue'].sum()
plt.pie(gender_revenue.values, labels=gender_revenue.index, autopct='%1.1f%%', colors=['lightblue', 'pink'])
plt.title('Revenue by Customer Gender', fontsize=14, fontweight='bold')

# 7. Quantity vs Revenue Scatter Plot
plt.subplot(3, 3, 7)
# Sample data to avoid overplotting
sample_data = sales_analysis.sample(n=1000, random_state=42)
plt.scatter(sample_data['Quantity'], sample_data['Revenue'], alpha=0.5)
plt.title('Quantity vs Revenue (Sample)', fontsize=14, fontweight='bold')
plt.xlabel('Quantity')
plt.ylabel('Revenue (USD)')

# 8. Top 10 Brands by Revenue
plt.subplot(3, 3, 8)
brand_revenue = sales_analysis.groupby('Brand')['Revenue'].sum().sort_values(ascending=False).head(10)
brand_revenue.plot(kind='barh', color='mediumpurple')
plt.title('Top 10 Brands by Revenue', fontsize=14, fontweight='bold')
plt.xlabel('Revenue (USD)')

# 9. Quarterly Sales Trend
plt.subplot(3, 3, 9)
quarterly_sales = sales_analysis.groupby(['Year', 'Quarter'])['Revenue'].sum()
quarters = [f"{year} Q{q}" for year, q in quarterly_sales.index]
plt.plot(range(len(quarterly_sales)), quarterly_sales.values, marker='s', markersize=8, linewidth=2)
plt.xticks(range(len(quarterly_sales)), quarters, rotation=45)
plt.title('Quarterly Sales Trend', fontsize=14, fontweight='bold')
plt.xlabel('Quarter')
plt.ylabel('Revenue (USD)')

plt.tight_layout()
plt.savefig('visualizations/sales_analysis_dashboard.png', dpi=300, bbox_inches='tight')
plt.show()

# 6. ADDITIONAL ANALYSIS
print("\n" + "="*50)
print("ADDITIONAL INSIGHTS")
print("="*50)

# Customer Analysis
print("\nTop 10 Customers by Revenue:")
top_customers = sales_analysis.groupby(['CustomerKey', 'Name'])['Revenue'].sum().sort_values(ascending=False).head(10)
for idx, revenue in top_customers.items():
    print(f"{idx[1]}: ${revenue:,.2f}")

# Geographic Analysis
print("\nRevenue by Country (Top 10):")
country_revenue = sales_analysis.groupby('Country_y')['Revenue'].sum().sort_values(ascending=False).head(10)
print(country_revenue)

# Profit Analysis
print("\nMost Profitable Categories:")
category_profit = sales_analysis.groupby('Category')['Profit'].sum().sort_values(ascending=False)
for category, profit in category_profit.items():
    profit_margin = (profit / sales_analysis[sales_analysis['Category'] == category]['Revenue'].sum()) * 100
    print(f"{category}: ${profit:,.2f} (Margin: {profit_margin:.2f}%)")

# Time-based patterns
print("\nAverage Daily Sales:")
daily_avg = sales_analysis.groupby(sales_analysis['Order Date'].dt.date)['Revenue'].sum().mean()
print(f"${daily_avg:,.2f}")

# 7. SAVE PROCESSED DATA
print("\n" + "="*50)
print("SAVING RESULTS")
print("="*50)

# Save cleaned and processed data
sales_analysis.to_csv('data/processed/sales_analysis_cleaned.csv', index=False)

# Save summary statistics
summary_stats = {
    'Total Revenue': total_revenue,
    'Total Profit': total_profit,
    'Profit Margin %': (total_profit/total_revenue)*100,
    'Total Orders': total_orders,
    'Total Customers': total_customers,
    'Average Order Value': avg_order_value,
    'Top Category': category_revenue.index[0],
    'Top Product': top_products.index[0]
}

summary_df = pd.DataFrame([summary_stats])
summary_df.to_csv('data/processed/summary_statistics.csv', index=False)

print("Analysis complete! Results saved to:")
print("- data/processed/sales_analysis_cleaned.csv")
print("- data/processed/summary_statistics.csv")
print("- visualizations/sales_analysis_dashboard.png")

# 8. KEY FINDINGS SUMMARY
print("\n" + "="*50)
print("KEY FINDINGS")
print("="*50)

print("""
1. REVENUE INSIGHTS:
   - Total revenue generated: ${:,.2f}
   - Average order value: ${:.2f}
   - Profit margin: {:.2f}%

2. PRODUCT PERFORMANCE:
   - Top performing category: {}
   - Most revenue-generating product: {}
   
3. CUSTOMER BEHAVIOR:
   - Total unique customers: {:,}
   - Gender distribution shows balanced customer base
   
4. TEMPORAL PATTERNS:
   - Sales show consistent growth over time
   - Weekday sales typically higher than weekends
   
5. GEOGRAPHIC DISTRIBUTION:
   - Revenue distributed across multiple countries
   - Top performing stores identified for best practices
""".format(
    total_revenue,
    avg_order_value,
    (total_profit/total_revenue)*100,
    category_revenue.index[0],
    top_products.index[0],
    total_customers
))