"""Pydantic schemas for request/response validation."""

from typing import Literal
from pydantic import BaseModel, Field, validator


class PatientData(BaseModel):
    """Input schema for patient health data."""
    
    age: int = Field(..., ge=18, le=100, description="Age in years")
    sex: Literal[0, 1] = Field(..., description="Sex (0=Female, 1=Male)")
    cp: Literal[0, 1, 2, 3] = Field(..., description="Chest pain type (0=Typical angina, 1=Atypical angina, 2=Non-anginal pain, 3=Asymptomatic)")
    trestbps: int = Field(..., ge=90, le=200, description="Resting blood pressure (mm Hg)")
    chol: int = Field(..., ge=100, le=600, description="Serum cholesterol (mg/dl)")
    fbs: Literal[0, 1] = Field(..., description="Fasting blood sugar > 120 mg/dl (0=No, 1=Yes)")
    restecg: Literal[0, 1, 2] = Field(..., description="Resting ECG results (0=Normal, 1=ST-T wave abnormality, 2=Left ventricular hypertrophy)")
    thalach: int = Field(..., ge=60, le=220, description="Maximum heart rate achieved (bpm)")
    exang: Literal[0, 1] = Field(..., description="Exercise induced angina (0=No, 1=Yes)")
    oldpeak: float = Field(..., ge=0, le=6.2, description="ST depression induced by exercise relative to rest")
    slope: Literal[0, 1, 2] = Field(..., description="Slope of peak exercise ST segment (0=Upsloping, 1=Flat, 2=Downsloping)")
    ca: Literal[0, 1, 2, 3, 4] = Field(..., description="Number of major vessels colored by fluoroscopy")
    thal: Literal[0, 1, 2, 3] = Field(..., description="Thalassemia (0=Normal, 1=Fixed defect, 2=Reversible defect, 3=Not normal)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 55,
                "sex": 1,
                "cp": 2,
                "trestbps": 120,
                "chol": 220,
                "fbs": 1,
                "restecg": 1,
                "thalach": 150,
                "exang": 1,
                "oldpeak": 2.5,
                "slope": 1,
                "ca": 2,
                "thal": 1
            }
        }


class PredictionRequest(BaseModel):
    """Request schema for prediction."""
    
    patient_data: PatientData
    model_type: Literal["knn", "random_forest", "auto"] = Field(
        default="auto",
        description="Model to use for prediction (auto selects best performing model)"
    )


class PredictionResponse(BaseModel):
    """Response schema for prediction."""
    
    risk_percentage: float = Field(..., description="Risk of heart disease as percentage")
    risk_level: str = Field(..., description="Risk level classification")
    model_used: str = Field(..., description="Model used for prediction")
    confidence: float = Field(..., description="Prediction confidence score")
    recommendation: str = Field(..., description="Health recommendation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "risk_percentage": 75.5,
                "risk_level": "High",
                "model_used": "random_forest",
                "confidence": 0.85,
                "recommendation": "High risk detected. Please consult a cardiologist immediately."
            }
        }


class ModelInfo(BaseModel):
    """Model information schema."""
    
    name: str
    accuracy: float
    last_trained: str
    features: int


class HealthResponse(BaseModel):
    """Health check response schema."""
    
    status: str
    version: str
    environment: str
    models_loaded: bool


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    error: str
    detail: str
    timestamp: str
