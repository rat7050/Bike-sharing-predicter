from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path


# ==========================================
# CREATE FASTAPI APP
# ==========================================

app = FastAPI(
    title="Bike Sharing Demand Prediction API",
    description="Bike rental prediction using multiple regression models",
    version="1.0.0"
)


# ==========================================
# LOAD MODELS
# ==========================================

MODEL_DIR = Path(__file__).resolve().parent / "models"

linear_model = joblib.load(
    MODEL_DIR / "multiple_linear_regression.pkl"
)

poly_model = joblib.load(
    MODEL_DIR / "polynomial_regression_degree2.pkl"
)

rf_model = joblib.load(
    MODEL_DIR / "random_forest_regression.pkl"
)


# ==========================================
# INPUT DATA
# ==========================================

class BikeData(BaseModel):

    season: int
    yr: int
    mnth: int
    holiday: int
    weekday: int
    workingday: int
    weathersit: int
    temp: float
    hum: float
    windspeed: float

    # Model selection
    # Options:
    # linear
    # polynomial
    # random_forest
    # all

    model: str = "random_forest"


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Bike Sharing Demand Prediction API",
        "status": "running"
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ==========================================
# PREDICTION
# ==========================================

@app.post("/predict")
def predict(data: BikeData):

    input_data = pd.DataFrame([{
        "season": data.season,
        "yr": data.yr,
        "mnth": data.mnth,
        "holiday": data.holiday,
        "weekday": data.weekday,
        "workingday": data.workingday,
        "weathersit": data.weathersit,
        "temp": data.temp,
        "hum": data.hum,
        "windspeed": data.windspeed
    }])

    # Convert model name to lowercase
    selected_model = data.model.lower()

    # ======================================
    # OPTION 1: SINGLE MODEL
    # ======================================

    if selected_model == "linear":

        prediction = linear_model.predict(
            input_data
        )[0]

        return {
            "model": "Multiple Linear Regression",
            "prediction": round(
                float(prediction), 2
            )
        }


    elif selected_model == "polynomial":

        prediction = poly_model.predict(
            input_data
        )[0]

        return {
            "model": "Polynomial Regression",
            "prediction": round(
                float(prediction), 2
            )
        }


    elif selected_model == "random_forest":

        prediction = rf_model.predict(
            input_data
        )[0]

        return {
            "model": "Random Forest Regression",
            "prediction": round(
                float(prediction), 2
            )
        }


    # ======================================
    # OPTION 2: ALL MODELS
    # ======================================

    elif selected_model == "all":

        linear_prediction = linear_model.predict(
            input_data
        )[0]

        polynomial_prediction = poly_model.predict(
            input_data
        )[0]

        random_forest_prediction = rf_model.predict(
            input_data
        )[0]

        return {

            "model": "All Models",

            "predictions": {

                "multiple_linear_regression": round(
                    float(linear_prediction), 2
                ),

                "polynomial_regression": round(
                    float(polynomial_prediction), 2
                ),

                "random_forest_regression": round(
                    float(random_forest_prediction), 2
                )
            },

            "best_model": "Random Forest Regression",

            "recommended_prediction": round(
                float(random_forest_prediction), 2
            )
        }


    # ======================================
    # INVALID MODEL
    # ======================================

    else:

        return {
            "error": "Invalid model selected",

            "available_models": [
                "linear",
                "polynomial",
                "random_forest",
                "all"
            ]
        }