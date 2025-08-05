# Sales Data Analysis Project

**Project:** Global Electronics Retailer Dataset Analysis  
**Author:** Ammar Siregar  
**Internship:** Coding Samurai  
**Level:** 1 - Beginner  

## Project Overview

This project analyzes sales data from a global electronics retailer to uncover business insights, trends, and performance metrics. The analysis includes customer behavior, product performance, geographic distribution, and temporal patterns.

## Dataset Description

The project uses six main datasets:

- **Sales.csv** (62,884 records): Core transaction data with order details
- **Customers.csv** (15,266 records): Customer demographic information
- **Products.csv** (2,517 records): Product catalog with pricing information
- **Stores.csv** (67 records): Store location and details
- **Exchange_Rates.csv** (11,215 records): Currency conversion rates
- **Data_Dictionary.csv** (37 records): Field descriptions and metadata

## Project Structure

```
Project_1_Sales_Data_Analysis/
│
├── data/
│   ├── raw/                          # Original data files
│   │   ├── Customers.csv
│   │   ├── Products.csv
│   │   ├── Sales.csv
│   │   ├── Stores.csv
│   │   ├── Exchange_Rates.csv
│   │   └── Data_Dictionary.csv
│   └── processed/                    # Cleaned and processed data
│       ├── customers_cleaned.csv
│       ├── products_cleaned.csv
│       ├── sales_cleaned.csv
│       ├── stores_cleaned.csv
│       ├── exchange_rates_cleaned.csv
│       ├── sales_analysis_complete.csv
│       ├── analysis_summary.csv
│       ├── category_performance.csv
│       ├── top_products.csv
│       ├── top_customers.csv
│       ├── store_performance.csv
│       ├── data_cleaning_summary.csv
│       └── business_insights.txt
│
├── notebooks/
│   ├── 01_data_exploration.ipynb     # Initial data exploration
│   ├── 02_data_cleaning.ipynb        # Data cleaning and preparation
│   └── 03_analysis_visualization.ipynb # Analysis and visualizations
│
├── scripts/
│   ├── data_cleaning.py              # Data cleaning functions
│   └── visualization.py              # Visualization functions
│
├── visualizations/
│   ├── sales_by_category.png         # Revenue by product category
│   ├── monthly_trends.png            # Monthly sales trends
│   ├── revenue_distribution.png      # Revenue distribution analysis
│   ├── top_products.png              # Top performing products
│   ├── sales_dashboard.png           # Comprehensive dashboard
│   └── [other generated charts]
│
├── sales_analysis.py                 # Original monolithic script (deprecated)
└── README.md                         # Project documentation
```

## Key Features

### 📊 Data Analysis Capabilities
- **Revenue Analysis**: Total revenue, profit margins, and growth trends
- **Product Performance**: Top products, category analysis, brand performance
- **Customer Insights**: Demographics, purchasing behavior, top customers
- **Geographic Analysis**: Performance by country and store locations
- **Temporal Patterns**: Seasonal trends, monthly/quarterly performance

### 🧹 Data Processing
- **Data Cleaning**: Handle missing values, format inconsistencies
- **Data Integration**: Merge multiple datasets for comprehensive analysis
- **Feature Engineering**: Create calculated fields (profit, margins, age groups)
- **Data Validation**: Ensure data quality and consistency

### 📈 Visualizations
- **Category Performance**: Bar charts and pie charts
- **Time Series**: Monthly and quarterly trends
- **Geographic Maps**: Revenue distribution by location
- **Customer Demographics**: Age and gender analysis
- **Profitability Analysis**: Margin analysis across dimensions

## Getting Started

### Prerequisites

```bash
pip install pandas numpy matplotlib seaborn plotly jupyter
```

### Usage

1. **Data Exploration**: Start with `01_data_exploration.ipynb`
   - Load and examine raw data
   - Understand data structure and quality
   - Identify data issues and patterns

2. **Data Cleaning**: Run `02_data_cleaning.ipynb`
   - Clean and preprocess all datasets
   - Handle missing values and format issues
   - Create integrated analysis dataset

3. **Analysis & Visualization**: Execute `03_analysis_visualization.ipynb`
   - Perform comprehensive business analysis
   - Generate insights and recommendations
   - Create visualizations and dashboard

### Alternative Usage

You can also use the modular scripts:

```python
# Import cleaning functions
from scripts.data_cleaning import *

# Import visualization functions
from scripts.visualization import *

# Load and clean data
customers = load_customers_data('data/raw/Customers.csv')
products = load_products_data('data/raw/Products.csv')

# Create visualizations
create_category_revenue_chart(sales_df, save_path='visualizations/categories.png')
```

## Technologies Used

- **Python**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib/Seaborn**: Static visualizations
- **Plotly**: Interactive visualizations
- **Jupyter Notebooks**: Interactive development environment

## Author

**Ammar Siregar**  
Coding Samurai Internship Program  
Level 1 - Beginner Project

---

*This project demonstrates comprehensive data analysis skills including data cleaning, exploratory analysis, statistical analysis, and business intelligence reporting.*
[www.linkedin.com/in/ammar-pavel-zamora-siregar-788109187] | [ammarpvl@student.telkomuniversity.ac.id]

---

*Project completed as part of Coding Samurai Internship Program*