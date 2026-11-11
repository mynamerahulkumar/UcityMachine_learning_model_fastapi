"""Census income prediction API."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from starter.ml.data import process_data
from starter.ml.model import inference, load_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_PATH = Path(__file__).resolve().parent / "model" / "model.pkl"
ARTIFACT = {}

# Payloads verified against model/model.pkl on the held-out test split.
EXAMPLE_LOW_INCOME = {
    "age": 27,
    "workclass": "Private",
    "fnlgt": 245661,
    "education": "HS-grad",
    "education-num": 9,
    "marital-status": "Separated",
    "occupation": "Machine-op-inspct",
    "relationship": "Own-child",
    "race": "White",
    "sex": "Female",
    "capital-gain": 0,
    "capital-loss": 0,
    "hours-per-week": 40,
    "native-country": "United-States",
}
EXAMPLE_HIGH_INCOME = {
    "age": 47,
    "workclass": "Private",
    "fnlgt": 162034,
    "education": "Bachelors",
    "education-num": 13,
    "marital-status": "Married-civ-spouse",
    "occupation": "Sales",
    "relationship": "Husband",
    "race": "White",
    "sex": "Male",
    "capital-gain": 0,
    "capital-loss": 0,
    "hours-per-week": 70,
    "native-country": "United-States",
}


class CensusInput(BaseModel):
    """One Census row. Aliases keep the hyphenated CSV column names."""

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "examples": [EXAMPLE_LOW_INCOME, EXAMPLE_HIGH_INCOME]
        },
    )

    age: int = Field(examples=[27])
    workclass: str = Field(examples=["Private"])
    fnlgt: int = Field(examples=[245661])
    education: str = Field(examples=["HS-grad"])
    education_num: int = Field(alias="education-num", examples=[9])
    marital_status: str = Field(
        alias="marital-status",
        examples=["Separated"],
    )
    occupation: str = Field(examples=["Machine-op-inspct"])
    relationship: str = Field(examples=["Own-child"])
    race: str = Field(examples=["White"])
    sex: str = Field(examples=["Female"])
    capital_gain: int = Field(alias="capital-gain", examples=[0])
    capital_loss: int = Field(alias="capital-loss", examples=[0])
    hours_per_week: int = Field(alias="hours-per-week", examples=[40])
    native_country: str = Field(
        alias="native-country",
        examples=["United-States"],
    )


class WelcomeResponse(BaseModel):
    """Response body for the welcome route."""

    message: str


class PredictionResponse(BaseModel):
    """Response body for a salary prediction."""

    prediction: str


class HealthResponse(BaseModel):
    """Response body for the health route."""

    status: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the saved model once when the application starts."""
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"Model artifact not found at {MODEL_PATH}. "
            "Train it with: python starter/train_model.py"
        )
    ARTIFACT["data"] = load_model(MODEL_PATH)
    logger.info("Loaded model from %s", MODEL_PATH)
    yield
    ARTIFACT.clear()


app = FastAPI(
    title="Census Income Prediction API",
    description=(
        "Predict whether Census income is <=50K or >50K. "
        "Request fields use the original CSV column names."
    ),
    lifespan=lifespan,
)


@app.get("/", response_model=WelcomeResponse)
def welcome() -> WelcomeResponse:
    """Return a short welcome message."""
    return WelcomeResponse(
        message="Welcome to the Census Income Prediction API"
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Report whether the model artifact is loaded."""
    if "data" not in ARTIFACT:
        raise HTTPException(status_code=503, detail="Model is not loaded.")
    return HealthResponse(status="ok")


@app.post("/model", response_model=PredictionResponse)
def predict(payload: CensusInput) -> PredictionResponse:
    """Predict the salary class for one Census record."""
    if "data" not in ARTIFACT:
        raise HTTPException(status_code=503, detail="Model is not loaded.")

    artifact = ARTIFACT["data"]
    row = payload.model_dump(by_alias=True)
    frame = pd.DataFrame([row], columns=artifact["feature_columns"])
    try:
        features, _, _, _ = process_data(
            frame,
            categorical_features=artifact["categorical_features"],
            label=None,
            training=False,
            encoder=artifact["encoder"],
            lb=artifact["lb"],
        )
        predictions = inference(artifact["model"], features)
        label = artifact["lb"].inverse_transform(predictions)[0]
    except Exception as exc:
        logger.exception("Inference failed")
        raise HTTPException(
            status_code=400,
            detail="Unable to run inference on the provided input.",
        ) from exc

    prediction = str(label)
    logger.info("Prediction: %s", prediction)
    return PredictionResponse(prediction=prediction)
