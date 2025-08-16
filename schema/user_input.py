from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from fastapi.responses import JSONResponse
import pickle
import pandas as pd

model_version = "1.0.0"
app = FastAPI()

class ClaimData(BaseModel):
    AddressChange_Claim: Annotated[int, Field(..., description="Address change during claim")]
    BasePolicy: int
    VehiclePrice: float
    Deductible: float
    Fault: int
    PolicyNumber: float
    PastNumberOfClaims: float