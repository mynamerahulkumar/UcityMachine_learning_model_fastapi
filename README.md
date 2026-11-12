# Census Income Prediction API

Predict whether Census income is `<=50K` or `>50K`, then serve that model with FastAPI.

The classifier is a scikit-learn random forest trained on `data/census.csv`. A scaled logistic regression baseline was trained on the same split and scored a lower test F1, so the forest is the model in `model/model.pkl`. On the 6,033-row test set the forest reached accuracy 0.8497, precision 0.7308, recall 0.6272, and F1 0.6750 for the positive class `>50K`. Those numbers are copied from `model/metrics.json`, which `starter/train_model.py` writes. They are not a target you should expect to beat by editing this file.

This repository has not been deployed. There is no public URL yet.

## Problem statement

The task is to classify the `salary` column of the US Census Income (Adult) extract. The two labels are `<=50K` and `>50K`. The finished project trains the model, writes slice metrics, documents the model, and exposes inference over HTTP.

## Dataset

`data/census.csv` has 32,561 rows. The label is `salary`. Features keep the file's column names, including hyphens and the weight column `fnlgt`.

Numeric features: `age`, `fnlgt`, `education-num`, `capital-gain`, `capital-loss`, `hours-per-week`.

Categorical features: `workclass`, `education`, `marital-status`, `occupation`, `relationship`, `race`, `sex`, `native-country`.

`?` marks missing values in `workclass`, `occupation`, and `native-country`. The raw file is not edited.

## Technology stack

- Python 3.13 (local virtualenv: 3.13.13)
- pandas and NumPy
- scikit-learn and joblib
- FastAPI, Pydantic v2, and Uvicorn
- pytest and Flake8
- GitHub Actions for CI and a gated Render deploy hook

## Project architecture

Training cleans the CSV in memory, splits 80/20 with `random_state=42` and stratification, one-hot encodes categorical columns, and binarizes `salary`. The saved joblib file contains the fitted model, encoder, label binarizer, and column lists. `POST /model` builds a one-row dataframe with the original column names, runs that same preprocessing with `training=False`, and maps the prediction back to `<=50K` or `>50K`.

## Repository structure

```text
.
├── .github/workflows/ci.yml
├── data/census.csv
├── model/model.pkl
├── model/metrics.json
├── screenshots/example.png
├── starter/ml/data.py
├── starter/ml/model.py
├── starter/train_model.py
├── tests/test_api.py
├── tests/test_model.py
├── main.py
├── request_live.py
├── slice_output.txt
├── model_card.md
├── model_card_template.md
├── DEPLOYMENT.md
├── render.yaml
└── requirements.txt
```

Run every command below from this directory. It is the Git repository root. The GitHub repository is https://github.com/mynamerahulkumar/UcityMachine_learning_model_fastapi.git.

## Python environment setup

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Use Python 3.13. On this machine `python3` is 3.14, which is not the version this project pins.

## Dependency installation

```bash
pip install -r requirements.txt
pip install -e .
```

`pip install -e .` can warn if Git has no commits yet. The `starter` package still imports when that warning appears.

## Data cleaning

`clean_data` in `starter/ml/data.py` strips string fields and drops rows where a categorical value is `?`. That removes 2,399 rows and leaves 30,162. Training calls it after `read_csv(..., skipinitialspace=True)`. `data/census.csv` stays as it was shipped.

## Model training

```bash
python starter/train_model.py
```

The script compares a random forest with a logistic regression pipeline that scales the encoded matrix. It saves the higher test F1 to `model/model.pkl` and writes `model/metrics.json`. The current winner is `RandomForestClassifier`.

## Model evaluation

Overall test metrics are printed by the training script and stored under `selected` in `model/metrics.json`. The narrative, including limits of the accuracy number, is in `model_card.md`.

## Model slice evaluation

The same training run scores every `education` value on the test split and writes `slice_output.txt`. Precision, recall, and F1 use the positive class `>50K`. `zero_division=1` fills a metric when a slice has no positive labels or no positive predictions. Slices with fewer than 30 rows are marked `small_sample`. Read `model_card.md` before treating a 1.0000 in that file as a real perfect score.

## Running FastAPI locally

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

