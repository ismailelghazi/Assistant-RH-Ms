import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from backend.main import app

client = TestClient(app)

def test_auth_flow():
    print("\n--- 1. Register User ---")
    user_data = {"username": "hr_manager", "password": "securepassword123"}
    resp = client.post("/register", json=user_data)
    print(resp.json())
    assert resp.status_code == 200

    print("\n--- 2. Login (Get Token) ---")
    login_data = {"username": "hr_manager", "password": "securepassword123"}
    resp = client.post("/token", data=login_data)
    token_data = resp.json()
    print(f"Token: {token_data.get('access_token')[:20]}...")
    assert resp.status_code == 200
    token = token_data["access_token"]

    print("\n--- 3. Access Protected Route (/predict) ---")
    employee_data = {
        "Age": 30, "BusinessTravel": "Travel_Rarely", "DailyRate": 800, "Department": "Sales",
        "DistanceFromHome": 2, "Education": 2, "EducationField": "Life Sciences",
        "EnvironmentSatisfaction": 3, "Gender": "Male", "HourlyRate": 70,
        "JobInvolvement": 3, "JobLevel": 2, "JobRole": "Sales Executive",
        "JobSatisfaction": 3, "MaritalStatus": "Single", "MonthlyIncome": 5000,
        "MonthlyRate": 15000, "NumCompaniesWorked": 1, "OverTime": "No",
        "PercentSalaryHike": 12, "PerformanceRating": 3, "RelationshipSatisfaction": 3,
        "StockOptionLevel": 0, "TotalWorkingYears": 8, "TrainingTimesLastYear": 2,
        "WorkLifeBalance": 3, "YearsAtCompany": 6, "YearsInCurrentRole": 2,
        "YearsSinceLastPromotion": 0, "YearsWithCurrManager": 2
    }
    
    # Try WITHOUT token (Should Fail)
    print("  > Trying without token...")
    resp = client.post("/predict", json=employee_data)
    print(f"  > Status: {resp.status_code}")
    assert resp.status_code == 401

    # Try WITH token (Should Succeed)
    print("  > Trying with token...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.post("/predict", json=employee_data, headers=headers)
    print(f"  > Status: {resp.status_code}")
    print(f"  > Result: {resp.json()}")
    assert resp.status_code == 200

if __name__ == "__main__":
    test_auth_flow()
