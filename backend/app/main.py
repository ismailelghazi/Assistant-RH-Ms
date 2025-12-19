from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, prediction

# Create Tables (for development, better to use Alembic in prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RetentionAI API",
    description="API for predicting employee churn",
    version="1.0.0"
)

# CORS middleware - must specify exact origin when using credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "https://hybrid-analyzer.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(prediction.router)

@app.get("/")
def read_root():
    return {"status": "online", "message": "RetentionAI API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
