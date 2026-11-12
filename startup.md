# Startup and rubric check

Run every command from this directory:

```text
/Users/rahulkumar/Documents/GitHub/UcityMachine_learning_model_fastapi
```

That folder is the Git root for https://github.com/mynamerahulkumar/UcityMachine_learning_model_fastapi.git.

[architecture.md](architecture.md) explains the training path, the request path, and the code. This file is the checklist you follow in order. Sections 1–5 stay on this Mac. Section 6 pushes `main` to GitHub. Section 7 connects that repository to Render and stores the deploy hook. Section 8 takes the four live screenshots. Section 9 commits those pictures and pushes them. Section 10 protects `main` after that push has succeeded.

The evidence notes are what this directory produced on 11 November 2026 with Python 3.13.13. Cloud rows stay pending until you push and create the Render service.

`python3` on this Mac is 3.14.6. Use `python3.13` for every step below.

There are five screenshots in total. One is local (section 3). Four are live (section 8). Take each picture, rename it, and only then take the next one.

| When | File | Page that must be in the picture |
|---|---|---|
| Section 3, while uvicorn is running | `screenshots/example.png` | `http://127.0.0.1:8000/docs` with `POST /model` expanded. Already captured. Retake it only if the file is missing. |
| Section 8, after both Actions jobs are green | `screenshots/continuous_integration.png` | GitHub Actions run on `main` with a green `pytest-and-flake8` job |
| Section 8, same green Actions run | `screenshots/continuous_deployment.png` | GitHub Actions job `render-deploy` green, including `Render deploy hook accepted the request.` |
| Section 8, public site awake | `screenshots/live_get.png` | Browser on `https://YOUR-SERVICE.onrender.com/` showing the welcome JSON |
| Section 8, after `request_live.py` | `screenshots/live_post.png` | Terminal with the public `/model` URL, HTTP 200, and `>50K` |

## How to capture a window on this Mac

Do this once before section 3, and again before each picture in section 8.

1. Press **Shift+Command+5**. The screenshot toolbar opens at the bottom of the screen.
2. Click **Options**.
3. Set **Save to** to **Desktop**.
4. Press **Escape** to close the toolbar.
5. When a step says "capture this window":
   1. Make the browser or terminal window large enough that the address bar (or the full command output) is on screen.
   2. Press **Shift+Command+4**.
   3. Press **Space**. The pointer becomes a camera.
   4. Click the window you want. macOS saves `Screenshot <date> at <time>.png` on the Desktop.
6. Rename that file immediately, before you take another picture. From this directory:

```bash
ls -t ~/Desktop/Screenshot*.png | head -3
mv "$(ls -t ~/Desktop/Screenshot*.png | head -1)" screenshots/THE-NAME-IN-THE-STEP.png
```

Replace `THE-NAME-IN-THE-STEP.png` with the file name in that step, for example `example.png`.

A picture of the wrong host, a login page, a spinner, or a red job does not satisfy the rubric. Capture the page only after the expected text is visible.

## 1. Environment

Open a terminal. Go to this directory and create the virtual environment.

```bash
cd /Users/rahulkumar/Documents/GitHub/UcityMachine_learning_model_fastapi
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

`pip install -e .` can warn when Git has no commits. The `starter` package still imports. Keep this terminal. Later sections assume `(.venv)` is at the start of the prompt. If you open a new terminal, run `cd` and `source .venv/bin/activate` again.

Evidence: a new `.venv` on Python 3.13.13 installed `requirements.txt` and the editable `starter` package. `aequitas==0.42.0` and `Flask==0.12.2` installed. They are not on the training or API path.

## 2. Saved model

Leave the model in place when `model/model.pkl` is already present. The API tests are locked to its predictions.

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

## 3. Local API and `screenshots/example.png`

### 3.1 Start the server

In the first terminal, with the virtual environment active:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

Leave this process running. The server exits at startup if `model/model.pkl` is missing. You should see Uvicorn report that it is listening on `http://127.0.0.1:8000`.

### 3.2 Call the local routes

Open a second terminal:

