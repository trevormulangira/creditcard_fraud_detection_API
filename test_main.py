from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_health():
    response = client.get("/")
    assert response.status_code == 200

def test_predict():
    with TestClient(app) as client:
            data = {
                
                "V1": 2.115519,
                "V2": -0.69181,
                "V3": -1.30551,
                "V4": -0.68566,
                "V5": -0.64126,
                "V6": -0.76478,
                "V7": -0.92426,
                "V8": -0.02303,
                "V9": -0.23013,
                "V10": 0.22061,
                "V11": 1.058325,
                "V12": -0.72336,
                "V13": -0.61924,
                "V14": -2.24371,
                "V15": -0.27143,
                "V16": 2.007845,
                "V17": 1.213534,
                "V18": 0.282344,
                "V19": 0.579121,
                "V20": 0.067367,
                "V21": 0.241708,
                "V22": 0.682524,
                "V23": 0.037769,
                "V24": -0.54686,
                "V25": -0.12306,
                "V26": -0.08489,
                "V27": 0.00472,
                "V28": -0.02194,
                "Amount": 29.95

            }

            response = client.post("/predict", json=data)
            assert response.status_code == 200

            result = response.json()

            assert "is_fraud" in result
            assert "fraud_probability" in result

def test_get_transactions():
    response = client.get("/transactions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_transaction():
     transactions = client.get("/transactions").json()  # Replace with a valid transaction ID
     assert len(transactions) > 0, "No transactions found to test."
     transaction_id = transactions[0]["id"]  # Get the ID of the first transaction

     response = client.get(f"/transactions/{transaction_id}")
     assert response.status_code == 200
     assert response.json()["id"] == transaction_id

def test_update_transaction():
    transactions = client.get("/transactions").json()  # Replace with a valid transaction ID
    assert len(transactions) > 0, "No transactions found to test."
    transaction_id = transactions[0]["id"]  # Get the ID of the first transaction

    update_data = {
        "amount": 500.0
    }

    response = client.put(f"/transactions/{transaction_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["amount"] == update_data["amount"]

def test_delete_transaction():
    transactions = client.get("/transactions").json()  # Replace with a valid transaction ID
    assert len(transactions) > 0, "No transactions found to test."
    transaction_id = transactions[0]["id"]  # Get the ID of the first transaction

    response = client.delete(f"/transactions/{transaction_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction deleted successfully"