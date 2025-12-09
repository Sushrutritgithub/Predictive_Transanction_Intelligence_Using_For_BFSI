from fastapi import FastAPI
import joblib
from pydantic import BaseModel
from src.preprocessing.Preprocessing1 import preprocess_input
import json
import numpy as np

app = FastAPI(title="Fraud Detection API")

model = joblib.load("src/models/fraud_model.pkl")
feature_order = joblib.load("src/models/model_features.pkl")


try:
    with open("metrics.json", "r") as f:
        saved_metrics = json.load(f)
except:
    saved_metrics = {}

class Transaction(BaseModel):
    amount: float
    sender_old_balance: float
    sender_new_balance: float
    receiver_old_balance: float
    receiver_new_balance: float
    is_flagged: int
    transaction_type: str  


@app.get("/")
def root():
    return {"message": "Fraud Detection API Running"}


@app.post("/predict")
def predict_transaction(txn: Transaction):
    
    
    data = txn.dict()

   
    X = preprocess_input(data, feature_order)

    
    prob = model.predict_proba(X)[0][1]

    
    threshold = 0.10
    pred = int(prob > threshold)

    # Optional: Save prediction to DB
    # from src.database.mysql_connection import save_prediction
    # save_prediction(data, prob, pred)

    return {
        "fraud_probability": float(prob),
        "is_fraud": pred
    }


@app.get("/metrics")
def get_metrics():
    return saved_metrics
