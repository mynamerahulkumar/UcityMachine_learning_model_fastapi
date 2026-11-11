"""POST one Census record to the deployed income API."""

import os
import sys

import requests

API_URL = os.getenv("API_URL")

if not API_URL:
    raise ValueError("API_URL environment variable is required")

normalized = API_URL.lower()
if "localhost" in normalized or "127.0.0.1" in normalized:
    raise ValueError(
        "API_URL must be the deployed Render URL, not localhost."
    )

# Held-out test row. The local model predicts >50K for this payload.
payload = {
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

url = f"{API_URL.rstrip('/')}/model"
print(f"Request URL: {url}")

try:
    response = requests.post(url, json=payload, timeout=30)
except requests.ConnectionError as exc:
    print(f"Connection failed: {exc}")
    sys.exit(1)
except requests.Timeout:
    print("Request timed out.")
    sys.exit(1)

print("HTTP Status:", response.status_code)
try:
    body = response.json()
except ValueError:
    print("Response was not JSON:", response.text)
    sys.exit(1)

print("Inference Result:", body)
try:
    response.raise_for_status()
except requests.HTTPError as exc:
    print(f"HTTP error: {exc}")
    sys.exit(1)
