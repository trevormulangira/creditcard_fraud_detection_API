# Credit Card Fraud Detection API

This project is a FastAPI application for detecting fraudulent credit card transactions using a trained machine learning pipeline. The app loads a saved scikit-learn model at startup, validates incoming transaction data, and exposes endpoints for prediction and health checks.

## What has been added

The current version includes the following project changes:

- A FastAPI app with a startup lifespan hook that loads the serialized model once at application startup
- A `/predict` endpoint that accepts transaction features in the expected schema and returns:
  - `is_fraud`
  - `fraud_probability`
- Input validation using Pydantic for all `V1` to `V28` features and `Amount`
- Validation that rejects negative transaction amounts
- A `/health` endpoint to confirm the model is loaded and the service is healthy
- Basic automated tests covering invalid and valid request payloads
- Docker configuration for running the API in a container
- Utility script for inspecting the saved model pipeline

## Project overview

The API is designed for a card fraud dataset where each request contains a transaction record with:

- 28 anonymized PCA features: `V1` through `V28`
- A numeric `Amount` value

The model is expected to be trained and saved as a pipeline object compatible with `predict()` and `predict_proba()`.

## Tech stack

- Python 3.12+
- FastAPI
- Uvicorn
- Pydantic
- pandas
- scikit-learn
- joblib
- pytest
- Docker

## Project structure

```text
.
├── main.py                     # FastAPI app, model loading, and endpoints
├── test_main.py                # API tests for validation and prediction behavior
├── inspect_model.py            # Model inspection utility
├── tuned_random_forest_v1.joblib   # Trained model pipeline
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container build definition
├── .env                        # Local config values for the model name
├── .gitignore                 # Git exclusions
├── README.md                  # Project documentation
└── .vscode/
```

## Installation

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Start the API:

```powershell
uvicorn main:app --reload
```

The app will be available at:

- API: http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API endpoints

### GET /health

Returns the current application health and whether the model has loaded successfully.

Example response:

```json
{
  "status": "healthy",
  "model_loaded": true
}
```

If the model is not initialized, the endpoint returns:

```json
{
  "status": "unhealthy",
  "model_loaded": false
}
```

### POST /predict

This endpoint accepts a transaction object and returns a fraud prediction.

Request body example:

```json
{
  "V1": -1.456,
  "V2": 0.524,
  "V3": 1.123,
  "V4": -2.034,
  "V5": 0.789,
  "V6": -0.456,
  "V7": 1.567,
  "V8": -1.234,
  "V9": 0.654,
  "V10": 0.432,
  "V11": -0.111,
  "V12": 0.933,
  "V13": -0.876,
  "V14": 1.001,
  "V15": -1.452,
  "V16": 0.518,
  "V17": 0.222,
  "V18": -0.776,
  "V19": 0.998,
  "V20": -0.432,
  "V21": 1.121,
  "V22": -0.333,
  "V23": 0.991,
  "V24": -1.412,
  "V25": 0.652,
  "V26": -0.883,
  "V27": 0.876,
  "V28": 1.229,
  "Amount": 100.0
}
```

Example response:

```json
{
  "is_fraud": false,
  "fraud_probability": 0.1203
}
```

Response behavior:

- `is_fraud` is a boolean prediction from the model
- `fraud_probability` is the probability for the fraud class returned by `predict_proba()`
- Negative `Amount` values are rejected with a 400 error
- Missing required features return a 422 validation error

## Testing

Run the test suite:

```powershell
pytest
```

Current tests verify:

- Missing feature payloads are rejected as invalid input
- A valid transaction payload returns a successful prediction response

## Docker

Build the image:

```powershell
docker build -t credit-card-fraud-api .
```

Run the container:

```powershell
docker run --rm -p 8000:8000 credit-card-fraud-api
```

Then open the app in the browser at:

http://localhost:8000/docs

## Model inspection

To inspect the loaded model object and confirm the expected feature names and pipeline steps:

```powershell
python inspect_model.py
```

## Notes

- The app expects a valid serialized model file named `tuned_random_forest_v1.joblib` in the project root.
- The model must be trained with the same feature schema used by this API (`V1` to `V28` + `Amount`).
- This API is suitable for local development and testing, and should be hardened before production deployment.
- Fraud detection is a risk signal, not an automatic decision-making system for financial enforcement.