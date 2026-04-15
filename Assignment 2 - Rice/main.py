from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from pycaret.classification import load_model, predict_model

app = FastAPI()

model = load_model("best_pipeline")


class RiceInput(BaseModel):
    Area: float
    Perimeter: float
    Major_Axis_Length: float
    Minor_Axis_Length: float
    Eccentricity: float
    Convex_Area: float
    Extent: float


@app.get("/")
def home():
    return {"message": "Rice classification API is running."}


@app.post("/predict")
def predict(data: RiceInput):
    input_df = pd.DataFrame([data.dict()])
    prediction = predict_model(model, data=input_df)

    return {
        "prediction": prediction["prediction_label"][0]
    }