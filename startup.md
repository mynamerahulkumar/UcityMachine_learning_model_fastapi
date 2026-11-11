# Startup and rubric check

Run every command from this directory. It is the Git root for https://github.com/mynamerahulkumar/UcityMachine_learning_model_fastapi.git.

[architecture.md](architecture.md) explains the training path, the request path, and the code. This file is the checklist. Copy the commands in order on a clean machine. Sections 1–5 stay on this machine. Sections 6–9 are the first commit, the Render service, the four live screenshots, and the second push. The "Evidence" column is what this directory produced on 11 November 2026 with Python 3.13.13. Cloud rows stay pending until you push and create the Render service.

`python3` on the development Mac is 3.14.6. Use `python3.13`.

## 1. Environment

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

`pip install -e .` can warn when Git has no commits. The `starter` package still imports.

Evidence: a new `.venv` on Python 3.13.13 installed `requirements.txt` and the editable `starter` package. `aequitas==0.42.0` and `Flask==0.12.2` installed. They are not on the training or API path.

## 2. Saved model

Do not retrain if `model/model.pkl` is already present. The API tests are locked to its predictions.

```bash
python - <<'PY'
import json
from pathlib import Path
from starter.ml.model import load_model

artifact = load_model(Path("model/model.pkl"))
metrics = json.loads(Path("model/metrics.json").read_text())
print(artifact["algorithm"])
print(metrics["training_samples"], metrics["test_samples"])
print(metrics["selected"])
PY
```

Expected output:

```text
RandomForestClassifier
24129 6033
{'accuracy': 0.8496602022211172, 'precision': 0.730799069045772, 'recall': 0.6271637816245007, 'f1': 0.675026872088857}
```

That is what a fresh process printed on 11 November 2026. The artifact keys are `algorithm`, `categorical_features`, `encoder`, `feature_columns`, `lb`, and `model`.

Train only when the file is missing:

```bash
python starter/train_model.py
```

That command also rewrites `model/metrics.json` and `slice_output.txt`. After a retrain, confirm the two POST examples in [architecture.md](architecture.md) still return `<=50K` and `>50K` before you trust `tests/test_api.py`.

## 3. Local API

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

In a second terminal:

```bash
curl -sS -D - http://127.0.0.1:8000/
echo
curl -sS -D - http://127.0.0.1:8000/health
echo
curl -sS -D - http://127.0.0.1:8000/model \
  -H 'Content-Type: application/json' \
  -d '{"age":27,"workclass":"Private","fnlgt":245661,"education":"HS-grad","education-num":9,"marital-status":"Separated","occupation":"Machine-op-inspct","relationship":"Own-child","race":"White","sex":"Female","capital-gain":0,"capital-loss":0,"hours-per-week":40,"native-country":"United-States"}'
echo
curl -sS -D - http://127.0.0.1:8000/model \
  -H 'Content-Type: application/json' \
  -d '{"age":47,"workclass":"Private","fnlgt":162034,"education":"Bachelors","education-num":13,"marital-status":"Married-civ-spouse","occupation":"Sales","relationship":"Husband","race":"White","sex":"Male","capital-gain":0,"capital-loss":0,"hours-per-week":70,"native-country":"United-States"}'
echo
```

Evidence from the running server on 11 November 2026:

| Call | Result |
|---|---|
| `GET /` | HTTP 200, `{"message":"Welcome to the Census Income Prediction API"}` |
| `GET /health` | HTTP 200, `{"status":"ok"}` |
| Low-income `POST /model` | HTTP 200, `{"prediction":"<=50K"}` |
| High-income `POST /model` | HTTP 200, `{"prediction":">50K"}` |
| Same body with `age` removed | HTTP 422, `detail` loc `body.age` |

Open http://127.0.0.1:8000/docs and expand `POST /model`. The schema required names include `education-num`, `marital-status`, `capital-gain`, `capital-loss`, `hours-per-week`, and `native-country`. Both example bodies are in the OpenAPI schema.

`screenshots/example.png` is already that page, captured on 11 November 2026. Retake it only when the file is missing. Leave uvicorn running, open the docs URL, and expand `POST /model` until the example body is on screen. On a Mac, press Shift+Command+4, then Space, then click the browser window. macOS saves the picture on the Desktop. Move it into this folder and name it `screenshots/example.png`. The address bar must show `127.0.0.1:8000/docs`, and the example body must show the hyphenated field names.

Stop the server with Ctrl-C when you are done.

## 4. Tests, lint, and the sanity check