- `GET http://127.0.0.1:8000/` returns the welcome message.
- `POST http://127.0.0.1:8000/model` expects the 14 Census fields. Hyphenated names are Pydantic aliases, so the JSON uses `education-num`, `marital-status`, `capital-gain`, `capital-loss`, `hours-per-week`, and `native-country`.
- `GET http://127.0.0.1:8000/health` reports that the artifact loaded.

The process exits at startup if `model/model.pkl` is missing.

## Swagger documentation

Open `http://127.0.0.1:8000/docs`. Expand `POST /model`. The Example Value is a full Census body using the CSV field names. `screenshots/example.png` is a capture of that page from the local server.

## Running unit tests

```bash
pytest -v
```

On 11 November 2026, `pytest -v` in this directory reported `11 passed, 1 warning in 35.58s`: four model tests and seven API tests. The warning is a Starlette/AnyIO deprecation inside the test client. The two salary tests use rows that this saved model actually scores as `<=50K` and `>50K`. Re-training with a different seed will break those tests until the payloads are checked again.

## Running Flake8

```bash
flake8 .
```

Configuration is in `.flake8`. It excludes `.venv` and caches and sets the line length to 88. The 11 November 2026 run in this directory exited 0 with no findings.

## Running sanitycheck.py

The checker asks for a path on stdin. It does not use its command-line directory argument.

```bash
printf 'tests/test_api.py\n' | python sanitycheck.py
```

The 11 November 2026 run printed `Your test cases look good!` and exited 0.

## GitHub Actions CI

`.github/workflows/ci.yml` runs on pushes and pull requests to `main`. The job `pytest-and-flake8` installs this requirements file on Python 3.13, then runs `pytest -v` and `flake8 .`. The repository is https://github.com/mynamerahulkumar/UcityMachine_learning_model_fastapi.git.

`model/model.pkl` is required for the tests. `.gitignore` ignores `*.pkl`, so stage it explicitly before the first push:

```bash
git add -f model/model.pkl
```

## Render deployment

`DEPLOYMENT.md` is the setup guide. `render.yaml` defines a Python web service with auto-deploy turned off. The start command is:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Deployment from GitHub Actions happens only in the `render-deploy` job, which `needs` the test job and runs only for pushes to `main`. You must store the Render deploy hook as the Actions secret `RENDER_DEPLOY_HOOK_URL`. That has not been done, and no deploy has been verified.

## Live API testing

After the service is public:

```bash
export API_URL=https://YOUR-SERVICE.onrender.com
python request_live.py
```

The script prints the URL it called, the HTTP status, and the JSON prediction. It rejects a localhost URL and exits on connection failures and HTTP errors.

## Screenshot evidence

| File | Status |
|---|---|
| `screenshots/example.png` | Captured from local Swagger |
| `screenshots/continuous_integration.png` | Not captured. Needs a GitHub Actions run |
| `screenshots/continuous_deployment.png` | Not captured. Needs a successful hook deploy |
| `screenshots/live_get.png` | Not captured. Needs the public GET page |
| `screenshots/live_post.png` | Not captured. Needs `request_live.py` against Render |

`.gitignore` ignores PNG files in `screenshots/`. Stage the real files with `git add -f`.

## Model artifact details

`model/model.pkl` is one joblib object with:

- `model`: fitted `RandomForestClassifier`
- `encoder`: fitted `OneHotEncoder` (`handle_unknown="ignore"`)
- `lb`: fitted `LabelBinarizer`
- `categorical_features`
- `feature_columns`
- `algorithm`

The file is about 66 MB. GitHub warns above 50 MB and rejects files above 100 MB, so this file can be pushed, with a warning. Do not commit `.venv` or secrets.

## Known limitations

The positive class is the minority label, so accuracy overstates how often `>50K` is found. Test recall for that class is 0.6272. Error rates differ by education; `HS-grad` recall is much lower than `Bachelors`. `sex`, `race`, and `native-country` are model inputs and can reproduce historical inequality. Slice scores of 1.0000 on tiny or single-class groups are not proof of fairness. See `model_card.md`.

## GitHub repository URL

https://github.com/mynamerahulkumar/UcityMachine_learning_model_fastapi.git

The remote `origin` points at this repository. Use this URL for the submission. Do not use https://github.com/mynamerahulkumar/ucityproject-alls.git.

## Branch protection

After the first GitHub Actions run, protect `main` so merges require the check `pytest-and-flake8`. Steps are in `DEPLOYMENT.md`. Do not require the deploy job on pull requests. It does not run there.