```bash
cd /Users/rahulkumar/Documents/GitHub/UcityMachine_learning_model_fastapi
source .venv/bin/activate
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

### 3.3 Open Swagger and capture `example.png`

`screenshots/example.png` is already that page, captured on 11 November 2026. Skip this capture when the file is present. Retake it when the file is missing, using the steps below. Leave uvicorn running the whole time.

1. In the browser, open http://127.0.0.1:8000/docs.
2. Confirm the address bar shows `127.0.0.1:8000/docs`.
3. On the page, find **POST** `/model` and click it so the row expands.
4. Click **Try it out** only if the example body is still collapsed. You need the example JSON on screen. You do not need to execute the request.
5. Scroll until the example body is visible. The body must show the hyphenated names `education-num`, `marital-status`, `capital-gain`, `capital-loss`, `hours-per-week`, and `native-country`.
6. Capture the browser window with the shortcut in "How to capture a window on this Mac".
7. Move the picture:

```bash
mv "$(ls -t ~/Desktop/Screenshot*.png | head -1)" screenshots/example.png
```

The address bar in the picture must show `127.0.0.1:8000/docs`, and the example body must show those hyphenated field names.

Stop the server with Ctrl-C in the first terminal when the file is saved. Sections 4 and 5 do not need the server.

## 4. Tests, lint, and the sanity check

In the terminal where the virtual environment is active:

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

## 6. First commit and push to GitHub

GitHub is the source repository. Render deploys the commit that is already on `main`. The remote is:

```text
origin  https://github.com/mynamerahulkumar/UcityMachine_learning_model_fastapi.git
```

Follow this order. `main` stays open to a direct push through section 9. Section 10 turns on branch protection only after the screenshot commit is on GitHub. A ruleset that requires a pull request rejects `git push` to `main`.

1. Section 6. Push the code, the model, and `screenshots/example.png`.
2. Section 7. Create the Render service from this GitHub repository, store the deploy hook, and push once more so the deploy job can run.
3. Section 8. Capture the four live screenshots from the green Actions run and the live Render URL.
4. Section 9. Commit those four pictures and push them to `main`.
5. Section 10. Protect `main` so later merges require a pull request and a green `pytest-and-flake8` check.

Do this push before you open Render. The API fails to boot if `model/model.pkl` is missing from that commit.

`.gitignore` ignores `*.pkl`, other generated model files, `*.csv` except `data/census.csv`, screenshot images, `.venv`, caches, and secrets. A plain `git add` therefore skips the model and every PNG. `git add -f` stages one ignored file anyway. Force-add only the two files below. Leave the rest of `model/` untracked.

```bash
git add -f model/model.pkl
git add -f screenshots/example.png
git add .
git status
```

`git add .` stages the source, tests, workflow, and docs. It still skips `.venv`, caches, and any PNG you have not force-added. Before you commit, `git status` must list `model/model.pkl`, `screenshots/example.png`, `main.py`, `tests/`, `.github/workflows/ci.yml`, `README.md`, `DEPLOYMENT.md`, `architecture.md`, and this file. It must list neither `.venv` nor a deploy-hook URL.

```bash
git commit -m "$(cat <<'EOF'
Add the census income API, saved model, and CI workflow.

