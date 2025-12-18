from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
from pathlib import Path

# Add ml folder to path to import src
# Adjust path assuming backend/app/routers is 2 levels deep from backend
# We need to reach ml folder which is at ../../ml from backend
# backend/app/routers -> backend/app -> backend -> .. -> ml
# Current file is backend/app/routers/prediction.py
# Root is HRPRJOJECT
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "ml"))

from src.predict import get_predictor
from ..database import get_db
from ..models.user import User
from ..models.prediction import PredictionLog
from ..schemas.prediction import EmployeeData
from ..services.genai_service import get_agent
from .auth import get_current_user

router = APIRouter(
    tags=["prediction"]
)

@router.post("/predict")
def predict_churn(
    employee: EmployeeData, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Predict churn and log the request to DB.
    """
    try:
        data = employee.dict()
        predictor = get_predictor()
        result = predictor.predict(data)
        
        # Log to Database
        log_entry = PredictionLog(
            user_id=current_user.id,
            input_data=data,
            churn_probability=result['churn_probability'],
            risk_level=result['risk_level']
        )
        db.add(log_entry)
        db.commit()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-retention-plan")
def generate_retention_plan(
    employee: EmployeeData,
    current_user: User = Depends(get_current_user)
):
    """
    Generate a retention plan using GenAI (if risk is high).
    """
    try:
        # 1. Predict first
        data = employee.dict()
        predictor = get_predictor()
        prediction = predictor.predict(data)
        
        risk_level = prediction['risk_level']
        
        # 2. Generate Plan
        agent = get_agent()
        plan = agent.generate_plan(data, risk_level)
        
        return {
            "risk_level": risk_level,
            "churn_probability": prediction['churn_probability'],
            "retention_plan": plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
