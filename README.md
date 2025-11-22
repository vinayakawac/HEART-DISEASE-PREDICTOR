# Heart Disease Prediction API

> An intelligent API that helps predict heart disease risk using machine learning. Think of it as your AI-powered medical assistant that analyzes patient data and provides instant risk assessments.

## What Does This Do?

This is a REST API that predicts whether a patient is at risk of heart disease based on their medical data. Just send us patient information like age, blood pressure, cholesterol levels, and our Random Forest machine learning model will analyze it and give you back a risk assessment with probability scores.

**Real-world use case**: Doctors and healthcare apps can integrate this API to get quick preliminary risk assessments, helping prioritize patients who may need further testing.

## Why Use This?

- **Fast & Accurate**: 85%+ accuracy with predictions in milliseconds
- **Easy to Use**: Simple REST API with clear documentation
- **Production Ready**: Already set up with logging, monitoring, and error handling
- **Deploy Anywhere**: Works with Docker, Kubernetes, AWS, Google Cloud, Heroku, etc.
- **Well Tested**: Comprehensive test suite ensures reliability
- **Free & Open Source**: Use it, modify it, deploy it - it's yours!

## What You'll Need

Don't worry, it's straightforward! You just need:

- **Python 3.9 or newer** (if running locally)
- **Docker** (easiest way to run it - we recommend this!)
- **5 minutes** of your time to get it running

## Getting Started (Super Easy!)

### The Fastest Way: Using Docker

This is the easiest method - just three commands and you're done!

```bash
# 1. Get the code
git clone https://github.com/vinayakawac/HEART-DISEASE-PREDICTOR.git
cd HEART-DISEASE-PREDICTOR

# 2. Start everything with Docker
docker-compose up -d

# 3. That's it! Open your browser
# Go to: http://localhost:8000/docs
```

**What just happened?** Docker automatically downloaded everything needed, set up the API, and started it. You can now test it directly in your browser!

### Running Locally (Without Docker)

If you prefer to run it directly on your machine:

```bash
# 1. Create a clean Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install everything we need
pip install -r requirements.txt

# 3. Start the API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs to see your API in action!

### For Kubernetes Users

Already have a K8s cluster? Deploy it with:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/ingress.yaml
```

## How to Use the API

### Try It Out in Your Browser (No Coding Required!)

Just open http://localhost:8000/docs in your browser. You'll see an interactive playground where you can:
1. Click on any endpoint
2. Hit "Try it out"
3. Enter patient data
4. Click "Execute"
5. See the results instantly!

**No terminal commands needed** - it's all point-and-click.

### For Developers: Make API Calls

Here's how to check a patient's heart disease risk from your code:

```bash
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
```

**What you'll get back:**
```json
{
  "prediction": 1,           // 1 = Risk detected, 0 = No risk
  "probability": 0.85,       // 85% confidence
  "risk_level": "High",      // Easy-to-understand risk level
  "timestamp": "2025-11-22T12:00:00Z"
}
```

**Understanding the result**: This patient has an 85% probability of heart disease risk. The API categorizes this as "High" risk, suggesting they should consult a healthcare professional.

### Want More Details?

We have two types of documentation:
- **Interactive (Swagger)**: http://localhost:8000/docs - Play around and test everything
- **Traditional (ReDoc)**: http://localhost:8000/redoc - Read detailed descriptions

## Running Tests

Want to make sure everything works? Run the test suite:

```bash
# Run all tests (should see 14 tests pass)
pytest tests/ -v

# Check how much code is tested
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html  # See a detailed report
```

All 14 tests should pass - if they do, you're good to go!

## Understanding the Patient Data

The API needs 13 pieces of information about a patient. Here's what each means in plain English:

| What It Is | What It Means | Valid Values |
|------------|---------------|--------------|
| **age** | Patient's age in years | 20 to 100 |
| **sex** | Gender of patient | 1 = Male, 0 = Female |
| **cp** | Type of chest pain they feel | 0 to 3 (0=typical angina, 3=no symptoms) |
| **trestbps** | Blood pressure at rest (mm Hg) | 90 to 200 |
| **chol** | Cholesterol level (mg/dl) | 100 to 600 |
| **fbs** | Is blood sugar over 120? | 1 = Yes, 0 = No |
| **restecg** | Resting heart electrical activity | 0 to 2 (ECG results) |
| **thalach** | Max heart rate during exercise | 60 to 220 |
| **exang** | Does exercise cause chest pain? | 1 = Yes, 0 = No |
| **oldpeak** | ST depression (heart stress indicator) | 0 to 6.2 |
| **slope** | Heart rate pattern during peak exercise | 0 to 2 |
| **ca** | Major blood vessels visible in scan | 0 to 3 |
| **thal** | Thalassemia blood disorder status | 0 to 3 |

### How Accurate Is It?