EOF
)"
git push -u origin main
```

`model/model.pkl` is about 66 MB. GitHub warns above 50 MB and accepts this file. GitHub rejects a file above 100 MB.

This pass did not commit or push. `main` still has no commits. On disk, `model/model.pkl` and `screenshots/example.png` are already staged from the two `git add -f` commands.

The first push starts GitHub Actions. Open https://github.com/mynamerahulkumar/UcityMachine_learning_model_fastapi/actions and watch the run named **CI** on branch `main`.

- `pytest-and-flake8` can pass on this first run.
- `render-deploy` fails until the secret in section 7 exists. The log says `RENDER_DEPLOY_HOOK_URL secret is not set.` That failure is expected. Leave this red run on the screen. The screenshots in section 8 are of the later green run, after the secret exists.

## 7. Render service from the GitHub repository

After you push `main`, GitHub runs `.github/workflows/ci.yml`.

- Job `pytest-and-flake8` installs this requirements file on Python 3.13, then runs `pytest -v` and `flake8 .`. It runs on pushes and on pull requests to `main`.
- Job `render-deploy` has `needs` that test job. It runs only on a push to `main`. It POSTs the secret `RENDER_DEPLOY_HOOK_URL` and does not print the URL. A failed test or lint job does not start it.

That second job is the continuous deployment. Render **Auto-Deploy** stays **No**, so a push cannot go live before `pytest-and-flake8` passes. `render.yaml` sets `autoDeploy: false`. The Actions job is what starts the Render build after the tests pass.

Create the service only after section 6 has pushed `main`. The clicks below match the Render and GitHub pages you will see. More background is in [DEPLOYMENT.md](DEPLOYMENT.md).

### 7.1 Create the Render account

1. Open https://render.com in the browser.
2. Click **Get Started** or **Sign Up**.
3. Sign up with GitHub if you can. That connects the repository in the same step. Otherwise create the account with email, then connect GitHub in the next step.
4. Finish any email confirmation Render asks for. You should land on https://dashboard.render.com.

The blueprint uses the free plan. If the account has no free web-service allowance, change `plan: free` in `render.yaml` to a paid plan, commit that change, and push before you apply the blueprint.

### 7.2 Give Render access to this repository only

If you signed up with GitHub and already granted access to `mynamerahulkumar/UcityMachine_learning_model_fastapi`, skip to section 7.3.

1. On the Render dashboard, click your avatar in the top right.
2. Open **Account Settings**.
3. Open **GitHub** (sometimes labeled **Git Providers**).
4. Click **Connect** or **Configure**.
5. GitHub opens an install page for Render. Choose **Only select repositories**.
6. Select `mynamerahulkumar/UcityMachine_learning_model_fastapi`.
7. Click **Install** or **Save**.

Connect this repository. The parent folder on your Mac is not a GitHub repository Render can deploy. `main.py`, `requirements.txt`, `render.yaml`, and `.github/workflows/ci.yml` are at the root of this repo, so the root directory on Render stays empty.

### 7.3 Create the service from the blueprint

1. Go back to https://dashboard.render.com.
2. Click the **New** button (top right).
3. Click **Blueprint**.
4. If Render asks you to connect a repository, pick the GitHub account `mynamerahulkumar` and the repository `UcityMachine_learning_model_fastapi`.
5. Branch: `main`.
6. Blueprint path: `render.yaml`. Leave the default if that path is already filled in.
7. Read the preview. It must show one web service named `census-income-api`, runtime Python, plan Free.
8. Confirm these values in the preview. They come from `render.yaml`. If a field is editable and differs, set it to the value in this table before you apply.

| Setting | Value |
|---|---|
| Name | `census-income-api` |
| Runtime | Python |
| Plan | Free |
| Build command | `pip install -r requirements.txt && pip install -e .` |
| Start command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Auto-Deploy | No (`autoDeploy: false`) |
| `PYTHON_VERSION` | `3.13.13` |

9. Click **Apply** (the button may say **Create Blueprint**).
10. Wait until Render finishes creating the service. The first apply builds once, even with auto-deploy off. That build uses the commit you pushed in section 6, including `model/model.pkl`.

If **Blueprint** is missing from the **New** menu, create the service by hand:

1. **New → Web Service**.
2. Select `mynamerahulkumar/UcityMachine_learning_model_fastapi`, branch `main`.
3. Name: `census-income-api`.
4. Language / runtime: Python.
5. Root directory: leave it empty.
6. Build command: `pip install -r requirements.txt && pip install -e .`
7. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
8. Instance type: Free.
9. Add environment variable `PYTHON_VERSION` = `3.13.13`.
10. Click **Create Web Service**.

### 7.4 Confirm the service settings

1. On the dashboard, click the web service `census-income-api`.
2. Copy the public URL at the top of the service page. It looks like `https://census-income-api.onrender.com` or `https://census-income-api-xxxx.onrender.com`. Save it in a note. You will paste it in section 8. There is no public URL until this page shows one.
3. Open the **Settings** tab.
4. Under **Build & Deploy**, confirm:
   - Build command: `pip install -r requirements.txt && pip install -e .`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Auto-Deploy** is **No**. If it says **Yes** or **On**, change it to **No** and save. Auto-deploy must stay off so a push cannot go live before `pytest-and-flake8` passes. `render.yaml` also sets `autoDeploy: false`.
5. Under **Environment**, confirm `PYTHON_VERSION` is `3.13.13`. If the build log says Render has no such patch, set this to the newest 3.13 the log offers, save, and use that same version later if you change GitHub Actions.

