import sys
from pathlib import Path
from fastapi.testclient import TestClient
import uuid

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from app.main import app

# NOTE: We are NOT mocking anything here. 
# This test hits the REAL Database and REAL Gemini API configured in .env

client = TestClient(app)

def test_full_flow():
    print("1. Testing Health Check...")
    response = client.get("/health")
    assert response.status_code == 200
    print("   [OK] Health Check passed")

    # Generate unique user to avoid DB conflicts
    unique_id = str(uuid.uuid4())[:8]
    username = f"test_user_{unique_id}"
    password = "testpassword123"

    print(f"\n2. Testing Registration for {username}...")
    reg_response = client.post("/auth/register", json={
        "username": username,
        "password": password
    })
    if reg_response.status_code != 200:
        print(f"FAILED: {reg_response.text}")
    assert reg_response.status_code == 200
    print("   [OK] Registration passed")

    print("\n3. Testing Login...")
    login_response = client.post("/auth/token", data={
        "username": username,
        "password": password
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("   [OK] Login passed, token received")

    # Sample Data
    employee_data = {
        "Age": 30,
        "BusinessTravel": "Travel_Rarely",
        "DailyRate": 800,
        "Department": "Sales",
        "DistanceFromHome": 2,
        "Education": 2,
        "EducationField": "Life Sciences",
        "EnvironmentSatisfaction": 3,
        "Gender": "Male",
        "HourlyRate": 70,
        "JobInvolvement": 3,
        "JobLevel": 2,
        "JobRole": "Sales Executive",
        "JobSatisfaction": 3,
        "MaritalStatus": "Single",
        "MonthlyIncome": 5000,
        "MonthlyRate": 15000,
        "NumCompaniesWorked": 1,
        "OverTime": "No",
        "PercentSalaryHike": 12,
        "PerformanceRating": 3,
        "RelationshipSatisfaction": 3,
        "StockOptionLevel": 0,
        "TotalWorkingYears": 8,
        "TrainingTimesLastYear": 2,
        "WorkLifeBalance": 3,
        "YearsAtCompany": 6,
        "YearsInCurrentRole": 2,
        "YearsSinceLastPromotion": 0,
        "YearsWithCurrManager": 2
    }

    print("\n4. Testing Prediction Endpoint (Real DB Write)...")
    predict_response = client.post("/predict", json=employee_data, headers=headers)
    if predict_response.status_code != 200:
        print(f"FAILED: {predict_response.text}")
    assert predict_response.status_code == 200
    print("   [OK] Prediction passed")
    print(f"   Result: {predict_response.json()}")

    print("\n5. Testing Generative AI Plan (Real Gemini Call)...")
    plan_response = client.post("/generate-retention-plan", json=employee_data, headers=headers)
    if plan_response.status_code != 200:
        print(f"FAILED: {plan_response.text}")
    assert plan_response.status_code == 200
    print("   [OK] GenAI Plan passed")
    # Verify we got a string plan back
    assert "retention_plan" in plan_response.json()
    print("   [OK] Retention Plan generated")

if __name__ == "__main__":
    try:
        test_full_flow()
        print("\nSUCCESS: All endpoints verified against LIVE system!")
    except Exception as e:
        print(f"\nERROR: Test failed with {e}")
        sys.exit(1)
