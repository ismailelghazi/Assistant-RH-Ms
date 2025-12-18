# RetentionAI - ML Module

Machine Learning pipeline for Employee Churn Prediction.

## Project Structure

```
ml/
├── data/                   # Dataset folder
│   └── HR_Employee_Attrition.csv
├── models/                 # Saved models
│   ├── best_model.pkl
│   └── preprocessor.pkl
├── notebooks/              # Jupyter notebooks (RUN THESE)
│   ├── 01_EDA.ipynb        # Data exploration
│   └── 02_Model_Training.ipynb  # Model training
├── reports/                # Generated plots
├── src/                    # Python modules
│   ├── config.py           # Settings
│   ├── data_loader.py      # Data loading
│   ├── eda.py              # EDA functions
│   ├── preprocessing.py    # Preprocessing
│   ├── model_training.py   # Model training
│   └── predict.py          # Prediction utilities
├── requirements.txt
└── README.md
```

## Quick Start

### 1. Install Requirements

```bash
cd ml
pip install -r requirements.txt
```

### 2. Generate Sample Data (if needed)

```python
from src.data_loader import generate_sample_data
generate_sample_data(1000)
```

### 3. Run Notebooks

Open Jupyter and run notebooks in order:

```bash
jupyter notebook notebooks/
```

1. Run `01_EDA.ipynb` - Explore the data
2. Run `02_Model_Training.ipynb` - Train models

## What Each Notebook Does

### 01_EDA.ipynb
- Loads and views data
- Cleans unnecessary columns
- Analyzes target variable (Attrition)
- Creates visualizations
- Finds correlations

### 02_Model_Training.ipynb
- Preprocesses data (encoding, scaling)
- Trains Logistic Regression
- Trains Random Forest
- Evaluates models (accuracy, ROC-AUC, etc.)
- Saves best model

## Making Predictions

After training, use the saved model:

```python
import joblib
import pandas as pd

# Load model and preprocessor
model = joblib.load('models/best_model.pkl')['model']
preprocessor = joblib.load('models/preprocessor.pkl')['preprocessor']

# Employee data
employee = pd.DataFrame([{
    'Age': 35,
    'Department': 'Sales',
    'MonthlyIncome': 5000,
    'OverTime': 'Yes',
    # ... other features
}])

# Predict
X = preprocessor.transform(employee)
probability = model.predict_proba(X)[0, 1]
print(f"Churn probability: {probability:.2%}")
```

## Key Metrics

After training, you should see:
- Accuracy: How many predictions are correct
- Precision: When we predict "Leave", how often is it true
- Recall: Of employees who leave, how many did we catch
- F1 Score: Balance between precision and recall
- ROC-AUC: Overall model quality (higher is better)
