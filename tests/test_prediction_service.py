"""Test cases for the prediction service."""
import pytest
import numpy as np
from app.services.prediction import PredictionService
from app.models.schemas import PatientData


def test_service_initialization():
    """Test that the prediction service initializes correctly."""
    service = PredictionService()
    assert service.model is not None
    assert service.scaler is not None


def test_preprocess_input():
    """Test input preprocessing."""
    service = PredictionService()
    patient_data = PatientData(
        age=55, sex=1, cp=2, trestbps=130, chol=250,
        fbs=1, restecg=1, thalach=150, exang=0,
        oldpeak=1.5, slope=2, ca=0, thal=2
    )
    
    processed = service.preprocess_input(patient_data)
    assert isinstance(processed, np.ndarray)
    assert processed.shape == (1, 13)


def test_predict_single():
    """Test single prediction."""
    service = PredictionService()
    patient_data = PatientData(
        age=55, sex=1, cp=2, trestbps=130, chol=250,
        fbs=1, restecg=1, thalach=150, exang=0,
        oldpeak=1.5, slope=2, ca=0, thal=2
    )
    
    result = service.predict(patient_data)
    assert "prediction" in result
    assert "probability" in result
    assert "risk_level" in result
    assert result["prediction"] in [0, 1]
    assert 0 <= result["probability"] <= 1
    assert result["risk_level"] in ["Low", "Moderate", "High", "Very High"]


def test_predict_batch():
    """Test batch prediction."""
    service = PredictionService()
    patient_data = [
        PatientData(
            age=55, sex=1, cp=2, trestbps=130, chol=250,
            fbs=1, restecg=1, thalach=150, exang=0,
            oldpeak=1.5, slope=2, ca=0, thal=2
        ),
        PatientData(
            age=45, sex=0, cp=1, trestbps=120, chol=200,
            fbs=0, restecg=0, thalach=170, exang=0,
            oldpeak=0.5, slope=1, ca=0, thal=1
        )
    ]
    
    results = service.predict_batch(patient_data)
    assert len(results) == 2
    for result in results:
        assert "prediction" in result
        assert "probability" in result
        assert "risk_level" in result


def test_get_risk_level():
    """Test risk level calculation."""
    service = PredictionService()
    
    assert service._get_risk_level(0.1) == "Low"
    assert service._get_risk_level(0.4) == "Moderate"
    assert service._get_risk_level(0.6) == "High"
    assert service._get_risk_level(0.9) == "Very High"


def test_get_feature_names():
    """Test feature names retrieval."""
    service = PredictionService()
    features = service.get_feature_names()
    
    assert len(features) == 13
    assert "age" in features
    assert "sex" in features
    assert "cp" in features
