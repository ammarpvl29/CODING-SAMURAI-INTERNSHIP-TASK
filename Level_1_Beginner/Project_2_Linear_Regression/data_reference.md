# Data Structure Reference - Global Electronics Retailer Dataset

## Column Mapping for sales_analysis_complete.csv

### Important: Duplicate Columns from Merging
- **Country_x**: Customer country (from customers table)
- **Country_y**: Store country (from stores table)  
- **State_x**: Customer state (from customers table)
- **State_y**: Store state (from stores table)

### For Store-Level Analysis Use:
- `Country_y` - Store country
- `State_y` - Store state
- `Square Meters` - Store size

### For Customer-Level Analysis Use:
- `Country_x` - Customer country
- `State_x` - Customer state
- `Gender` - Customer gender
- `Customer Age` - Customer age

### Key Columns for Linear Regression:
- **Target Variable**: `Revenue` (float64)
- **Numeric Features**: 
  - `Quantity`, `Unit Price USD`, `Square Meters`
  - `Year`, `Month`, `Quarter`, `Week of Year`
  - `Customer Age`, `Delivery Days`
- **Categorical Features**: 
  - `Category`, `Brand`, `Country_y`, `State_y`
  - `Gender`, `Age Group`, `Day of Week`

### Data Types Summary:
- **Total Records**: 62,884 rows, 44 columns
- **Memory Usage**: ~101 MB
- **Missing Values**: 
  - `Delivery Date`: 49,719 (79.1% missing)
  - `Delivery Days`: 49,719 (79.1% missing)
  - `State Code`: 30 (minimal)

### Feature Engineering Opportunities:
1. **Temporal Features**: Already created (Year, Month, Quarter, etc.)
2. **Lag Features**: Previous day/week sales
3. **Categorical Encoding**: Country, State, Category, Brand
4. **Customer Segmentation**: Age groups already created
5. **Store Performance**: Size-based categories
