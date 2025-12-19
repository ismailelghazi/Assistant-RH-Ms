# HR Retention & Analysis AI System

A full-stack intelligent RH application that predicts employee churn risk and generates personalized retention plans using Generative AI.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![React](https://img.shields.io/badge/frontend-React%20%2B%20Vite-61DAFB.svg)
![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688.svg)

## Features

*   **Predictive Analytics**: Accurately predicts employee turnover probability using an integrated XGBoost Machine Learning model.
*   **AI Retention Plans**: Uses Google Gemini 2.0 Flash to generate actionable, personalized strategies to retain at-risk employees.
*   **Modern UI**: Beautiful, responsive dashboard built with React 18, TailwindCSS, and Framer Motion.
*   **Secure Auth**: Robust JWT-based authentication system with hashed passwords.
*   **Dockerized**: Fully containerized architecture using Docker Compose.

---

## Technical Architecture

### 1. Frontend (/front)
The user interface is built for speed and aesthetics.
*   **Core**: React 18 + TypeScript + Vite (Lightning fast build tool).
*   **Styling**: TailwindCSS with a custom "Pro" color palette (Deep Navy & Soft Beige).
*   **Animations**: `framer-motion` for smooth page transitions and interactive elements.
*   **State Management**: React Context (`AuthContext`) for global user state.
*   **API Layer**: Centralized `Axios` instance with interceptors for automatic token handling.
*   **Key Components**:
    *   `EmployeeForm`: A comprehensive 30-field form mapped dynamically to the ML model.
    *   `AnalyticsPage`: Real-time dashboard visualizing churn risk and AI insights.

### 2. Backend (/backend)
A high-performance asynchronous API built with Python.
*   **Framework**: FastAPI (REST API with automatic Swagger docs).
*   **Database**: PostgreSQL (via NeonDB) with SQLAlchemy ORM.
*   **Authentication**: OAuth2 with Password Flow + JWT Tokens (Secure & Stateless).
*   **Architecture**:
    *   `routers/`: Distinct endpoints for `auth` and `prediction`.
    *   `services/`: Business logic isolation (e.g., `GenAIService` abstracts Google Gemini interactions).
    *   `schemas/`: Pydantic models for strict data validation (Input/Output).

### 3. Machine Learning (/ml)
The intelligence core of the application.
*   **Model**: XGBoost Classifier (Gradient Boosting) for high-accuracy predictions on tabular HR data.
*   **Preprocessing**: Custom `LabelEncoder` pipelines to transform categorical data (e.g., "Travel_Rarely" -> 1).
*   **Integration**: The model is serialized (`.pkl` or `.json`) and loaded into the backend memory for sub-millisecond inference latency.

### 4. Infrastructure (Docker)
The entire stack is containerized for consistency across environments.
*   **Frontend Container**: Multi-stage build (Node build -> Nginx Alpine image) to serve static assets efficiently.
*   **Backend Container**: Python 3.11 slim image running `uvicorn` server.
*   **Networking**: Internal Docker network allows services to communicate securely (Frontend talks to Backend on port 8000).

---

## Quick Start (Docker)

**Prerequisites**: Docker Desktop installed.

1.  **Configure Environment**:
    Create `backend/.env` with your API keys (Database URL, Secret Key, Gemini Key).

2.  **Run Application**:
    ```bash
    docker-compose up --build
    ```

3.  **Access**:
    *   **App**: [http://localhost:3000](http://localhost:3000)
    *   **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Development Setup

If you need to run services manually without Docker:

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd front
npm install
npm run dev
```
