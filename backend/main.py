from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import sys
from pathlib import Path
from datetime import timedelta
from sqlalchemy.orm import Session

# Add ml folder to path to import src
sys.path.append(str(Path(__file__).parent.parent / "ml"))

from src.predict import get_predictor
from .auth import create_access_token, get_password_hash, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from .database import engine, get_db, Base
from .models import User as UserModel, PredictionLog

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RetentionAI API",
    description="API for predicting employee churn",
    version="1.0.0"
)

# CORS (Allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Security & Auth ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserSchema(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Validate token and get user from DB."""
    username = token # In real JWT, we decode this. Ideally we decode 'sub'.
    # Simplified: We trust token is username for now (Wait, auth.py encodes username in 'sub')
    # Let's verify properly:
    from jose import jwt, JWTError
    from .auth import SECRET_KEY, ALGORITHM
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.post("/register")
def register(user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = UserModel(
        username=user.username,
        hashed_password=get_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "id": new_user.id}

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Input Schema ---
class EmployeeData(BaseModel):
    Age: int
    BusinessTravel: str
    DailyRate: int
    Department: str
    DistanceFromHome: int
    Education: int
    EducationField: str
    EnvironmentSatisfaction: int
    Gender: str
    HourlyRate: int
    JobInvolvement: int
    JobLevel: int
    JobRole: str
    JobSatisfaction: int
    MaritalStatus: str
    MonthlyIncome: int
    MonthlyRate: int
    NumCompaniesWorked: int
    OverTime: str
    PercentSalaryHike: int
    PerformanceRating: int
    RelationshipSatisfaction: int
    StockOptionLevel: int
    TotalWorkingYears: int
    TrainingTimesLastYear: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsSinceLastPromotion: int
    YearsWithCurrManager: int

@app.get("/")
def read_root():
    return {"status": "online", "message": "RetentionAI API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict")
def predict_churn(
    employee: EmployeeData, 
    current_user: UserModel = Depends(get_current_user),
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

from .genai import get_agent

@app.post("/generate-retention-plan")
def generate_retention_plan(
    employee: EmployeeData,
    current_user: UserModel = Depends(get_current_user)
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
