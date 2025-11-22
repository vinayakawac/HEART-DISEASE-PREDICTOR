# Scripts Directory

This directory contains utility scripts for training models and processing data.

## Training Scripts

Located in `training/` directory:

### `train_random_forest.py`
Trains the Random Forest classifier model for heart disease prediction.

**Usage:**
```bash
python scripts/training/train_random_forest.py
```

**Outputs:**
- `models/heart_disease_model_forest.joblib` - Trained Random Forest model
- `models/scaler_forest.joblib` - StandardScaler for feature normalization

### `train_knn.py`
Trains the K-Nearest Neighbors (KNN) model for heart disease prediction.

**Usage:**
```bash
python scripts/training/train_knn.py
```

**Outputs:**
- `models/heart_disease_knn_model.joblib` - Trained KNN model
- `models/scaler_knn.joblib` - StandardScaler for feature normalization

## Data Processing Scripts

Located in `data_processing/` directory (empty - add your preprocessing scripts here).

## Requirements

Ensure you have installed all dependencies:
```bash
pip install -r requirements.txt
```

## Training Data

Training data should be placed in:
- `data/raw/` - Raw CSV files
- `data/processed/` - Processed datasets ready for training

## Model Versioning

After training new models:
1. Test the model with `pytest tests/`
2. Update model version in `app/core/config.py`
3. Document model performance metrics
4. Commit models with Git LFS (if configured)
