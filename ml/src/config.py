"""
Configuration file for the ML pipeline
Contains all settings and column definitions
"""
from pathlib import Path

# =============================================================================
# PROJECT PATHS
# =============================================================================
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# =============================================================================
# MODEL SETTINGS
# =============================================================================
RANDOM_STATE = 42  # For reproducibility
TEST_SIZE = 0.2    # 20% for testing, 80% for training

# =============================================================================
# TARGET COLUMN
# =============================================================================
TARGET_COLUMN = "Attrition"

# =============================================================================
# COLUMNS TO DROP (not useful for prediction)
# =============================================================================
COLUMNS_TO_DROP = [
    "EmployeeNumber",   # Just an ID
    "EmployeeCount",    # Always 1
    "Over18",           # Always Y
    "StandardHours"     # Always 80
]

# =============================================================================
# CATEGORICAL COLUMNS (text data - need encoding)
# =============================================================================
CATEGORICAL_COLUMNS = [
    "BusinessTravel",
    "Department",
    "EducationField",
    "Gender",
    "JobRole",
    "MaritalStatus",
    "OverTime"
]

# =============================================================================
# NUMERICAL COLUMNS (numbers - need scaling)
# =============================================================================
NUMERICAL_COLUMNS = [
    "Age",
    "DailyRate",
    "DistanceFromHome",
    "Education",
    "EnvironmentSatisfaction",
    "HourlyRate",
    "JobInvolvement",
    "JobLevel",
    "JobSatisfaction",
    "MonthlyIncome",
    "MonthlyRate",
    "NumCompaniesWorked",
    "PercentSalaryHike",
    "PerformanceRating",
    "RelationshipSatisfaction",
    "StockOptionLevel",
    "TotalWorkingYears",
    "TrainingTimesLastYear",
    "WorkLifeBalance",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager"
]
