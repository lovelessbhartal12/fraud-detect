from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from fastapi.responses import JSONResponse
import pickle
import pandas as pd

model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
pca = pickle.load(open('pca.pkl', 'rb'))
features = pickle.load(open('features.pkl', 'rb'))

app = FastAPI()

class ClaimData(BaseModel):
    AddressChange_Claim: Annotated[int, Field(..., description="Address change during claim")]
    BasePolicy: int
    VehiclePrice: float
    Deductible: float
    Fault: int
    PolicyNumber: float
    PastNumberOfClaims: float
@app.get("/about")
def about():
    return 
{"message":"THIS IS THE FRAUD DETECTION"
 ,"version":"1.0.0","description":"A simple API for detecting fraudulent claims"}


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