```bash
pytest -v
flake8 .
printf 'tests/test_api.py\n' | python sanitycheck.py
```

Evidence:

- `pytest -v`: `11 passed, 1 warning in 35.58s`. Failed: 0. Tests are the seven functions in `tests/test_api.py` and the four functions in `tests/test_model.py`.
- `flake8 .`: exit 0, no findings. Config is `.flake8`.
- `sanitycheck.py`: `Your test cases look good!` and exit 0. The script reads the test path from stdin. It ignores a directory passed as an argument.

## 5. Slice file and model card

```bash
test -f slice_output.txt && test -f model_card.md && test -f model/metrics.json && test -f screenshots/example.png && echo "artifacts present"
grep '^HS-grad' slice_output.txt
grep '^Bachelors' slice_output.txt
```

`HS-grad | 2023 | 0.8601 | 0.6095 | 0.3891 | 0.4750` and `Bachelors | 1010 | 0.7960 | 0.7547 | 0.7583 | 0.7565` are calculated rows, not typed examples. `model_card.md` uses the same test metrics. A `small_sample` row is fewer than 30 test rows. It is not a fairness result.

## 6. First commit and push

`.gitignore` ignores `*.pkl`, other generated model files, `*.csv` except `data/census.csv`, screenshot images, `.venv`, caches, and secrets. A plain `git add` therefore skips the model and every PNG. `git add -f` stages one ignored file anyway. Force-add only the two files below. Do not `git add -f model/`.

```bash
git add -f model/model.pkl
git add -f screenshots/example.png
git add .
git status
```

`git add .` stages the source, tests, workflow, and docs. It still skips `.venv`, caches, and any PNG you have not force-added. Before you commit, `git status` must list `model/model.pkl`, `screenshots/example.png`, `main.py`, `tests/`, `.github/workflows/ci.yml`, `README.md`, `DEPLOYMENT.md`, `architecture.md`, and this file. It must not list `.venv` or a deploy-hook URL.

```bash
git commit -m "$(cat <<'EOF'
Add the census income API, saved model, and CI workflow.

EOF
)"
git push -u origin main
```

`model/model.pkl` is about 66 MB. GitHub warns above 50 MB and accepts this file. GitHub rejects a file above 100 MB.

This pass did not commit or push. `main` still has no commits. On disk, `model/model.pkl` and `screenshots/example.png` are already staged from the two `git add -f` commands. The remote is already:

```text
origin  https://github.com/mynamerahulkumar/UcityMachine_learning_model_fastapi.git
```

The first push starts GitHub Actions. `pytest-and-flake8` can pass. `render-deploy` fails until the secret in section 7 exists. That failure is expected. Add the secret, then push again.

## 7. GitHub Actions and Render

After you push `main`, GitHub runs `.github/workflows/ci.yml`.

- Job `pytest-and-flake8` installs this requirements file on Python 3.13, then runs `pytest -v` and `flake8 .`. It runs on pushes and on pull requests to `main`.
- Job `render-deploy` has `needs` that test job. It runs only on a push to `main`. It POSTs the secret `RENDER_DEPLOY_HOOK_URL` and does not print the URL. A failed test or lint job does not start it.

Create the service from [DEPLOYMENT.md](DEPLOYMENT.md). The short path is:

1. Sign in at https://render.com and connect GitHub. Grant Render access to `mynamerahulkumar/UcityMachine_learning_model_fastapi` only. Connect this repository, not a parent folder.
2. Render dashboard → **New → Blueprint**. Select that repository and apply `render.yaml`.
3. Build command: `pip install -r requirements.txt && pip install -e .`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Environment variable `PYTHON_VERSION` = `3.13.13`. If Render lacks that patch, use the newest 3.13 it offers.
6. Service **Settings** → set **Auto-Deploy** to **No**. `render.yaml` also sets `autoDeploy: false`.
7. **Settings → Deploy Hook → Create deploy hook**. Copy the URL once. It is a credential. Do not commit it.

Store the hook on GitHub:

1. Repository → **Settings → Secrets and variables → Actions**.
2. **New repository secret**.
3. Name: `RENDER_DEPLOY_HOOK_URL`.
4. Value: the hook URL from Render.

After Actions has run once, GitHub knows the check name `pytest-and-flake8`. Protect `main`:

1. **Settings → Branches → Add branch ruleset**, or a classic branch protection rule.
2. Branch name pattern: `main`.
3. Require a pull request before merging.
4. Require status checks to pass before merging, and select `pytest-and-flake8`.
5. Do not require `render-deploy`. That job does not run on pull requests.

