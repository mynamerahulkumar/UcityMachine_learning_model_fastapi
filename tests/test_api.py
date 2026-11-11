"""API tests for the Census income service.

The two salary payloads were checked against the saved model on the
held-out test split before they were copied here.
"""

import pytest
from fastapi.testclient import TestClient

from main import app

LOW_INCOME = {
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

HIGH_INCOME = {
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


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_get_welcome(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Welcome to the Census Income Prediction API"


def test_get_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_post_predicts_low_income(client):
    response = client.post("/model", json=LOW_INCOME)
    assert response.status_code == 200
    assert response.json()["prediction"] == "<=50K"


def test_post_predicts_high_income(client):
    response = client.post("/model", json=HIGH_INCOME)
    assert response.status_code == 200
    assert response.json()["prediction"] == ">50K"


def test_post_rejects_missing_field(client):
    payload = dict(LOW_INCOME)
    del payload["age"]
    response = client.post("/model", json=payload)
    assert response.status_code == 422
    assert "detail" in response.json()


def test_post_rejects_invalid_age_type(client):
    payload = dict(LOW_INCOME)
    payload["age"] = "thirty"
    response = client.post("/model", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"]


def test_post_unknown_workclass_still_predicts(client):
    payload = dict(LOW_INCOME)
    payload["workclass"] = "Not-A-Real-Class"
    response = client.post("/model", json=payload)
    assert response.status_code == 200
    assert response.json()["prediction"] in {"<=50K", ">50K"}
