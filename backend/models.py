from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="hr_manager")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    logs = relationship("PredictionLog", back_populates="user")

class PredictionLog(Base):
    __tablename__ = "predictions_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Store the input data as a JSON blob
    input_data = Column(JSON)
    
    # Prediction results
    churn_probability = Column(Float)
    risk_level = Column(String)
    
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="logs")