These settings need admin rights on the GitHub repository.

Trigger the hook after the secret exists:

```bash
git commit --allow-empty -m "$(cat <<'EOF'
Trigger the gated Render deploy.

EOF
)"
git push
```

Open the repository **Actions** tab. Wait until `pytest-and-flake8` is green and `render-deploy` is green. On Render, wait until the service is **Live**, then copy the public URL. It looks like `https://something.onrender.com`. The first request can take about a minute while a free instance wakes up. There is no public URL yet, so the live command below was not run.

## 8. Capture the four live screenshots

Use the same Mac shortcut as section 3: Shift+Command+4, then Space, then click the window. Move each Desktop picture into `screenshots/` and rename it to the exact file name. The address bar or the terminal output must show the public Render host.

| File | What the picture must show |
|---|---|
| `screenshots/continuous_integration.png` | GitHub Actions run on `main` with a green `pytest-and-flake8` job. Open `https://github.com/mynamerahulkumar/UcityMachine_learning_model_fastapi/actions` and click that run. |
| `screenshots/continuous_deployment.png` | The same Actions run with a green `render-deploy` job, or the Render deploy that the hook started. |
| `screenshots/live_get.png` | A browser on `https://YOUR-SERVICE.onrender.com/` showing `{"message":"Welcome to the Census Income Prediction API"}`. The address bar must be the Render host. |
| `screenshots/live_post.png` | The terminal after the command below, including the public `/model` URL, the HTTP status, and `{"prediction":">50K"}`. |

Replace the host with the URL Render shows:

```bash
export API_URL=https://YOUR-SERVICE.onrender.com
python request_live.py
```

The script rejects `localhost` and `127.0.0.1`. It prints the URL it called, the HTTP status, and the JSON body. The payload is the `>50K` example from section 3.

If the Desktop names differ, move the real files:

```bash
mv ~/Desktop/continuous_integration.png screenshots/continuous_integration.png
mv ~/Desktop/continuous_deployment.png screenshots/continuous_deployment.png
mv ~/Desktop/live_get.png screenshots/live_get.png
mv ~/Desktop/live_post.png screenshots/live_post.png
```

## 9. Commit the live screenshots

`.gitignore` ignores the new PNGs too. Force-add the four files, check the status, then commit and push:

```bash
git add -f screenshots/continuous_integration.png
git add -f screenshots/continuous_deployment.png
git add -f screenshots/live_get.png
git add -f screenshots/live_post.png
git status
git commit -m "$(cat <<'EOF'
Add CI, deploy, and live API screenshots.

EOF
)"
git push
```

`git status` before that commit should list only those four PNGs. This push runs the tests again and asks Render to deploy again.

## Rubric checklist

| Rubric requirement | Status | Evidence |
|---|---|---|
| Git and CI setup | Pending | Section 6. `.github/workflows/ci.yml` is in this folder. Remote is set. `main` has no commits, so Actions has not run. |
| Six passing pytest tests | Complete | `11 passed, 1 warning in 35.58s` |
| Flake8 | Complete | `flake8 .` exit 0 |
| ML model | Complete | Fresh load of `model/model.pkl`: `RandomForestClassifier` |
| Model evaluation | Complete | `model/metrics.json` selected F1 0.6750, accuracy 0.8497, precision 0.7308, recall 0.6272 |
| Slice evaluation | Complete | `slice_output.txt`, including `HS-grad` and `Bachelors` |
| Model card | Complete | `model_card.md` |
| FastAPI | Complete | Local `GET /` 200 and both `POST /model` labels |
| Pydantic examples | Complete | OpenAPI required names use hyphens. `screenshots/example.png` |
| API tests | Complete | Seven tests in `tests/test_api.py`, including both salary labels and HTTP 422 |
| Cloud deployment | Pending | Section 7. No Render service and no live URL |
| Continuous deployment | Pending | Section 7, then `screenshots/continuous_deployment.png` in section 8. `render-deploy` has not been executed |
| Live GET | Pending | Section 8. `screenshots/live_get.png` does not exist |
| Live POST | Pending | Section 8. `screenshots/live_post.png` does not exist |
| Model artifacts submitted | Pending | Section 6. `model/model.pkl` is on disk and staged. It is not committed |
| Repository documentation | Complete | `README.md`, `DEPLOYMENT.md`, `architecture.md`, `startup.md`. GitHub URL is the remote above |