The API reads `model/model.pkl` from the deployed Git tree at startup. It does not train on boot. A missing file fails the deploy with a clear error in the Render logs. Paths in the app are relative to `main.py`.

### 7.5 Create the deploy hook

The hook URL is a credential. Copy it into the GitHub secret in the next step. Keep it out of the terminal history you will screenshot, out of markdown, and out of Git.

1. Stay on the service **Settings** tab.
2. Scroll to **Deploy Hook**.
3. Click **Create Deploy Hook**.
4. Name it `github-actions`.
5. Click **Create**.
6. Copy the full URL. It looks like `https://api.render.com/deploy/srv-xxxxxxxx?key=yyyyyyyy`.
7. Leave that tab open until the GitHub secret is saved. Some accounts show the key only once.

### 7.6 Store the hook as a GitHub secret

1. Open https://github.com/mynamerahulkumar/UcityMachine_learning_model_fastapi/settings/secrets/actions.
2. Click **New repository secret**.
3. Name: `RENDER_DEPLOY_HOOK_URL` (this exact spelling, including capitals).
4. Secret: paste the hook URL from Render.
5. Click **Add secret**.
6. The Actions secrets list should show `RENDER_DEPLOY_HOOK_URL`. The value stays hidden. That is what you want.

### 7.7 Trigger the gated deploy

The secret does not rerun the failed job by itself. Push an empty commit so Actions starts a new run, the test job passes, and `render-deploy` POSTs the hook.

```bash
git commit --allow-empty -m "$(cat <<'EOF'
Trigger the gated Render deploy.

EOF
)"
git push
```

### 7.8 Wait until GitHub and Render are both green

1. Open https://github.com/mynamerahulkumar/UcityMachine_learning_model_fastapi/actions.
2. Click the newest **CI** run on `main`. Its commit message is `Trigger the gated Render deploy.`
3. Wait until `pytest-and-flake8` has a green check.
4. Wait until `render-deploy` has a green check. Open that job. The log must contain `Render deploy hook accepted the request.` The log must not contain the hook URL.
5. Go back to the Render service `census-income-api`.
6. Open **Events** (the tab may be labeled **Deploys**).
7. Wait until the newest deploy, the one started by the deploy hook, shows **Live**. A free instance build often takes several minutes. If the deploy fails, open the build log, fix the setting it names, and push again. The usual miss is a missing `model/model.pkl` or a Python version Render does not offer.

Leave both pages open. Section 8 captures them next. The first request to a free instance can take about a minute while it wakes up. Leave `main` unprotected until section 10, after the screenshot commit is on GitHub.

## 8. Capture the four live screenshots

Use the Mac shortcut from the top of this file. Take the pictures in the order below. After each one, run the `mv` command before you take the next picture. The two Actions pictures use the green run from section 7.8. The two live pictures use the public Render host from section 7.4. A `127.0.0.1` or `localhost` address is the local server, and it does not count for `live_get.png` or `live_post.png`.

### 8.1 `screenshots/continuous_integration.png`

This picture proves the tests and Flake8 passed on GitHub.

1. Use the Actions tab you left open in section 7.8. If you closed it, open https://github.com/mynamerahulkumar/UcityMachine_learning_model_fastapi/actions and click the green **CI** run for `Trigger the gated Render deploy.`
2. Stay on the run summary, where the job list is visible. You need a green check next to `pytest-and-flake8`, the branch name `main`, and the address bar on `github.com/.../actions`.
3. If the summary is too small to read the job name, click `pytest-and-flake8` and scroll so a passed `pytest` step and a passed `flake8` step are on screen. The address bar must still be the Actions URL for this repository.
4. Capture the browser window.
5. Save it:

```bash
mv "$(ls -t ~/Desktop/Screenshot*.png | head -1)" screenshots/continuous_integration.png
```

Capture the green run from section 7.8. The earlier run, where `render-deploy` failed because the secret was missing, is the wrong picture.

### 8.2 `screenshots/continuous_deployment.png`

This picture proves the deployment stage finished after the tests. That stage is the GitHub Actions job `render-deploy`.

