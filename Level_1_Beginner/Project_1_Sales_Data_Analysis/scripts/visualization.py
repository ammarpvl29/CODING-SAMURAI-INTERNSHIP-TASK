"""
Visualization Module for Sales Analysis
Author: Ammar Siregar
Purpose: Centralized visualization functions for the sales analysis project
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set default style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def create_category_revenue_chart(sales_df, save_path=None):
    """
    Create a bar chart showing revenue by product category
    """
    category_revenue = sales_df.groupby('Category')['Revenue'].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(12, 8))
    bars = plt.bar(range(len(category_revenue)), category_revenue.values, 
                   color=plt.cm.Set3(np.linspace(0, 1, len(category_revenue))))
    
    plt.title('Revenue by Product Category', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Product Category', fontsize=12)
    plt.ylabel('Revenue (USD)', fontsize=12)
    plt.xticks(range(len(category_revenue)), category_revenue.index, rotation=45, ha='right')
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved to {save_path}")
    
    return plt.gcf()

def create_top_products_chart(sales_df, top_n=15, save_path=None):
    """
    Create a horizontal bar chart showing top products by revenue
    """
    top_products = sales_df.groupby('Product Name')['Revenue'].sum().sort_values(ascending=True).tail(top_n)
    
    plt.figure(figsize=(12, 8))
    bars = plt.barh(range(len(top_products)), top_products.values, color='skyblue')
    
    plt.title(f'Top {top_n} Products by Revenue', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Revenue (USD)', fontsize=12)
    plt.ylabel('Products', fontsize=12)
    plt.yticks(range(len(top_products)), [name[:40] + '...' if len(name) > 40 else name 
                                        for name in top_products.index])
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'${width:,.0f}', ha='left', va='center', fontsize=9)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved to {save_path}")
    
    return plt.gcf()

def create_monthly_trends_chart(sales_df, save_path=None):
    """
    Create a line chart showing monthly sales trends
    """
    monthly_sales = sales_df.groupby(sales_df['Order Date'].dt.to_period('M')).agg({
        'Revenue': 'sum',
        'Profit': 'sum'
    })
    monthly_sales.index = monthly_sales.index.to_timestamp()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Revenue trend
    ax1.plot(monthly_sales.index, monthly_sales['Revenue'], marker='o', linewidth=2, 
             markersize=6, color='#2E8B57')
    ax1.set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Revenue (USD)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Format y-axis labels
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
    
    # Profit trend
    ax2.plot(monthly_sales.index, monthly_sales['Profit'], marker='s', linewidth=2, 
             markersize=6, color='#DC143C')
    ax2.set_title('Monthly Profit Trend', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Month', fontsize=12)
    ax2.set_ylabel('Profit (USD)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)
    
    # Format y-axis labels
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved to {save_path}")
    
    return fig

def create_seasonal_analysis_chart(sales_df):
    """
    Create charts showing seasonal patterns in sales
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Quarterly sales
    quarterly_sales = sales_df.groupby('Quarter')['Revenue'].sum()
    bars1 = ax1.bar(quarterly_sales.index, quarterly_sales.values, color='lightblue')
    ax1.set_title('Revenue by Quarter', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Quarter')
    ax1.set_ylabel('Revenue (USD)')
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'${height/1e6:.1f}M', ha='center', va='bottom')
    
    # Monthly sales
    monthly_sales = sales_df.groupby('Month')['Revenue'].sum()
    ax2.plot(monthly_sales.index, monthly_sales.values, marker='o', linewidth=2)
    ax2.set_title('Revenue by Month', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Revenue (USD)')
    ax2.set_xticks(range(1, 13))
    ax2.grid(True, alpha=0.3)
    
    # Day of week analysis
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_sales = sales_df.groupby('Day of Week')['Revenue'].sum().reindex(day_order)
    bars3 = ax3.bar(range(len(daily_sales)), daily_sales.values, color='lightgreen')
    ax3.set_title('Revenue by Day of Week', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Day of Week')
    ax3.set_ylabel('Revenue (USD)')
    ax3.set_xticks(range(len(daily_sales)))
    ax3.set_xticklabels([day[:3] for day in daily_sales.index], rotation=45)
    
    # Yearly trend
    yearly_sales = sales_df.groupby('Year')['Revenue'].sum()
    bars4 = ax4.bar(yearly_sales.index, yearly_sales.values, color='coral')
    ax4.set_title('Revenue by Year', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Revenue (USD)')
    for bar in bars4:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'${height/1e6:.1f}M', ha='center', va='bottom')
    
    plt.tight_layout()
    return fig

def create_customer_demographics_chart(sales_df):
    """
    Create charts showing customer demographics analysis
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Gender distribution by revenue
    gender_revenue = sales_df.groupby('Gender')['Revenue'].sum()
    colors1 = ['lightblue', 'pink']
    wedges1, texts1, autotexts1 = ax1.pie(gender_revenue.values, labels=gender_revenue.index, 
                                          autopct='%1.1f%%', colors=colors1, startangle=90)
    ax1.set_title('Revenue Distribution by Gender', fontsize=14, fontweight='bold')
    
    # Age group analysis
    age_revenue = sales_df.groupby('Age Group')['Revenue'].sum()
    bars2 = ax2.bar(range(len(age_revenue)), age_revenue.values, color='mediumpurple')
    ax2.set_title('Revenue by Age Group', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Age Group')
    ax2.set_ylabel('Revenue (USD)')
    ax2.set_xticks(range(len(age_revenue)))
    ax2.set_xticklabels(age_revenue.index, rotation=45)
    
    # Customer count by gender
    gender_customers = sales_df.groupby('Gender')['CustomerKey'].nunique()
    bars3 = ax3.bar(gender_customers.index, gender_customers.values, color=['lightblue', 'pink'])
    ax3.set_title('Customer Count by Gender', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Gender')
    ax3.set_ylabel('Number of Customers')
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}', ha='center', va='bottom')
    
    # Age group customer count
    age_customers = sales_df.groupby('Age Group')['CustomerKey'].nunique()
    bars4 = ax4.bar(range(len(age_customers)), age_customers.values, color='lightcoral')
    ax4.set_title('Customer Count by Age Group', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Age Group')
    ax4.set_ylabel('Number of Customers')
    ax4.set_xticks(range(len(age_customers)))
    ax4.set_xticklabels(age_customers.index, rotation=45)
    
    plt.tight_layout()
    return fig

def create_geographic_analysis_chart(sales_df):
    """
    Create charts showing geographic analysis
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Revenue by country
    country_revenue = sales_df.groupby('Country_y')['Revenue'].sum().sort_values(ascending=True)
    bars1 = ax1.barh(range(len(country_revenue)), country_revenue.values, color='lightseagreen')
    ax1.set_title('Revenue by Country', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Revenue (USD)')
    ax1.set_ylabel('Country')
    ax1.set_yticks(range(len(country_revenue)))
    ax1.set_yticklabels(country_revenue.index)
    
    # Add value labels
    for i, bar in enumerate(bars1):
        width = bar.get_width()
        ax1.text(width, bar.get_y() + bar.get_height()/2.,
                f'${width/1e6:.1f}M', ha='left', va='center')
    
    # Top stores by revenue
    store_revenue = sales_df.groupby(['StoreKey', 'Country_y']).agg({
        'Revenue': 'sum'
    }).reset_index().sort_values('Revenue', ascending=True).tail(10)
    
    store_labels = [f"Store {row['StoreKey']} ({row['Country_y']})" 
                   for _, row in store_revenue.iterrows()]
    
    bars2 = ax2.barh(range(len(store_revenue)), store_revenue['Revenue'], color='orange')
    ax2.set_title('Top 10 Stores by Revenue', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Revenue (USD)')
    ax2.set_ylabel('Store')
    ax2.set_yticks(range(len(store_revenue)))
    ax2.set_yticklabels(store_labels)
    
    plt.tight_layout()
    return fig

def create_brand_performance_chart(sales_df, top_n=10):
    """
    Create charts showing brand performance analysis
    """
    brand_data = sales_df.groupby('Brand').agg({
        'Revenue': 'sum',
        'Profit': 'sum'
    }).reset_index()
    brand_data['Profit Margin'] = (brand_data['Profit'] / brand_data['Revenue']) * 100
    brand_data = brand_data.sort_values('Revenue', ascending=False).head(top_n)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Revenue by brand
    bars1 = ax1.bar(range(len(brand_data)), brand_data['Revenue'], color='steelblue')
    ax1.set_title(f'Top {top_n} Brands by Revenue', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Brand')
    ax1.set_ylabel('Revenue (USD)')
    ax1.set_xticks(range(len(brand_data)))
    ax1.set_xticklabels(brand_data['Brand'], rotation=45, ha='right')
    
    # Profit margin by brand
    bars2 = ax2.bar(range(len(brand_data)), brand_data['Profit Margin'], color='darkgreen')
    ax2.set_title(f'Profit Margin by Top {top_n} Brands', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Brand')
    ax2.set_ylabel('Profit Margin (%)')
    ax2.set_xticks(range(len(brand_data)))
    ax2.set_xticklabels(brand_data['Brand'], rotation=45, ha='right')
    
    # Add value labels
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom')
    
    plt.tight_layout()
    return fig

def create_profitability_analysis_chart(sales_df):
    """
    Create charts showing profitability analysis
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Profit margin by category
    category_data = sales_df.groupby('Category').agg({
        'Revenue': 'sum',
        'Profit': 'sum'
    })
    category_data['Profit Margin'] = (category_data['Profit'] / category_data['Revenue']) * 100
    category_data = category_data.sort_values('Profit Margin', ascending=True)
    
    bars1 = ax1.barh(range(len(category_data)), category_data['Profit Margin'], color='gold')
    ax1.set_title('Profit Margin by Category', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Profit Margin (%)')
    ax1.set_ylabel('Category')
    ax1.set_yticks(range(len(category_data)))
    ax1.set_yticklabels(category_data.index)
    
    # Revenue vs Profit scatter
    ax2.scatter(sales_df['Revenue'], sales_df['Profit'], alpha=0.5, color='purple')
    ax2.set_title('Revenue vs Profit Correlation', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Revenue (USD)')
    ax2.set_ylabel('Profit (USD)')
    ax2.grid(True, alpha=0.3)
    
    # Monthly profit margin trend
    monthly_data = sales_df.groupby(sales_df['Order Date'].dt.to_period('M')).agg({
        'Revenue': 'sum',
        'Profit': 'sum'
    })
    monthly_data['Profit Margin'] = (monthly_data['Profit'] / monthly_data['Revenue']) * 100
    monthly_data.index = monthly_data.index.to_timestamp()
    
    ax3.plot(monthly_data.index, monthly_data['Profit Margin'], marker='o', linewidth=2, color='red')
    ax3.set_title('Monthly Profit Margin Trend', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Profit Margin (%)')
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(True, alpha=0.3)
    
    # Profit distribution histogram
    ax4.hist(sales_df['Profit'], bins=50, color='lightcoral', alpha=0.7, edgecolor='black')
    ax4.set_title('Profit Distribution', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Profit (USD)')
    ax4.set_ylabel('Frequency')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def create_revenue_distribution_chart(sales_df, save_path=None):
    """
    Create charts showing revenue distribution analysis
    """
    # Calculate order-level revenue
    order_revenue = sales_df.groupby('Order Number')['Revenue'].sum()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Revenue distribution histogram
    ax1.hist(order_revenue, bins=50, color='skyblue', alpha=0.7, edgecolor='black')
    ax1.set_title('Order Value Distribution', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Order Value (USD)')
    ax1.set_ylabel('Frequency')
    ax1.grid(True, alpha=0.3)
    
    # Revenue by quantity
    quantity_revenue = sales_df.groupby('Quantity')['Revenue'].sum().head(20)
    bars2 = ax2.bar(quantity_revenue.index, quantity_revenue.values, color='lightgreen')
    ax2.set_title('Revenue by Quantity (Top 20)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Quantity')
    ax2.set_ylabel('Total Revenue (USD)')
    
    # Cumulative revenue contribution
    category_revenue = sales_df.groupby('Category')['Revenue'].sum().sort_values(ascending=False)
    cumulative_pct = (category_revenue.cumsum() / category_revenue.sum()) * 100
    
    ax3.bar(range(len(category_revenue)), category_revenue.values, color='orange', alpha=0.7)
    ax3_twin = ax3.twinx()
    ax3_twin.plot(range(len(cumulative_pct)), cumulative_pct.values, 
                  color='red', marker='o', linewidth=2)
    ax3.set_title('Revenue Pareto Analysis by Category', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Category')
    ax3.set_ylabel('Revenue (USD)', color='orange')
    ax3_twin.set_ylabel('Cumulative %', color='red')
    ax3.set_xticks(range(len(category_revenue)))
    ax3.set_xticklabels(category_revenue.index, rotation=45, ha='right')
    
    # Box plot of revenue by category
    categories = sales_df['Category'].unique()
    revenue_by_category = [sales_df[sales_df['Category'] == cat]['Revenue'].values 
                          for cat in categories]
    
    ax4.boxplot(revenue_by_category, labels=categories)
    ax4.set_title('Revenue Distribution by Category', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Category')
    ax4.set_ylabel('Revenue (USD)')
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved to {save_path}")
    
    return fig

def create_sales_dashboard(sales_df, save_path=None):
    """
    Create a comprehensive sales dashboard with multiple visualizations
    """
    fig = plt.figure(figsize=(20, 16))
    
    # 1. Revenue by Category (Top left)
    ax1 = plt.subplot(3, 3, 1)
    category_revenue = sales_df.groupby('Category')['Revenue'].sum().sort_values(ascending=False)
    bars1 = ax1.bar(range(len(category_revenue)), category_revenue.values, color='skyblue')
    ax1.set_title('Revenue by Category', fontweight='bold')
    ax1.set_xticks(range(len(category_revenue)))
    ax1.set_xticklabels(category_revenue.index, rotation=45, ha='right')
    
    # 2. Monthly Sales Trend (Top center)
    ax2 = plt.subplot(3, 3, 2)
    monthly_sales = sales_df.groupby(sales_df['Order Date'].dt.to_period('M'))['Revenue'].sum()
    monthly_sales.index = monthly_sales.index.to_timestamp()
    ax2.plot(monthly_sales.index, monthly_sales.values, marker='o', linewidth=2, color='green')
    ax2.set_title('Monthly Revenue Trend', fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Top 10 Products (Top right)
    ax3 = plt.subplot(3, 3, 3)
    top_products = sales_df.groupby('Product Name')['Revenue'].sum().sort_values(ascending=True).tail(10)
    ax3.barh(range(len(top_products)), top_products.values, color='coral')
    ax3.set_title('Top 10 Products', fontweight='bold')
    ax3.set_yticks(range(len(top_products)))
    ax3.set_yticklabels([name[:20] + '...' if len(name) > 20 else name 
                        for name in top_products.index])
    
    # 4. Customer Demographics (Middle left)
    ax4 = plt.subplot(3, 3, 4)
    gender_revenue = sales_df.groupby('Gender')['Revenue'].sum()
    ax4.pie(gender_revenue.values, labels=gender_revenue.index, autopct='%1.1f%%', 
            colors=['lightblue', 'pink'])
    ax4.set_title('Revenue by Gender', fontweight='bold')
    
    # 5. Geographic Distribution (Middle center)
    ax5 = plt.subplot(3, 3, 5)
    country_revenue = sales_df.groupby('Country_y')['Revenue'].sum().sort_values(ascending=True)
    ax5.barh(range(len(country_revenue)), country_revenue.values, color='lightgreen')
    ax5.set_title('Revenue by Country', fontweight='bold')
    ax5.set_yticks(range(len(country_revenue)))
    ax5.set_yticklabels(country_revenue.index)
    
    # 6. Day of Week Analysis (Middle right)
    ax6 = plt.subplot(3, 3, 6)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_sales = sales_df.groupby('Day of Week')['Revenue'].sum().reindex(day_order)
    ax6.bar(range(len(daily_sales)), daily_sales.values, color='gold')
    ax6.set_title('Sales by Day of Week', fontweight='bold')
    ax6.set_xticks(range(len(daily_sales)))
    ax6.set_xticklabels([day[:3] for day in daily_sales.index])
    
    # 7. Top Brands (Bottom left)
    ax7 = plt.subplot(3, 3, 7)
    top_brands = sales_df.groupby('Brand')['Revenue'].sum().sort_values(ascending=True).tail(8)
    ax7.barh(range(len(top_brands)), top_brands.values, color='mediumpurple')
    ax7.set_title('Top 8 Brands', fontweight='bold')
    ax7.set_yticks(range(len(top_brands)))
    ax7.set_yticklabels(top_brands.index)
    
    # 8. Quarterly Performance (Bottom center)
    ax8 = plt.subplot(3, 3, 8)
    quarterly_sales = sales_df.groupby(['Year', 'Quarter'])['Revenue'].sum()
    quarters = [f"{year} Q{q}" for year, q in quarterly_sales.index]
    ax8.plot(range(len(quarterly_sales)), quarterly_sales.values, marker='s', linewidth=2, color='red')
    ax8.set_title('Quarterly Sales', fontweight='bold')
    ax8.set_xticks(range(0, len(quarterly_sales), 2))
    ax8.set_xticklabels([quarters[i] for i in range(0, len(quarters), 2)], rotation=45)
    
    # 9. Profit Margin by Category (Bottom right)
    ax9 = plt.subplot(3, 3, 9)
    category_data = sales_df.groupby('Category').agg({'Revenue': 'sum', 'Profit': 'sum'})
    category_data['Profit Margin'] = (category_data['Profit'] / category_data['Revenue']) * 100
    ax9.bar(range(len(category_data)), category_data['Profit Margin'], color='darkgreen')
    ax9.set_title('Profit Margin by Category', fontweight='bold')
    ax9.set_xticks(range(len(category_data)))
    ax9.set_xticklabels(category_data.index, rotation=45, ha='right')
    ax9.set_ylabel('Profit Margin (%)')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Dashboard saved to {save_path}")
    
    return fig

def create_interactive_plotly_dashboard(sales_df):
    """
    Create an interactive dashboard using Plotly
    """
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Revenue by Category', 'Monthly Trends', 
                       'Geographic Distribution', 'Top Products'),
        specs=[[{"type": "bar"}, {"type": "scatter"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Revenue by Category
    category_revenue = sales_df.groupby('Category')['Revenue'].sum().sort_values(ascending=False)
    fig.add_trace(
        go.Bar(x=category_revenue.index, y=category_revenue.values, name="Category Revenue"),
        row=1, col=1
    )
    
    # Monthly Trends
    monthly_sales = sales_df.groupby(sales_df['Order Date'].dt.to_period('M'))['Revenue'].sum()
    monthly_sales.index = monthly_sales.index.to_timestamp()
    fig.add_trace(
        go.Scatter(x=monthly_sales.index, y=monthly_sales.values, mode='lines+markers', name="Monthly Revenue"),
        row=1, col=2
    )
    
    # Geographic Distribution
    country_revenue = sales_df.groupby('Country_y')['Revenue'].sum().sort_values(ascending=False)
    fig.add_trace(
        go.Bar(x=country_revenue.index, y=country_revenue.values, name="Country Revenue"),
        row=2, col=1
    )
    
    # Top Products
    top_products = sales_df.groupby('Product Name')['Revenue'].sum().sort_values(ascending=False).head(10)
    fig.add_trace(
        go.Bar(x=top_products.values, y=top_products.index, orientation='h', name="Top Products"),
        row=2, col=2
    )
    
    fig.update_layout(height=800, showlegend=False, title_text="Sales Analysis Dashboard")
    
    return fig

if __name__ == "__main__":
    print("Visualization Module for Sales Analysis")
    print("=====================================")
    print("This module contains functions for creating visualizations.")
    print("Import this module in your notebooks to use the visualization functions.")
