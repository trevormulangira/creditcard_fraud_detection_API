# Credit Card Fraud Detection API

A FastAPI service that classifies credit card transactions as fraudulent or legitimate using a trained scikit-learn Random Forest pipeline. The API loads the serialized model at startup and exposes prediction and health-check endpoints.

## Features

- Fraud prediction through a JSON REST endpoint
- Fraud probability returned with each prediction
- Required transaction feature validation through Pydantic/FastAPI
- Application health and model-loading status endpoint
- Interactive OpenAPI documentation
- Docker support
- Automated endpoint tests

## Tech Stack

- Python
- FastAPI
- Uvicorn
- scikit-learn
- pandas
- joblib
- Pydantic
- pytest

## Project Structure

```text
.
|-- main.py                        # FastAPI application and endpoints
|-- test_main.py                   # API tests
|-- inspect_model.py               # Utility for inspecting the trained model
|-- tuned_random_forest_v1.joblib  # Serialized trained model pipeline
|-- requirements.txt               # Python dependencies
|-- Dockerfile                     # Container configuration
|-- .env                           # Local model configuration
`-- README.md
```

## Requirements

- Python 3.12 or later
- The model file `tuned_random_forest_v1.joblib` in the project root

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Start the API:

```powershell
uvicorn main:app --reload
```

The service will be available at:

- API: <http://127.0.0.1:8000>
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## API Endpoints

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "model_loaded": true
}
```

If the pipeline has not loaded, the response reports:

```json
{
  "status": "unhealthy",
  "model_loaded": false
}
```

### Predict Fraud

```http
POST /predict
Content-Type: application/json
```

The request must contain numeric values for `V1` through `V28` and a non-negative numeric `Amount`.

Example request:

```json
{
  "V1": 0.0,
  "V2": 0.0,
  "V3": 0.0,
  "V4": 0.0,
  "V5": 0.0,
  "V6": 0.0,
  "V7": 0.0,
  "V8": 0.0,
  "V9": 0.0,
  "V10": 0.0,
  "V11": 0.0,
  "V12": 0.0,
  "V13": 0.0,
  "V14": 0.0,
  "V15": 0.0,
  "V16": 0.0,
  "V17": 0.0,
  "V18": 0.0,
  "V19": 0.0,
  "V20": 0.0,
  "V21": 0.0,
  "V22": 0.0,
  "V23": 0.0,
  "V24": 0.0,
  "V25": 0.0,
  "V26": 0.0,
  "V27": 0.0,
  "V28": 0.0,
  "Amount": 100.0
}
```

Example response:

```json
{
  "is_fraud": false,
  "fraud_probability": 0.12
}
```

`is_fraud` indicates the model's predicted class. `fraud_probability` is the model's probability for the fraud class and may be influenced by the model's decision threshold or training configuration.

### Status Codes

| Status | Meaning |
| --- | --- |
| `200` | Prediction completed successfully |
| `422` | Required transaction fields are missing or invalid |
| `400` | The transaction amount is negative |
| `500` | An unexpected prediction error occurred |

## cURL Example

```bash
curl.exe -X POST "http://127.0.0.1:8000/predict" ^
  -H "Content-Type: application/json" ^
  -d "{\"V1\":0,\"V2\":0,\"V3\":0,\"V4\":0,\"V5\":0,\"V6\":0,\"V7\":0,\"V8\":0,\"V9\":0,\"V10\":0,\"V11\":0,\"V12\":0,\"V13\":0,\"V14\":0,\"V15\":0,\"V16\":0,\"V17\":0,\"V18\":0,\"V19\":0,\"V20\":0,\"V21\":0,\"V22\":0,\"V23\":0,\"V24\":0,\"V25\":0,\"V26\":0,\"V27\":0,\"V28\":0,\"Amount\":100}"
```

## Testing

Run the test suite from the project root:

```powershell
pytest
```

The tests verify that:

- Requests with missing transaction features are rejected
- Valid transactions produce both prediction fields

## Docker

Build the image:

```powershell
docker build -t credit-card-fraud-api .
```

Run the container:

```powershell
docker run --rm -p 8000:8000 credit-card-fraud-api
```

Then open <http://localhost:8000/docs>.

## Model Inspection

To view the serialized model type and, when available, its pipeline steps and expected feature names:

```powershell
python inspect_model.py
```

## Notes

- Replace `tuned_random_forest_v1.joblib` with a compatible trained pipeline that supports `predict` and `predict_proba`.
- The model expects the same 29 input features in the same order used during training.
- The API is intended for development or internal use and should be secured before production deployment.
- Fraud prediction probabilities should not be treated as definitive financial or legal decisions.