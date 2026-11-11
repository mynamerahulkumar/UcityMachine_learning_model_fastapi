# Render deployment

This API is prepared for Render as a Python web service. Nothing in this repository has been deployed. There is no live URL until you create the service.

The GitHub repository root is this project directory: `https://github.com/mynamerahulkumar/UcityMachine_learning_model_fastapi.git`. Connect that repository to Render. `main.py`, `requirements.txt`, and `.github/workflows/ci.yml` are at the top level. Do not connect the parent folder `ucityproject-alls`.

Continuous deployment is gated in `.github/workflows/ci.yml`. The `render-deploy` job runs only after `pytest-and-flake8` succeeds, and only on a push to `main`. It POSTs to the secret `RENDER_DEPLOY_HOOK_URL`. The workflow does not print that URL. Render auto-deploy must stay off, or a push can go live before the tests finish.

## 1. Render account

1. Open [https://render.com/](https://render.com/) and create an account.
2. Confirm the account can create a web service. The blueprint uses `plan: free`. If your account has no free web-service allowance, change `plan` in `render.yaml` to a paid plan before you apply the blueprint.

## 2. Connect GitHub

1. In the Render dashboard, open Account Settings and connect GitHub.
2. Grant Render access to the dedicated repository for this project.

Push this directory to that repository only after `model/model.pkl` is force-added. The API loads that file at startup and does not train on boot. `.gitignore` ignores `*.pkl`, so a normal `git add` skips it:

```bash
git add -f model/model.pkl
git add -f screenshots/example.png
```

Add the other four screenshots the same way after you capture them. Do not `git add -f model/`.

## 3. Create the web service

Use the blueprint in `render.yaml`, or create the service by hand with the same settings.

Blueprint:

1. Render dashboard → New → Blueprint.
2. Select the GitHub repository.
3. Apply `render.yaml`.

Manual service:

1. New → Web Service.
2. Select the same repository.
3. Language: Python.
4. Root directory: repository root (leave it empty).

## 4. Build command

```bash
pip install -r requirements.txt && pip install -e .
```

## 5. Start command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Render sets `PORT`. The process must listen on `0.0.0.0`.

## 6. Environment variables

| Key | Value |
|---|---|
| `PYTHON_VERSION` | `3.13.13` |

Local tests ran on Python 3.13.13. If Render does not offer that exact patch release, choose the newest 3.13 it does offer and use that same version in GitHub Actions.

Do not put the deploy hook, API keys, or other secrets in `render.yaml` or in the repository.

## 7. Model artifact

`model/model.pkl` must be in the deployed Git tree. It holds the random forest, the one-hot encoder, the label binarizer, the categorical column names, and the feature column order. Paths in the app are relative to `main.py`. There are no machine-specific absolute paths.

Startup fails with a clear error if the file is missing. The service does not retrain.

## 8. Deploy hook

Turn off Render's own auto-deploy so only the GitHub Actions job deploys:

1. Open the service → Settings.
2. Set Auto-Deploy to **No**. `render.yaml` also sets `autoDeploy: false`.
3. Settings → Deploy Hook → Create deploy hook.
4. Copy the hook URL once. It is a credential.

On GitHub:

1. Repository → Settings → Secrets and variables → Actions.
2. New repository secret.
3. Name: `RENDER_DEPLOY_HOOK_URL`.
4. Value: the hook URL from Render.

The next push to `main` runs tests and lint. If both pass, the deploy job POSTs to the hook and Render builds the service. A failed test or lint job does not start the deploy job.

## 9. Protect `main`

After the workflow has run once, GitHub knows the check name `pytest-and-flake8`.

1. GitHub repository → Settings → Branches → Add branch ruleset, or Add classic branch protection rule.
2. Branch name pattern: `main`.
3. Require a pull request before merging.
4. Require status checks to pass before merging.
5. Select the required check `pytest-and-flake8`.
6. Do not require `render-deploy` as a merge check. That job does not run on pull requests.

These settings need admin rights on the GitHub repository. This environment cannot change them.

## 10. Test the live endpoints

Replace the host below with the URL Render shows for the service. Do not guess it.

```bash
curl https://YOUR-SERVICE.onrender.com/
```

Expect HTTP 200 and:

```json
{"message":"Welcome to the Census Income Prediction API"}
```

```bash
export API_URL=https://YOUR-SERVICE.onrender.com
python request_live.py
```

The script refuses `localhost` and `127.0.0.1`. It prints the request URL, the HTTP status, and the JSON body. The payload is a held-out row that the local model scores as `>50K`.

Swagger for the live service is `https://YOUR-SERVICE.onrender.com/docs`.

## Screenshots still required

Capture these from the real GitHub and Render pages and force-add them:

- `screenshots/continuous_integration.png` — a green `pytest-and-flake8` run
- `screenshots/continuous_deployment.png` — the deploy job or the Render deploy that the hook started
- `screenshots/live_get.png` — the browser showing the live `GET /` JSON
- `screenshots/live_post.png` — `request_live.py` output with the live URL, status, and prediction

`screenshots/example.png` is already the local Swagger POST example.
