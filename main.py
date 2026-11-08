from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel, create_model  
import joblib
import pandas as pd
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
#IMPLEMENT LIFESPAN

MODEL_PATH = Path(__file__).resolve().parent / "tuned_random_forest_v1.joblib"
@asynccontextmanager
async def lifespan(app: FastAPI):
    
    app.state.pipeline = joblib.load(MODEL_PATH)

    print("Fraud detection model loaded successfully")
    yield

    del app.state.pipeline

    print("Application shutting down")

app = FastAPI(lifespan=lifespan)

#How FastAPI receives the data
#Define our expected data type of the input i.e. a schema
TransactionSchema = create_model(
    "TransactionSchema", 
    **{
        **{f"V{i}": (float, ...) for i in range (1, 29)},
          "Amount": (float, ...),  # Create fields V1 to V28 as float
    }
)

@app.post("/predict", summary="Predict Fraud")
def predict(transaction: TransactionSchema, request: Request): # type: ignore

    logger.info("Prediction request received")

    try:
        pipeline = request.app.state.pipeline  # Access the loaded model pipeline from the app state
        data = transaction.model_dump()  # Convert the Pydantic model to a dictionary
        df = pd.DataFrame([data])  # Convert the dictionary to a DataFrame

        if transaction.Amount < 0:
            raise HTTPException(status_code=400, detail="Amount must be non-negative")  # Raise an error if the amount is negative

        prediction = pipeline.predict(df)[0]  # Make prediction using the loaded model

        probability = pipeline.predict_proba(df)[0][1]  # Get the probability of the positive class

        logger.info("Prediction completed successfully")
        
    except Exception as e:
        logger.exception("Prediction failed"
                         )
        raise HTTPException(status_code=500, 
                            detail="Error occurred while making prediction"
        )  # Raise an error if prediction fails
    
    return {
        "is_fraud": bool(prediction),
        "fraud_probability": float(probability)
     }

#BUILD HEALTH CHECKPOINT
@app.get("/")
def health(request: Request):

    pipeline = getattr(request.app.state, "pipeline", None)

    if pipeline is None:
        return {
            "status": "unhealthy",
            "model_loaded": False
        }

    return {
        "status": "healthy",
        "model_loaded": True
    }