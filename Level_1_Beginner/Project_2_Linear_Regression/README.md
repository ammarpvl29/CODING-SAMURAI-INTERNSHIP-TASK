# Project 2: Linear Regression on Sales Dataset

## 📊 Predicting Sales Revenue based on Various Features
**Global Electronics Retailer Dataset Analysis**

---

## 🎯 Project Overview

This project demonstrates the implementation of linear regression models to predict daily sales revenue using the Global Electronics Retailer dataset. We explore both multiple linear regression and simple linear regression approaches, providing comprehensive analysis and actionable business insights.

### 🏆 Key Achievements
- Built multiple linear regression model with **72.37% R² score** (Good performance)
- Achieved **27.8% improvement** over simple regression baseline
- Engineered temporal and lag features for enhanced prediction accuracy  
- Created comprehensive visualizations for model interpretation
- Generated actionable business recommendations based on model insights
- Implemented proper model evaluation and comparison techniques

---

## 📁 Project Structure

```
Project_2_Linear_Regression/
├── notebooks/
│   └── linear_regression_analysis.ipynb    # Main analysis notebook
├── data/
│   ├── raw/                                # Original dataset files
│   │   ├── Customers.csv
│   │   ├── Products.csv
│   │   ├── Sales.csv
│   │   ├── Stores.csv
│   │   ├── Exchange_Rates.csv
│   │   └── Data_Dictionary.csv
│   └── processed/                          # Cleaned and processed data
│       └── sales_analysis_complete.csv
├── models/                                 # Saved models and results
│   ├── linear_regression_model.pkl
│   ├── simple_linear_regression_model.pkl
│   ├── scaler.pkl
│   ├── label_encoder_*.pkl
│   ├── model_metrics.csv
│   └── test_predictions.csv
├── explore_data_structure.py               # Data exploration script
├── data_reference.md                       # Data structure reference
└── README.md                              # This file
```

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn scikit-learn joblib
```

### Running the Analysis
1. **Clone the repository** and navigate to the project directory
2. **Ensure data files** are in the correct `data/` directories
3. **Open and run** `notebooks/linear_regression_analysis.ipynb`
4. **Execute cells sequentially** for complete analysis

### Quick Data Exploration
```bash
python explore_data_structure.py
```

---

## 📈 Methodology

### 1. **Data Preparation**
- **Dataset**: 62,884 sales transactions aggregated to 18,081 daily observations
- **Time Period**: January 2, 2016 to February 20, 2021 (5+ years)
- **Scope**: 58 stores across 9 countries
- **Aggregation**: Daily store-level revenue prediction
- **Revenue Range**: $1.99 to $64,522.04 per day
- **Average Daily Revenue**: $3,074.96

### 2. **Feature Engineering**
- **Temporal Features**: Year, month, day of week, weekend indicators
- **Lag Features**: Previous day's revenue and quantity
- **Aggregated Metrics**: Daily customer count, order count, product diversity
- **Store Characteristics**: Store size, location, country encoding
- **Categorical Encoding**: Product categories, store countries

### 3. **Model Development**
- **Multiple Linear Regression**: 13 features predicting daily revenue
- **Simple Linear Regression**: Quantity-only baseline model
- **Feature Scaling**: StandardScaler for optimal performance
- **Train/Test Split**: 80/20 split with random seed for reproducibility

### 4. **Evaluation Metrics**
- **R² Score**: Variance explained by the model
- **RMSE**: Root Mean Square Error for prediction accuracy
- **MAE**: Mean Absolute Error for average deviation
- **Residual Analysis**: Model assumption validation

---

## 📊 Key Results

### Model Performance
| Model | Features | R² Score | RMSE | MAE | Improvement |
|-------|----------|----------|------|-----|-------------|
| **Multiple Linear Regression** | 13 features | **0.7237** | $2,173.48 | $1,176.87 | **27.8% better** |
| **Simple Linear Regression** | 1 feature | 0.5662 | ~$2,800 | ~$2,100 | Baseline |

### Top Influential Features
1. **Number of Orders** - Negative impact (efficiency indicator)
2. **Number of Customers** - Positive impact (customer diversity)
3. **Quantity Sold** - Strong positive correlation (r = 0.750)
4. **Average Price** - Product mix influence
5. **Number of Products** - Negative impact (complexity factor)

### Business Insights
- **72.37% of daily revenue variance** is predictable using the model
- **Quantity sold** has the strongest single correlation with revenue (r = 0.750)
- **Customer count vs order count** shows interesting dynamics (opposite effects)
- **Model generalization** is good (minimal overfitting: 0.0153 difference)
- **Weekend patterns** and **temporal effects** are detectable
- **Some multicollinearity** detected between features

---

## 📈 Visualizations

The notebook includes comprehensive visualizations:

1. **Correlation Heatmap** - Feature relationships analysis
2. **Actual vs Predicted** - Model accuracy assessment  
3. **Residual Plots** - Model assumption validation
4. **Feature Importance** - Coefficient magnitude analysis
5. **Learning Curves** - Training efficiency evaluation
6. **Error Distribution** - Prediction accuracy patterns

---

## 💼 Business Recommendations

### Immediate Actions
1. **Optimize Order Efficiency** - Negative correlation suggests order consolidation opportunities
2. **Focus on Customer Acquisition** - Strong positive impact on revenue
3. **Leverage Quantity-Revenue Relationship** - Strongest single predictor (r = 0.750)
4. **Implement Weekend Strategies** - Distinct weekend patterns detected

### Strategic Initiatives
1. **Revenue Forecasting System** using the trained model (72% accuracy)
2. **Customer Acquisition Programs** - High impact on daily revenue
3. **Order Consolidation Analysis** - Understand negative order count impact
4. **Product Mix Optimization** - Leverage average price influence

### Performance Targets
- **Current RMSE**: $2,173 per day
- **Target RMSE**: $1,739 per day (20% improvement)
- **Focus Areas**: Customer acquisition, order efficiency, quantity optimization

---

## 🔧 Technical Implementation

### Model Architecture
```python
# Multiple Linear Regression
LinearRegression(
    features=13,
    scaling=StandardScaler(),
    encoding=LabelEncoder()
)

