"""Test cases for API endpoints."""
import pytest
from fastapi.testclient import TestClient


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_loaded" in data
    assert "timestamp" in data


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Heart Disease Prediction API" in data["message"]


def test_model_info(client):
    """Test the model info endpoint."""
    response = client.get("/api/v1/model/info")
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "version" in data
    assert "features" in data
    assert len(data["features"]) == 13


def test_predict_valid_input(client, sample_valid_input):
    """Test prediction with valid input."""
    response = client.post("/api/v1/predict", json=sample_valid_input)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability" in data
    assert "risk_level" in data
    assert data["prediction"] in [0, 1]
    assert 0 <= data["probability"] <= 1


def test_predict_batch_valid_input(client, sample_valid_input):
    """Test batch prediction with valid input."""
    batch_input = {"patients": [sample_valid_input, sample_valid_input]}
    response = client.post("/api/v1/predict/batch", json=batch_input)
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert len(data["predictions"]) == 2
    for pred in data["predictions"]:
        assert "prediction" in pred
        assert "probability" in pred
        assert "risk_level" in pred


def test_predict_missing_field(client):
    """Test prediction with missing required field."""
    invalid_input = {
        "age": 55,
        "sex": 1,
        # Missing other required fields
    }
    response = client.post("/api/v1/predict", json=invalid_input)
    assert response.status_code == 422  # Validation error


def test_predict_invalid_value_type(client):
    """Test prediction with invalid value type."""
    invalid_input = {
        "age": "invalid",
        "sex": 1,
        "cp": 2,
        "trestbps": 130,
        "chol": 250,
        "fbs": 1,
        "restecg": 1,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 1.5,
        "slope": 2,
        "ca": 0,
        "thal": 2
    }
    response = client.post("/api/v1/predict", json=invalid_input)
    assert response.status_code == 422  # Validation error


def test_metrics_endpoint(client):
    """Test the metrics endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text or "predictions_total" in response.text