1. On the same green **CI** run from section 8.1, click `render-deploy`.
2. Scroll until the log shows `Render deploy hook accepted the request.`
3. The frame must include the green check, the job name `render-deploy`, the branch `main`, and that success line. The log must hide the hook URL. The workflow sends the secret and discards the response body, so the URL should not appear.
4. Capture the browser window.
5. Save it:

```bash
mv "$(ls -t ~/Desktop/Screenshot*.png | head -1)" screenshots/continuous_deployment.png
```

If that log is too short to read, use the Render service as the same file:

1. Open the Render dashboard and click `census-income-api`.
2. Open **Events** (or **Deploys**).
3. Select the deploy that started after the green `render-deploy` job. The trigger text says the deploy hook started it.
4. Wait until that row says **Live**.
5. Keep the public `*.onrender.com` URL in the same window.
6. Capture that window and run the same `mv` command so the file is still `screenshots/continuous_deployment.png`.

Keep a single file with that name. The Actions job is the picture to take when the log is readable.

### 8.3 `screenshots/live_get.png`

This picture proves the public GET works. Wake the free instance here, before the POST script, because `request_live.py` gives up after 30 seconds.

1. Paste the public URL from section 7.4 into the address bar. It must end at the site root, for example `https://census-income-api.onrender.com/`.
2. Press Return and wait. A free instance that has been asleep shows a Render loading page first. Wait until that page is replaced by the JSON. Give it about a minute.
3. The address bar must be the Render host, and the page body must be:

```json
{"message":"Welcome to the Census Income Prediction API"}
```

4. Capture the browser window so the address bar and that JSON are both visible.
5. Save it:

```bash
mv "$(ls -t ~/Desktop/Screenshot*.png | head -1)" screenshots/live_get.png
```

You can check the same response in a terminal, but the screenshot itself is the browser window:

```bash
curl -sS -D - https://YOUR-SERVICE.onrender.com/
echo
```

Replace the host with the URL you copied. Expect HTTP 200 and the welcome message.

### 8.4 `screenshots/live_post.png`

This picture proves a live POST returned a prediction. Run it in the project terminal with the virtual environment active, right after the GET page has loaded, while the instance is awake.

```bash
cd /Users/rahulkumar/Documents/GitHub/UcityMachine_learning_model_fastapi
source .venv/bin/activate
export API_URL=https://YOUR-SERVICE.onrender.com
python request_live.py
```

Replace `https://YOUR-SERVICE.onrender.com` with the URL from section 7.4. No trailing path. The script adds `/model`.

The script rejects `localhost` and `127.0.0.1`. It prints the URL it called, the HTTP status, and the JSON body. The payload is the `>50K` example from section 3.

Leave the terminal window open. The picture must include all of these lines, with your real host in the URL:

```text
Request URL: https://YOUR-SERVICE.onrender.com/model
HTTP Status: 200
Inference Result: {'prediction': '>50K'}
```

The command you typed (`export API_URL=...` and `python request_live.py`) should be in the same window, above that output.

1. Capture the terminal window.
2. Save it:

```bash
mv "$(ls -t ~/Desktop/Screenshot*.png | head -1)" screenshots/live_post.png
```

If the script prints `Request timed out` or `Connection failed`, the free instance was still waking up. Open the GET URL in the browser again, wait until the welcome JSON appears, then run `python request_live.py` a second time and capture that successful output.

### 8.5 Confirm the four files

```bash
file screenshots/continuous_integration.png \
  screenshots/continuous_deployment.png \
  screenshots/live_get.png \
  screenshots/live_post.png
```

Each line should say `PNG image data`. If a name is still a Desktop screenshot, move that file with the matching `mv` command above and run `file` again.

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

`git status` before that commit should list only those four PNGs. This push runs the tests again and asks Render to deploy again. You already have the four pictures, so you can leave that later deploy to finish on its own. Push it now, while a direct push to `main` still works. Section 10 runs after this push succeeds.

Before you submit, `screenshots/` must contain these five PNGs, and Git must be tracking them (`git ls-files screenshots`):

- `screenshots/example.png`
- `screenshots/continuous_integration.png`
- `screenshots/continuous_deployment.png`
- `screenshots/live_get.png`
- `screenshots/live_post.png`

## 10. Protect `main`

Do this after the section 9 push has succeeded. GitHub already knows the check name from the green run in section 7.8. You need admin rights on the repository. Later changes to `main` go through a pull request. The deploy job still runs only when that pull request is merged and the push to `main` passes `pytest-and-flake8`.