# Feature Set
numeric_features = [
    'Quantity', 'num_orders', 'num_customers', 'num_products',
    'avg_price', 'Square Meters', 'month', 'day_of_week',
    'is_weekend', 'prev_day_revenue', 'prev_day_quantity'
]
categorical_features = ['dominant_category', 'Country']
```

### Model Equation (Standardized)
```
Revenue = Intercept + 
          β₁ × prev_day_revenue +
          β₂ × num_customers +
          β₃ × Square_Meters +
          ... + βₙ × country_encoded
```

---

## 📚 Files Description

### Core Notebooks
- **`linear_regression_analysis.ipynb`**: Complete analysis pipeline with step-by-step implementation

### Data Files
- **`sales_analysis_complete.csv`**: Pre-processed dataset with all merged features
- **Raw CSV files**: Original data sources from Global Electronics Retailer

### Model Artifacts
- **`linear_regression_model.pkl`**: Trained multiple regression model
- **`simple_linear_regression_model.pkl`**: Baseline single-feature model
- **`scaler.pkl`**: Feature scaling transformer
- **`label_encoder_*.pkl`**: Categorical variable encoders

### Results
- **`model_metrics.csv`**: Comprehensive model comparison metrics
- **`test_predictions.csv`**: Detailed prediction results with errors

---

## 🔮 Future Enhancements

### Model Improvements
1. **Regularization**: Ridge/Lasso regression for overfitting prevention
2. **Polynomial Features**: Non-linear relationship capture
3. **Ensemble Methods**: Random Forest, XGBoost implementations
4. **Time Series Models**: ARIMA/Prophet for temporal patterns

### Feature Engineering
1. **Interaction Terms**: Feature combination effects
2. **External Data**: Weather, holidays, economic indicators
3. **Rolling Statistics**: Moving averages, trends
4. **Seasonality Decomposition**: Advanced temporal features

### Deployment
1. **Real-time Prediction API**: Flask/FastAPI implementation
2. **Dashboard**: Interactive visualization with Streamlit/Dash
3. **Automated Retraining**: MLOps pipeline setup
4. **A/B Testing Framework**: Model performance monitoring

---

## 👨‍💻 Author

**Ammar Siregar**  
Coding Samurai Internship Program  
Level 1 - Project 2  

---

## 📄 License

This project is part of the Coding Samurai Internship program and is intended for educational purposes.

---

## 🤝 Contributing

This is an educational project. For suggestions or improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

*Last updated: August 2025*
