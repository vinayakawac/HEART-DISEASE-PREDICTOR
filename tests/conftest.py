"""Pytest configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_valid_input():
    """Provide sample valid input data for testing."""
    return {
        "age": 55,
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


@pytest.fixture
def sample_invalid_input():
    """Provide sample invalid input data for testing."""
    return {
        "age": -5,
        "sex": 3,
        "cp": 5,
        "trestbps": 300,
        "chol": 1000,
        "fbs": 2,
        "restecg": 5,
        "thalach": 300,
        "exang": 3,
        "oldpeak": -5,
        "slope": 5,
        "ca": 10,
        "thal": 10
    }
