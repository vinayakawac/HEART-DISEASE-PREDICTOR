# API Reference

## Base URL

- **Local**: `http://localhost:8000`
- **Production**: `https://api.yourdomain.com`

## Authentication

Currently, the API is open. To add authentication:
- API Keys
- OAuth2/JWT tokens
- Basic Auth

## Endpoints

### Health Check

Check API health status.

**Endpoint**: `GET /health`

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-11-22T12:00:00Z",
  "version": "1.0.0"
}
```

---

### Root

API information.

**Endpoint**: `GET /`

**Response**: `200 OK`
```json
{
  "message": "Heart Disease Prediction API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

### Single Prediction

Predict heart disease for a single patient.

**Endpoint**: `POST /api/v1/predict`

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
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
```

**Field Descriptions**:
- `age`: Age in years (20-100)
- `sex`: Sex (1 = male, 0 = female)
- `cp`: Chest pain type (0-3)
- `trestbps`: Resting blood pressure in mm Hg (90-200)
- `chol`: Serum cholesterol in mg/dl (100-600)
- `fbs`: Fasting blood sugar > 120 mg/dl (1 = true, 0 = false)
- `restecg`: Resting electrocardiographic results (0-2)
- `thalach`: Maximum heart rate achieved (60-220)
- `exang`: Exercise induced angina (1 = yes, 0 = no)
- `oldpeak`: ST depression induced by exercise relative to rest (0-6.2)
- `slope`: Slope of the peak exercise ST segment (0-2)
- `ca`: Number of major vessels colored by fluoroscopy (0-3)
- `thal`: Thalassemia (0 = normal, 1 = fixed defect, 2 = reversible defect)

**Response**: `200 OK`
```json
{
  "prediction": 1,
  "probability": 0.85,
  "risk_level": "High",
  "timestamp": "2025-11-22T12:00:00.000Z"
}
```

**Response Fields**:
- `prediction`: 0 = No heart disease, 1 = Heart disease present
- `probability`: Probability of heart disease (0.0-1.0)
- `risk_level`: Risk category (Low, Moderate, High, Very High)
- `timestamp`: Prediction timestamp in ISO format

**Error Responses**:

`422 Unprocessable Entity` - Validation error
```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "ensure this value is greater than or equal to 20",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

`500 Internal Server Error` - Prediction failed
```json
{
  "detail": "Prediction failed: <error message>"
}
```

---

### Batch Prediction

Predict heart disease for multiple patients.

**Endpoint**: `POST /api/v1/predict/batch`

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "patients": [
    {
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
    },
    {
      "age": 45,
      "sex": 0,
      "cp": 1,
      "trestbps": 120,
      "chol": 200,
      "fbs": 0,
      "restecg": 0,
      "thalach": 170,
      "exang": 0,
      "oldpeak": 0.5,
      "slope": 1,
      "ca": 0,
      "thal": 1
    }
  ]
}
```

**Response**: `200 OK`
```json
{
  "predictions": [
    {
      "prediction": 1,
      "probability": 0.85,
      "risk_level": "High",
      "timestamp": "2025-11-22T12:00:00.000Z"
    },
    {
      "prediction": 0,
      "probability": 0.15,
      "risk_level": "Low",
      "timestamp": "2025-11-22T12:00:00.000Z"
    }
  ],
  "count": 2
}
```

---

### Model Information

Get information about the ML model.

**Endpoint**: `GET /api/v1/model/info`

**Response**: `200 OK`
```json
{
  "model_name": "RandomForestClassifier",
  "version": "1.0.0",
  "features": [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak",
    "slope", "ca", "thal"
  ],
  "feature_count": 13,
  "trained_date": "2024-01-15",
  "accuracy": 0.85
}
```

---

### Metrics

Prometheus-format metrics.

**Endpoint**: `GET /metrics`

**Response**: `200 OK`
```
# HELP prediction_requests_total Total number of prediction requests
# TYPE prediction_requests_total counter
prediction_requests_total{endpoint="/api/v1/predict"} 1234.0

# HELP prediction_duration_seconds Time spent processing predictions
# TYPE prediction_duration_seconds histogram
prediction_duration_seconds_bucket{le="0.01"} 100.0
...
```

---

## Rate Limiting

Default: 100 requests per minute per IP

**Response when rate limited**: `429 Too Many Requests`
```json
{
  "detail": "Rate limit exceeded. Try again later."
}
```

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error description"
}
```

**HTTP Status Codes**:
- `200`: Success
- `422`: Validation Error
- `429`: Rate Limit Exceeded
- `500`: Internal Server Error
- `503`: Service Unavailable

## Examples

### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{"age": 55, "sex": 1, "cp": 2, "trestbps": 130, "chol": 250, "fbs": 1, "restecg": 1, "thalach": 150, "exang": 0, "oldpeak": 1.5, "slope": 2, "ca": 0, "thal": 2}'
```

### Python

```python
import requests

url = "http://localhost:8000/api/v1/predict"
data = {
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

response = requests.post(url, json=data)
print(response.json())
```

### JavaScript

```javascript
const axios = require('axios');

const data = {
  age: 55,
  sex: 1,
  cp: 2,
  trestbps: 130,
  chol: 250,
  fbs: 1,
  restecg: 1,
  thalach: 150,
  exang: 0,
  oldpeak: 1.5,
  slope: 2,
  ca: 0,
  thal: 2
};

axios.post('http://localhost:8000/api/v1/predict', data)
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
