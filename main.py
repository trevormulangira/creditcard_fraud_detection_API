from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, Depends  
import joblib
import pandas as pd
import logging
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import Transaction as DBTransaction
from schemas import TransactionSchema, TransactionResponse, TransactionUpdate
Base.metadata.create_all(bind=engine)  # Create the database tables if they don't exist

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

@app.post("/predict", summary="Predict Fraud")
def predict(transaction: TransactionSchema, request: Request, db: Session = Depends(get_db)): # type: ignore

    logger.info("Prediction request received")

    try:
        pipeline = request.app.state.pipeline  # Access the loaded model pipeline from the app state
        data = transaction.model_dump()  # Convert the Pydantic model to a dictionary
        df = pd.DataFrame([data])  # Convert the dictionary to a DataFrame

        if transaction.Amount < 0:
            raise HTTPException(status_code=400, detail="Amount must be non-negative")  # Raise an error if the amount is negative

        prediction = pipeline.predict(df)[0]  # Make prediction using the loaded model

        probability = pipeline.predict_proba(df)[0][1]  # Get the probability of the positive
        
        new_transaction = DBTransaction(
            amount=transaction.Amount,
            prediction=int(prediction))
        db.add(new_transaction)  # Add the new transaction to the database session
        db.commit()  # Commit the transaction to the database
        db.refresh(new_transaction)  # Refresh the instance to get the updated data from the database

        logger.info("Prediction completed successfully")
        
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of an error
        logger.exception("Prediction failed"
                         )
        raise HTTPException(status_code=500, 
                            detail="Error occurred while making prediction"
        )  # Raise an error if prediction fails
    
    return {
        "is_fraud": bool(prediction),
        "fraud_probability": float(probability)
     }

@app.get("/transactions", response_model=list[TransactionResponse])
def get_transactions(db: Session = Depends(get_db)):  # type: ignore
    transactions = db.query(DBTransaction).order_by(DBTransaction.id.desc()).all()  # Query all transactions from the database
    return transactions  # Return the list of transactions

@app.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):  # type: ignore
    transaction = db.query(DBTransaction).filter(DBTransaction.id == transaction_id).first()  # Query the transaction by ID
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")  # Raise an error if the transaction is not found
    return transaction  # Return the transaction

@app.put("/transactions/{transaction_id}", response_model=TransactionResponse)
def update_transaction(transaction_id: int, update_data: TransactionUpdate, db: Session = Depends(get_db)):
    transaction = db.query(DBTransaction).filter(DBTransaction.id == transaction_id).first()  # Query the transaction by ID
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")  # Raise an error if the transaction is not found 

    transaction.amount = update_data.amount

    db.commit()
    db.refresh(transaction)  # Refresh the instance to get the updated data from the database

    return transaction

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(DBTransaction).filter(DBTransaction.id == transaction_id).first()  # Query the transaction by ID
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")  # Raise an error if the transaction is not found

    db.delete(transaction)
    db.commit()

    return {"message": "Transaction deleted successfully"}

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