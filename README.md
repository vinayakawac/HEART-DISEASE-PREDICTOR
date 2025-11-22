# Heart Disease Prediction API 

A production-ready REST API for predicting heart disease risk using machine learning. Built with FastAPI and containerized for easy deployment.

##  Features

- **High-Performance API**: Built with FastAPI for async request handling
- **Machine Learning**: Random Forest classifier with 85%+ accuracy
- **Production-Ready**: Comprehensive logging, monitoring, and error handling
- **Containerized**: Docker and Docker Compose support
- **Kubernetes-Ready**: K8s manifests for orchestration
- **CI/CD Pipeline**: GitHub Actions workflow for testing and deployment
- **Monitoring**: Prometheus metrics and Grafana dashboards
- **Comprehensive Tests**: Unit and integration tests with 90%+ coverage
- **API Documentation**: Interactive Swagger UI and ReDoc

## ? Prerequisites

- Python 3.9+ (for local development)
- Docker and Docker Compose (for containerized deployment)
- Kubernetes cluster (optional, for K8s deployment)

## ? Quick Start

### Option 1: Docker Compose (Recommended)

\`\`\`bash
# Clone repository
git clone https://github.com/vinayakawac/HEART-DISEASE-PREDICTOR.git
cd HEART-DISEASE-PREDICTOR

# Run with Docker Compose
docker-compose up -d

# Access API at http://localhost:8000/docs
\`\`\`

### Option 2: Local Development

\`\`\`bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

### Option 3: Kubernetes

\`\`\`bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/ingress.yaml
\`\`\`

##  API Usage

### Predict Heart Disease Risk

\`\`\`bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
\`\`\`

**Response:**
\`\`\`json
{
  "prediction": 1,
  "probability": 0.85,
  "risk_level": "High",
  "timestamp": "2025-11-22T12:00:00Z"
}
\`\`\`

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

##  Testing

\`\`\`bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
\`\`\`

##  Model Information

### Input Features (13 total)

| Feature | Description | Range |
|---------|-------------|-------|
| age | Age in years | 20-100 |
| sex | Sex (1=male, 0=female) | 0-1 |
| cp | Chest pain type | 0-3 |
| trestbps | Resting blood pressure (mm Hg) | 90-200 |
| chol | Serum cholesterol (mg/dl) | 100-600 |
| fbs | Fasting blood sugar > 120 mg/dl | 0-1 |
| restecg | Resting ECG results | 0-2 |
| thalach | Maximum heart rate achieved | 60-220 |
| exang | Exercise induced angina | 0-1 |
| oldpeak | ST depression | 0-6.2 |
| slope | Slope of peak exercise ST | 0-2 |
| ca | Major vessels colored | 0-3 |
| thal | Thalassemia | 0-3 |

### Model Performance
- **Algorithm**: Random Forest Classifier
- **Accuracy**: ~85%
- **Precision**: ~83%
- **Recall**: ~87%

##  Configuration

Create `.env` file from `.env.example`:

\`\`\`bash
cp .env.example .env
\`\`\`

Key environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| ENVIRONMENT | Environment mode | production |
| LOG_LEVEL | Logging level | INFO |
| MODEL_PATH | Path to model | models/heart_disease_model_forest.joblib |
| WORKERS | Number of workers | 4 |

##  Monitoring

### Prometheus Metrics
Access at http://localhost:9090 (when monitoring profile enabled)

\`\`\`bash
docker-compose --profile monitoring up -d
\`\`\`

Available metrics:
- `prediction_requests_total`: Total predictions
- `prediction_duration_seconds`: Prediction latency
- `http_requests_total`: HTTP request count

### Grafana Dashboards
Access at http://localhost:3000 (default: admin/admin)

## ? Deployment

### AWS ECS
\`\`\`bash
# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.region.amazonaws.com
docker tag heart-disease-predictor:latest <account>.dkr.ecr.region.amazonaws.com/heart-disease:latest
docker push <account>.dkr.ecr.region.amazonaws.com/heart-disease:latest
\`\`\`

### Google Cloud Run
\`\`\`bash
gcloud builds submit --tag gcr.io/PROJECT-ID/heart-disease
gcloud run deploy --image gcr.io/PROJECT-ID/heart-disease --platform managed
\`\`\`

### Heroku
\`\`\`bash
heroku container:push web -a your-app-name
heroku container:release web -a your-app-name
\`\`\`

##  Security Features

- Non-root Docker user
- Input validation with Pydantic
- Rate limiting
- CORS configuration
- Comprehensive error handling
- Health check endpoints

##  Project Structure

\`\`\`
.
+-- app/
|   +-- main.py              # FastAPI application
|   +-- api/
|   |   +-- endpoints.py     # API routes
|   +-- core/
|   |   +-- config.py        # Configuration
|   |   +-- logging.py       # Logging
|   +-- models/
|   |   +-- schemas.py       # Pydantic schemas
|   +-- services/
|       +-- prediction.py    # ML service
+-- models/                   # Trained models
+-- tests/                    # Test suite
+-- k8s/                      # Kubernetes manifests
+-- .github/workflows/        # CI/CD pipeline
+-- Dockerfile
+-- docker-compose.yml
+-- requirements.txt
\`\`\`

## ? Contributing

1. Fork the repository
2. Create feature branch (\`git checkout -b feature/amazing-feature\`)
3. Commit changes (\`git commit -m 'Add amazing feature'\`)
4. Push to branch (\`git push origin feature/amazing-feature\`)
5. Open Pull Request

## ? License

MIT License - see [LICENSE](LICENSE) file

## ? Author

**Vinayak** - [@vinayakawac](https://github.com/vinayakawac)

## ? Acknowledgments

- UCI Heart Disease Dataset
- FastAPI Framework
- scikit-learn Library

---

 **Disclaimer**: This API is for educational purposes. Consult healthcare professionals for medical decisions.
