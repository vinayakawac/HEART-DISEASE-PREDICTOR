# Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- kubectl configured (for Kubernetes)
- Cloud provider account (AWS/GCP/Azure)

## Local Deployment

### Using Docker Compose

1. **Start all services**
```bash
docker-compose up -d
```

2. **Check logs**
```bash
docker-compose logs -f app
```

3. **Stop services**
```bash
docker-compose down
```

### With Monitoring Stack

```bash
docker-compose --profile monitoring up -d
```

This starts:
- API service on port 8000
- Prometheus on port 9091
- Grafana on port 3000

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (EKS, GKE, AKS, or local like Minikube)
- kubectl configured

### Steps

1. **Create namespace**
```bash
kubectl create namespace heart-disease-predictor
```

2. **Deploy application**
```bash
kubectl apply -f k8s/deployment.yaml
```

3. **Deploy ingress (optional)**
```bash
kubectl apply -f k8s/ingress.yaml
```

4. **Check status**
```bash
kubectl get pods -n heart-disease-predictor
kubectl get svc -n heart-disease-predictor
```

5. **View logs**
```bash
kubectl logs -f deployment/heart-disease-api -n heart-disease-predictor
```

### Scaling

```bash
# Manual scaling
kubectl scale deployment heart-disease-api --replicas=5 -n heart-disease-predictor

# Auto-scaling is already configured via HPA
kubectl get hpa -n heart-disease-predictor
```

## Cloud Deployments

### AWS ECS

1. **Create ECR repository**
```bash
aws ecr create-repository --repository-name heart-disease-predictor
```

2. **Build and push image**
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker build -t heart-disease-predictor .
docker tag heart-disease-predictor:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/heart-disease-predictor:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/heart-disease-predictor:latest
```

3. **Create ECS cluster and service**
```bash
# Use AWS Console or CLI to create:
# - ECS Cluster
# - Task Definition
# - Service with load balancer
```

### Google Cloud Run

1. **Build and deploy**
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/heart-disease-predictor

gcloud run deploy heart-disease-api \
  --image gcr.io/PROJECT-ID/heart-disease-predictor \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 2 \
  --min-instances 1 \
  --max-instances 10
```

2. **Get service URL**
```bash
gcloud run services describe heart-disease-api --region us-central1
```

### Azure Container Instances

1. **Create resource group**
```bash
az group create --name heart-disease-rg --location eastus
```

2. **Deploy container**
```bash
az container create \
  --resource-group heart-disease-rg \
  --name heart-disease-api \
  --image <registry>/heart-disease-predictor:latest \
  --dns-name-label heart-disease-unique \
  --ports 8000 \
  --cpu 2 \
  --memory 2
```

### Heroku

1. **Login to Heroku**
```bash
heroku login
heroku container:login
```

2. **Create app**
```bash
heroku create your-app-name
```

3. **Deploy**
```bash
heroku container:push web -a your-app-name
heroku container:release web -a your-app-name
```

4. **Open app**
```bash
heroku open -a your-app-name
```

## Environment Variables

Set these in your deployment platform:

```bash
ENVIRONMENT=production
LOG_LEVEL=INFO
MODEL_PATH=/app/models/heart_disease_model_forest.joblib
SCALER_PATH=/app/models/scaler_forest.joblib
WORKERS=4
```

## Health Checks

Configure health check endpoints:
- **Liveness**: `GET /health`
- **Readiness**: `GET /health`

## Monitoring

### Prometheus

Scrape endpoint: `http://service:8000/metrics`

### Logging

Logs are available:
- **Docker**: `docker-compose logs -f`
- **Kubernetes**: `kubectl logs -f <pod-name>`
- **Cloud**: Check respective cloud provider's logging service

## Troubleshooting

### Container won't start

```bash
# Check logs
docker logs heart-disease-predictor

# Verify models exist
docker exec heart-disease-predictor ls -la /app/models
```

### High memory usage

```bash
# Reduce workers in environment
WORKERS=2

# Or limit memory in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 1G
```

### Model loading errors

```bash
# Verify model files
ls -lh models/

# Check file permissions
chmod 644 models/*.joblib
```

## Security Best Practices

1. **Use secrets management**
   - AWS Secrets Manager
   - GCP Secret Manager
   - Azure Key Vault
   - Kubernetes Secrets

2. **Enable HTTPS**
   - Use Ingress with TLS
   - Cloud provider load balancers
   - Let's Encrypt certificates

3. **Implement authentication**
   - API keys
   - OAuth2
   - JWT tokens

4. **Rate limiting**
   - Configure in ingress
   - Use cloud provider features
   - Implement in application

## Backup and Recovery

1. **Model files**
   - Store in S3/GCS/Azure Blob
   - Version control with Git LFS
   - Regular backups

2. **Logs**
   - Ship to centralized logging
   - CloudWatch, Stackdriver, Azure Monitor
   - ELK stack

## Performance Optimization

1. **Increase workers**
```bash
WORKERS=8  # Based on CPU cores
```

2. **Use load balancer**
   - Application Load Balancer (AWS)
   - Cloud Load Balancing (GCP)
   - Azure Load Balancer

3. **Enable caching**
   - Redis for prediction cache
   - CloudFront/CDN for static assets

4. **Horizontal scaling**
   - Auto-scaling groups
   - Kubernetes HPA
   - Cloud provider auto-scaling

## Cost Optimization

1. **Right-size instances**
   - Monitor resource usage
   - Adjust CPU/memory limits
   - Use spot/preemptible instances

2. **Auto-scaling**
   - Scale down during low traffic
   - Set minimum and maximum replicas

3. **Use serverless**
   - AWS Lambda with API Gateway
   - Google Cloud Functions
   - Azure Functions
