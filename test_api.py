import requests

#PREDICT
url = "http://127.0.0.1:8000"

def test_predict_transaction():
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

    response = requests.post(f"{url}/predict", json=data)

    print("Status:", response.status_code)
    print("Response:", response.json())

#PUT
def test_put_transaction():

    data = {
        "amount": 500.0}  # New amount value

    response = requests.put(f"{url}/transactions/6", json=data)

    print(response.status_code)
    print(response.json())

def test_delete_transaction():
    response = requests.delete(f"{url}/transactions/6")  # Replace with the actual transaction ID you want to delete

    print(response.status_code)
    print(response.text)

test_delete_transaction()