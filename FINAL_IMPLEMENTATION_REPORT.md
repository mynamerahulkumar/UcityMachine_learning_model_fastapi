# Final implementation report

Local install, model load, tests, lint, the sanity check, and live local HTTP calls were run in this directory on 11 November 2026. Python was 3.13.13. The model was not retrained. Cloud deployment was not run. No Git commit was created.

## A. Project implementation

Present in this working tree:

- In-memory cleaning in `starter/ml/data.py` (`clean_data`). The CSV was not edited.
- `train_model`, `inference`, `save_model`, `load_model`, metrics, and education slice scoring in `starter/ml/model.py`.
- `starter/train_model.py` trains a random forest and a scaled logistic regression, saves the better test F1, and writes `model/metrics.json` and `slice_output.txt`.
- `model/model.pkl` holds the forest, encoder, label binarizer, and column lists.
- `model_card.md` uses those measured results. `model_card_template.md` is unchanged.
- `main.py` serves `GET /`, `GET /health`, and `POST /model` with hyphenated Pydantic aliases.
- `tests/test_model.py` and `tests/test_api.py` (11 tests).
- `.gitignore`, `.flake8`, `.github/workflows/ci.yml`, `render.yaml`, `DEPLOYMENT.md`, `request_live.py`, `README.md`, `architecture.md`, `startup.md`, and `PROJECT_ANALYSIS.md`.
- `requirements.txt` pins `joblib==1.6.0` and `flake8==7.5.0`. `aequitas==0.42.0` and `Flask==0.12.2` installed on Python 3.13.13.
- `screenshots/example.png` is a capture of the local Swagger POST example.

`.gitignore`, `.flake8`, and `.github/workflows/ci.yml` were missing after the move into this repository. They were restored from the previous project copy. `model/metrics.json` records `model_path` as `model/model.pkl`.

## B. Machine learning results

Selected algorithm: `RandomForestClassifier` (`random_state=42`).

A fresh Python process loaded `model/model.pkl` and printed that algorithm name. The logistic regression baseline used a `StandardScaler` inside a pipeline on the same encoded matrix. Its test F1 was lower, so it was not saved.

| Item | Value |
|---|---|
| Rows in `data/census.csv` | 32561 |
| Rows after dropping `?` | 30162 |
| Training samples | 24129 |
| Test samples | 6033 |
| Positive class | `>50K` |
| Accuracy | 0.8497 |
| Precision | 0.7308 |
| Recall | 0.6272 |
| F1 | 0.6750 |

Logistic regression on the same test rows: accuracy 0.8472, precision 0.7339, recall 0.6059, F1 0.6637.

Source: `model/metrics.json`. Full-precision selected values printed by the load check: accuracy 0.8496602022211172, precision 0.730799069045772, recall 0.6271637816245007, F1 0.675026872088857. The four-decimal figures match `model_card.md`.

## C. Slice evaluation

`slice_output.txt` scores `education` on the 6,033 test rows.

- `HS-grad` (2,023 rows) has F1 0.4750 and recall 0.3891. `Bachelors` (1,010 rows) has F1 0.7565.
- `1st-4th` has 27 rows and is marked `small_sample`. Its precision, recall, and F1 are 1.0000 because `zero_division=1` and the slice has no positive labels.

Slice scores were not used to claim the model is fair.

## D. API verification

Local `uvicorn main:app --host 127.0.0.1 --port 8000` on 11 November 2026:

- `GET /` returned HTTP 200 and `{"message":"Welcome to the Census Income Prediction API"}`.
- `GET /health` returned HTTP 200 and `{"status":"ok"}`.
- `POST /model` with the low-income payload returned HTTP 200 and `{"prediction":"<=50K"}`.
- `POST /model` with the high-income payload returned HTTP 200 and `{"prediction":">50K"}`.
- `POST /model` with `age` removed returned HTTP 422 and a `detail` entry at `body.age`.
- `http://127.0.0.1:8000/openapi.json` lists the hyphenated required names and both Census examples.

`screenshots/example.png` is the earlier capture of Swagger at `/docs`. This pass confirmed the OpenAPI document. It did not replace the screenshot.

## E. Test results

