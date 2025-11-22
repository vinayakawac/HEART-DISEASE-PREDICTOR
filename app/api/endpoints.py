"""API endpoints for predictions."""

from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from typing import List

from app.models.schemas import PatientData
from app.services.prediction import PredictionService
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1", tags=["Predictions"])

# Initialize prediction service
prediction_service = PredictionService()


@router.post(
    "/predict",
    status_code=status.HTTP_200_OK,
    summary="Predict Heart Disease Risk",
    description="Predict the risk of heart disease based on patient health data."
)
async def predict_heart_disease(patient_data: PatientData):
    """
    Predict heart disease risk for a single patient.
    
    Returns prediction with probability and risk level.
    """
    try:
        result = prediction_service.predict(patient_data)
        result["timestamp"] = datetime.utcnow().isoformat() + "Z"
        return result
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post(
    "/predict/batch",
    status_code=status.HTTP_200_OK,
    summary="Batch Predict Heart Disease Risk",
    description="Predict heart disease risk for multiple patients."
)
async def predict_batch(patients: dict):
    """
    Predict heart disease risk for multiple patients.
    
    Returns predictions for all patients.
    """
    try:
        patient_list = [PatientData(**p) for p in patients["patients"]]
        results = prediction_service.predict_batch(patient_list)
        
        for result in results:
            result["timestamp"] = datetime.utcnow().isoformat() + "Z"
        
        return {
            "predictions": results,
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}"
        )


@router.get(
    "/model/info",
    summary="Get Model Information",
    description="Retrieve information about the ML model."
)
async def get_model_info():
    """Get information about the model."""
    try:
        features = prediction_service.get_feature_names()
        return {
            "model_name": "RandomForestClassifier",
            "version": "1.0.0",
            "features": features,
            "feature_count": len(features),
            "trained_date": "2024-01-15",
            "accuracy": 0.85
        }
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving model information"
        )
