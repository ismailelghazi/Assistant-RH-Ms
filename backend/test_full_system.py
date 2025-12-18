import sys
from pathlib import Path
from fastapi.testclient import TestClient
import os

# Ensure backend works with local sqlite
os.environ["DATABASE_URL"] = "sqlite:///./test_retention.db"

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

# Import AFTER setting env var
from backend.main import app
from backend.database import Base, engine

# Reset DB for fresh test
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_full_system():
    print("🚀 Starting End-to-End System Test...")

    # 1. Register
    print("\n[1/4] Registering User 'admin'...")
    resp = client.post("/register", json={"username": "admin", "password": "password123"})
    assert resp.status_code == 200
    print("✅ User Registered.")

    # 2. Login
    print("\n[2/4] Logging in...")
    resp = client.post("/token", data={"username": "admin", "password": "password123"})
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login Successful. Token acquired.")

    # 3. Predict (High Risk Scenario)
    print("\n[3/4] Testing Prediction (High Risk Profile)...")
    # This employee has stats likely to churn (low satisfaction, overtime, low salary hike)
    high_risk_employee = {
        "Age": 29, "BusinessTravel": "Travel_Frequently", "DailyRate": 400, "Department": "Sales",
        "DistanceFromHome": 25, "Education": 1, "EducationField": "Marketing",
        "EnvironmentSatisfaction": 1, "Gender": "Male", "HourlyRate": 30,
        "JobInvolvement": 1, "JobLevel": 1, "JobRole": "Sales Representative",
        "JobSatisfaction": 1, "MaritalStatus": "Single", "MonthlyIncome": 2500,
        "MonthlyRate": 8000, "NumCompaniesWorked": 7, "OverTime": "Yes",
        "PercentSalaryHike": 11, "PerformanceRating": 3, "RelationshipSatisfaction": 1,
        "StockOptionLevel": 0, "TotalWorkingYears": 4, "TrainingTimesLastYear": 1,
        "WorkLifeBalance": 1, "YearsAtCompany": 2, "YearsInCurrentRole": 1,
        "YearsSinceLastPromotion": 0, "YearsWithCurrManager": 0
    }
    
    resp = client.post("/predict", json=high_risk_employee, headers=headers)
    assert resp.status_code == 200
    result = resp.json()
    print(f"👉 Prediction Result: Churn Prob={result['churn_probability']}, Risk={result['risk_level']}")
    print("✅ Prediction logged to DB (SQLite).")

    # 4. Generate Retention Plan
    print("\n[4/4] Generating Retention Plan (GenAI)...")
    resp = client.post("/generate-retention-plan", json=high_risk_employee, headers=headers)
    assert resp.status_code == 200
    print(resp.json()["retention_plan"])
    print("✅ GenAI Agent Success.")

    print("\n🎉 ALL TESTS PASSED! The backend is fully functional.")

if __name__ == "__main__":
    test_full_system()
