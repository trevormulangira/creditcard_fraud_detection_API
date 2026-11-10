from pydantic import BaseModel, create_model, ConfigDict
from datetime import datetime
#How FastAPI receives the data
#Define our expected data type of the input i.e. a schema
TransactionSchema = create_model(
    "TransactionSchema", 
    **{
        **{f"V{i}": (float, ...) for i in range (1, 29)},
          "Amount": (float, ...),  # Create fields V1 to V28 as float
    }
)

#Response Schema
class TransactionResponse(BaseModel):
    id: int
    amount: float
    prediction: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  # Enable attribute access for the response model

#Update Schema
class TransactionUpdate(BaseModel):
    amount: float