Ruleset:

1. Open https://github.com/mynamerahulkumar/UcityMachine_learning_model_fastapi/settings/rules.
2. Click **New ruleset**, then **New branch ruleset**.
3. Ruleset name: `protect main`.
4. Enforcement status: **Active**.
5. Target branches: **Include default branch**, or add a branch name pattern `main`.
6. Enable **Require a pull request before merging**.
7. Enable **Require status checks to pass**.
8. In the status-check search box, add `pytest-and-flake8`. GitHub may show it as `CI / pytest-and-flake8`. Add that check.
9. Leave `render-deploy` off the required-checks list. That job does not run on pull requests, so requiring it would block every merge.
10. Save the ruleset.

Classic branch protection, if the settings page still has it:

1. **Settings → Branches → Add branch protection rule** (or **Add classic branch protection rule**).
2. Branch name pattern: `main`.
3. Enable **Require a pull request before merging**.
4. Enable **Require status checks to pass before merging**.
5. Search for and select `pytest-and-flake8`.
6. Leave `render-deploy` unselected.
7. Click **Create** or **Save changes**.

## Rubric checklist

The rows below follow [docs/rubric_points.md](docs/rubric_points.md) for this GitHub and Render project. Code rows are already in the repository. The pending rows are the GitHub secret, the live Render URL, the four live screenshots, and branch protection.

| Rubric requirement | Status | Evidence |
|---|---|---|
| GitHub Actions workflow on push to `main` | Complete in the repo, pending the first run | [.github/workflows/ci.yml](.github/workflows/ci.yml) runs `pytest` and `flake8` on Python 3.13. Section 6 pushes `main`. |
| At least six passing tests | Complete | `11 passed, 1 warning in 35.58s`. Four tests in [tests/test_model.py](tests/test_model.py), seven in [tests/test_api.py](tests/test_api.py). |
| Flake8 with no errors | Complete | `flake8 .` exit 0. Config is `.flake8`. |
| CI screenshot | Pending | Section 8.1. `screenshots/continuous_integration.png` |
| Train, save, load, inference, and metrics | Complete | [starter/ml/model.py](starter/ml/model.py). [starter/train_model.py](starter/train_model.py) calls those functions on an 80/20 split and saves `model/model.pkl`. |
| At least three model unit tests | Complete | [tests/test_model.py](tests/test_model.py) checks the fitted type, save/load, inference, and artifact keys. |
| Slice metrics for every `education` value | Complete | `evaluate_slices` writes [slice_output.txt](slice_output.txt), including `HS-grad` and `Bachelors`. |
| Model card, every template section, with metrics | Complete | [model_card.md](model_card.md). Selected F1 0.6750, accuracy 0.8497, precision 0.7308, recall 0.6272. |
| GET `/` and POST inference | Complete | [main.py](main.py). Local `GET /` 200 and both `POST /model` labels. |
| Pydantic example on the docs page | Complete | Hyphenated aliases and examples in `CensusInput`. `screenshots/example.png`. |
| API tests for GET and both labels | Complete | [tests/test_api.py](tests/test_api.py) checks status and body for `GET /`, `<=50K`, and `>50K`. |
| Model artifact in Git | Pending | Section 6. `model/model.pkl` is on disk and staged. It is not committed. |
| Deploy from GitHub only after pytest and flake8 | Complete in the workflow, pending the secret | `render-deploy` needs `pytest-and-flake8` and runs only on a push to `main`. Render Auto-Deploy stays No. |
| Deploy hook stored as a GitHub secret | Pending | Section 7.5 and 7.6. Name `RENDER_DEPLOY_HOOK_URL`. The URL is not in the repo. |
| Continuous deployment screenshot | Pending | Section 8.2. `screenshots/continuous_deployment.png` |
| Live GET screenshot | Pending | Section 8.3. `screenshots/live_get.png` |
| Live POST script | Complete | [request_live.py](request_live.py) prints the public URL, the status, and the prediction, and rejects localhost. |
| Live POST screenshot | Pending | Section 8.4. `screenshots/live_post.png` |
| Protected `main` | Pending | Section 10, after the screenshot push. Require a pull request and `pytest-and-flake8`. |