Our Random Forest model has been trained and tested on real patient data:
- **85% Accuracy** - Correctly predicts 85 out of 100 cases
- **83% Precision** - When it says "risk", it's right 83% of the time
- **87% Recall** - Catches 87% of actual heart disease cases

**What this means**: It's pretty reliable! But remember, this is a tool to help healthcare professionals, not replace them.

## Customizing Settings (Optional)

Want to change how the API behaves? Copy the example settings file:

```bash
cp .env.example .env
# Then edit .env with your preferred text editor
```

Here are the main settings you might want to tweak:

| Setting | What It Does | Default Value |
|---------|--------------|---------------|
| ENVIRONMENT | Switch between dev/production mode | production |
| LOG_LEVEL | How detailed should logs be? | INFO |
| WORKERS | Number of parallel processes | 4 |
| MODEL_PATH | Where the AI model file is stored | models/heart_disease_model_forest.joblib |

**For most users**: The defaults work great, no need to change anything!

## Monitoring Your API (For Production Use)

If you're running this in production and want to keep an eye on performance:

```bash
# Start the API with monitoring dashboards
docker-compose --profile monitoring up -d
```

This gives you:
- **Prometheus** (http://localhost:9090) - See real-time metrics
- **Grafana** (http://localhost:3000) - Beautiful performance dashboards
  - Login: admin / admin

You'll be able to see:
- How many predictions you're making
- How fast the API responds
- If there are any errors

## Deploying to the Cloud

Ready to make this API available to the world? Here are the easiest options:

### Heroku (Easiest - Perfect for Beginners)

```bash
heroku container:push web -a your-app-name
heroku container:release web -a your-app-name
```

Done! Your API is now live on the internet.

### Google Cloud Run (Also Very Easy)

```bash
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/heart-disease
gcloud run deploy --image gcr.io/YOUR-PROJECT-ID/heart-disease --platform managed
```

Google handles everything - scaling, SSL certificates, monitoring.

### Amazon AWS ECS (For AWS Users)

```bash
# Push your container to AWS
aws ecr get-login-password | docker login --username AWS --password-stdin YOUR-ACCOUNT.dkr.ecr.region.amazonaws.com
docker tag heart-disease-predictor:latest YOUR-ACCOUNT.dkr.ecr.region.amazonaws.com/heart-disease:latest
docker push YOUR-ACCOUNT.dkr.ecr.region.amazonaws.com/heart-disease:latest
```

**Need more detailed deployment instructions?** Check out `docs/DEPLOYMENT.md` for step-by-step guides for each platform.

## Security - We've Got You Covered

This API includes several security measures out of the box:

- **Input Validation**: Rejects bad or malicious data automatically
- **Rate Limiting**: Prevents abuse by limiting requests per minute
- **CORS Protection**: Controls which websites can access your API
- **Error Handling**: Never exposes sensitive system information
- **Health Checks**: Kubernetes and Docker can verify it's running correctly
- **No Root Access**: Runs with minimal privileges (Docker best practice)

## How Is This Organized?

Here's the folder structure - where everything lives:

```
heart-disease-predictor/
├── app/                      # Main application code
│   ├── main.py              # The heart of the API
│   ├── api/                 # API endpoints (routes)
│   ├── core/                # Configuration and logging
│   ├── models/              # Data validation schemas
│   └── services/            # The ML prediction logic
├── models/                   # Trained AI models (the brain!)
├── tests/                    # All our tests to ensure quality
├── k8s/                      # Kubernetes deployment files
├── docs/                     # Additional documentation
├── Dockerfile               # Instructions to build container
├── docker-compose.yml       # Easy multi-container setup
└── requirements.txt         # Python packages we need
```

## Want to Contribute?

We'd love your help! Here's how:

1. **Fork this repo** (top right on GitHub)
2. **Create a branch** for your feature: `git checkout -b feature/my-cool-feature`
3. **Make your changes** and commit: `git commit -m 'Added something cool'`
4. **Push to your fork**: `git push origin feature/my-cool-feature`
5. **Open a Pull Request** - describe what you've added!

All skill levels welcome - whether it's fixing a typo or adding a major feature!

## License

This project is open source under the MIT License. That means you can:
- Use it for free (personal or commercial)
- Modify it however you want
- Share it with others

See the [LICENSE](LICENSE) file for the legal details.

## Credits

**Created by**: Vinayak ([@vinayakawac](https://github.com/vinayakawac))

**Built with these amazing tools**:
- [FastAPI](https://fastapi.tiangolo.com/) - The web framework
- [scikit-learn](https://scikit-learn.org/) - Machine learning library
- UCI Heart Disease Dataset - Training data

**Special thanks** to the open source community!

---

## Important Note

**This API is for educational and research purposes.** While our model is quite accurate, it should never replace professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for medical decisions.

Think of this as a screening tool that can help prioritize cases, not a replacement for doctors!

---

**Questions? Issues? Ideas?** 
Open an issue on GitHub or reach out. We're here to help!
