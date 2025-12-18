from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="hr_manager")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    logs = relationship("PredictionLog", back_populates="user")