Command: `.venv/bin/python -m pytest -v` on Python 3.13.13.

- Total pytest tests: 11
- Passed: 11
- Failed: 0

The session line was `11 passed, 1 warning in 35.58s`. The warning is a Starlette/AnyIO deprecation inside the test client.

`flake8 .` exited 0 with no findings.

`printf 'tests/test_api.py\n' | python sanitycheck.py` printed `Your test cases look good!` and exited 0.

## F. CI/CD

- Workflow file: `.github/workflows/ci.yml`.
- Job `pytest-and-flake8` runs on pushes and pull requests to `main`.
- Job `render-deploy` needs that job and runs only on a push to `main`. It POSTs `secrets.RENDER_DEPLOY_HOOK_URL` and does not echo the URL.
- `render.yaml` sets `autoDeploy: false` and the start command `uvicorn main:app --host 0.0.0.0 --port $PORT`.
- Remote: `https://github.com/mynamerahulkumar/UcityMachine_learning_model_fastapi.git`.
- GitHub has not executed the workflow. This folder has no commits. The Render secret is not configured. No deploy was observed.

## G. Submission evidence

Screenshots:

| File | State |
|---|---|
| `screenshots/example.png` | Present (PNG, captured from local `/docs`) |
| `screenshots/continuous_integration.png` | Missing |
| `screenshots/continuous_deployment.png` | Missing |
| `screenshots/live_get.png` | Missing |
| `screenshots/live_post.png` | Missing |

Model artifact: `model/model.pkl` is on disk and loaded in a fresh process. `.gitignore` ignores `*.pkl`. It is not in the Git index until you force-add it.

## H. Remaining manual steps

1. From this directory, commit and push `main`. Force-add the model and the Swagger screenshot:

```bash
git add -f model/model.pkl
git add -f screenshots/example.png
```

Do not `git add -f model/`. GitHub may warn because `model.pkl` is about 66 MB. The hard limit is 100 MB.

2. On GitHub, after the first Actions run, protect `main` and require the check `pytest-and-flake8`. Steps are in `DEPLOYMENT.md`.
3. Create the Render web service from `render.yaml`, set Auto-Deploy to No, create a deploy hook, and store it as the Actions secret `RENDER_DEPLOY_HOOK_URL`.
4. Confirm a green `pytest-and-flake8` run and a deploy that starts only after that run.
5. Capture the four missing screenshots from those real pages and from:

```bash
export API_URL=https://YOUR-SERVICE.onrender.com
python request_live.py
```

6. Force-add those four PNGs the same way as `screenshots/example.png`.

## I. Final rubric assessment

| Rubric requirement | Status | Evidence |
|---|---|---|
| Git and CI setup | Pending | `.github/workflows/ci.yml` is in the repo root. Actions has not run. `main` has no commits. |
| Six passing pytest tests | Complete | `11 passed, 1 warning in 35.58s` |
| Flake8 | Complete | `flake8 .` exited 0 |
| ML model | Complete | Fresh load of `model/model.pkl`, algorithm `RandomForestClassifier` |
| Model evaluation | Complete | `model/metrics.json`: accuracy 0.8497, precision 0.7308, recall 0.6272, F1 0.6750 |
| Slice evaluation | Complete | `slice_output.txt` |
| Model card | Complete | `model_card.md` |
| FastAPI | Complete | Local `GET /` and both `POST /model` responses in section D |
| Pydantic examples | Complete | OpenAPI examples and `screenshots/example.png` |
| API tests | Complete | Seven tests in `tests/test_api.py`, including both salary labels |
| Cloud deployment | Pending | No Render service and no live URL |
| Continuous deployment | Pending | Deploy job is in the workflow and has not been executed |
| Live GET | Pending | `screenshots/live_get.png` does not exist |
| Live POST | Pending | `screenshots/live_post.png` does not exist |
| Model artifacts submitted | Pending | `model/model.pkl` exists locally and is still ignored by Git |
| Repository documentation | Complete | `README.md`, `DEPLOYMENT.md`, `architecture.md`, `startup.md`. URL: https://github.com/mynamerahulkumar/UcityMachine_learning_model_fastapi.git |
