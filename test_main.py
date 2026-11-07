from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_missing_features():

    response = client.post("/predict", json={"Amount": 100.0})  # Missing V1 to V28 features

    assert response.status_code == 422  # Expecting a validation error due to missing features

def test_valid_transaction():

    payload = {
        **{f"V{i}": 0.0 for i in range(1, 29)},  # Provide dummy values for V1 to V28
        "Amount": 100.0
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    result = response.json()

    assert "is_fraud" in result
    assert "fraud_probability" in result