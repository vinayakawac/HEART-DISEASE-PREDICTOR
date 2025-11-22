"""ML prediction service."""

import joblib
import numpy as np
from pathlib import Path
from typing import List, Dict

from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.schemas import PatientData

settings = get_settings()
logger = get_logger(__name__)


class PredictionService:
    """Service for handling ML predictions."""
    
    def __init__(self):
        """Initialize the prediction service."""
        self.model = None
        self.scaler = None
        self.models_loaded = False
        self.load_models()
        
    def load_models(self) -> bool:
        """Load ML model and scaler."""
        try:
            logger.info("Loading ML models...")
            
            # Load Random Forest model and scaler
            forest_path = Path(settings.FOREST_MODEL_PATH)
            forest_scaler_path = Path(settings.FOREST_SCALER_PATH)
            
            if forest_path.exists() and forest_scaler_path.exists():
                self.model = joblib.load(forest_path)
                self.scaler = joblib.load(forest_scaler_path)
                logger.info(f"Random Forest model loaded from {forest_path}")
                self.models_loaded = True
                return True
            else:
                logger.error(f"Model not found at {forest_path}")
                return False
            
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}", exc_info=True)
            return False
    
    def preprocess_input(self, patient_data: PatientData) -> np.ndarray:
        """Convert patient data to model input format."""
        data = np.array([[
            patient_data.age,
            patient_data.sex,
            patient_data.cp,
            patient_data.trestbps,
            patient_data.chol,
            patient_data.fbs,
            patient_data.restecg,
            patient_data.thalach,
            patient_data.exang,
            patient_data.oldpeak,
            patient_data.slope,
            patient_data.ca,
            patient_data.thal
        ]])
        return self.scaler.transform(data)
    
    def predict(self, patient_data: PatientData) -> Dict:
        """
        Predict heart disease risk for a patient.
        
        Returns:
            Dictionary with prediction, probability, and risk level
        """
        # Preprocess input
        X = self.preprocess_input(patient_data)
        
        # Make prediction
        prediction = int(self.model.predict(X)[0])
        probability = float(self.model.predict_proba(X)[0][1])
        
        # Determine risk level
        risk_level = self._get_risk_level(probability)
        
        return {
            "prediction": prediction,
            "probability": round(probability, 2),
            "risk_level": risk_level
        }
    
    def predict_batch(self, patients: List[PatientData]) -> List[Dict]:
        """Predict for multiple patients."""
        return [self.predict(patient) for patient in patients]
    
    def _get_risk_level(self, probability: float) -> str:
        """Determine risk level based on probability."""
        if probability < 0.3:
            return "Low"
        elif probability < 0.5:
            return "Moderate"
        elif probability < 0.7:
            return "High"
        else:
            return "Very High"
    
    def get_feature_names(self) -> List[str]:
        """Get list of feature names."""
        return [
            "age", "sex", "cp", "trestbps", "chol", "fbs",
            "restecg", "thalach", "exang", "oldpeak",
            "slope", "ca", "thal"
        ]


# Singleton instance
_prediction_service: PredictionService = None


def get_prediction_service() -> PredictionService:
    """Get or create prediction service instance."""
    global _prediction_service
    if _prediction_service is None:
        _prediction_service = PredictionService()
    return _prediction_service
