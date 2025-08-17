from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
from schema.user_input import ClaimData
model = pickle.load(open('model/model.pkl', 'rb'))
scaler = pickle.load(open('model/scaler.pkl', 'rb'))
pca = pickle.load(open('model/pca.pkl', 'rb'))
features = pickle.load(open('model/features.pkl', 'rb'))

model_version = "1.0.0"
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["https://your-streamlit-app-url"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Fraud Detection API."}
@app.get("/health")
def health_check():
    return {"status": "ok",
            "version": model_version,
            "description": "Fraud Detection API is running.",
            "model_loaded": model is not None
            }

@app.post("/predict")
def predict(data: ClaimData):
    df = pd.DataFrame([data.dict()])
    
    # Ensure all features are present
    df_full = df.reindex(columns=features, fill_value=0)
    
    # Scale
    scaled = scaler.transform(df_full)
    
    # PCA
    transformed = pca.transform(scaled)
    
    # Predict
    prediction = model.predict(transformed)[0]
    
    return JSONResponse(status_code=200, content={"prediction": "Fraud" if prediction == 1 else "Not Fraud"})
