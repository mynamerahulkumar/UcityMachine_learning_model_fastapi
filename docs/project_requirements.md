# MASTER CURSOR AI AGENT PROMPT
## Udacity Project: Deploying a Machine Learning Model with FastAPI

**Role:** Act as a Senior Machine Learning Engineer, Python Backend Developer, MLOps Engineer, QA Engineer, and DevOps Engineer.

Your task is to complete the Udacity project **Deploying a Machine Learning Model with FastAPI** end to end, using the existing starter repository.

You must implement the project, execute it locally, run all tests, fix errors, configure CI/CD, and prepare it for cloud deployment.

Do not simply provide instructions or code snippets. Work directly with the existing repository, create and modify files, execute commands, validate results, and maintain a clear implementation report.

---

# 1. DEVELOPMENT ENVIRONMENT

My development environment:

- Operating System: macOS
- IDE: Cursor
- Terminal: macOS Terminal / Cursor Terminal
- Python: Use a compatible version supported by the project dependencies.
- Version Control: Git and GitHub
- CI/CD: GitHub Actions
- Cloud Deployment: Render
- API Framework: FastAPI
- Machine Learning: Scikit-learn
- Testing: Pytest and Flake8

Use local development as the primary approach.

Do not depend on Udacity Workspace.

All model training, preprocessing, API development, and testing must work on my local machine.

Cloud deployment should be the final stage.

# 2. EXISTING PROJECT STRUCTURE

The current starter repository has the following structure, based on my VS Code screenshot:

```text
5_DEPLOYING_A_MACHINE_LEARNING_MODEL/
│
├── .github/
│
├── data/
│   └── census.csv
│
├── model/
│   └── .gitkeep
│
├── screenshots/
│   └── .gitkeep
│
├── starter/
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── data.py
│   │   └── model.py
│   │
│   ├── __init__.py
│   └── train_model.py
│
├── .gitignore
├── CODEOWNERS
├── dvc_on_heroku_instructions.md
├── LICENSE.txt
├── main.py
├── model_card_template.md
├── PYTHON_3_13_UPDATES.md
├── README.md
├── requirements.txt
├── sanitycheck.py
└── setup.py
```

This is the existing project structure.

IMPORTANT:

1. Do not delete the existing starter files.
2. Do not unnecessarily replace the starter architecture.
3. Do not create a completely separate project.
4. Inspect all existing Python files before implementing anything.
5. Complete the existing stubbed functions wherever possible.
6. Keep the `starter/ml/` Python package.
7. Keep the existing dataset at `data/census.csv`.
8. Keep the root-level `main.py`.
9. Preserve the provided model card template.
10. Preserve the provided `.gitignore` rules unless a necessary correction is justified.
11. Add missing folders and files only when required by the rubric.
12. Check whether the project is a flattened starter or uses another package layout before deciding import paths.

# 3. FIRST TASK: INSPECT THE ENTIRE PROJECT

Before writing code, inspect:

- `starter/ml/data.py`
- `starter/ml/model.py`
- `starter/train_model.py`
- `starter/__init__.py`
- `main.py`
- `setup.py`
- `requirements.txt`
- `sanitycheck.py`
- `.gitignore`
- `README.md`
- `model_card_template.md`
- `PYTHON_3_13_UPDATES.md`

Also inspect:

- Dataset columns.
- Dataset row count.
- Target variable.
- Data types.
- Missing values.
- Categorical features.
- Numerical features.
- Existing function signatures.
- Existing dependencies.
- Python version compatibility.

Run:

```bash
python3 --version
git status
find . -maxdepth 4 -type f | sort
```

Inspect the actual dataset using Pandas.

Do not assume that column names or target variable names are the same as other versions of the Udacity project.

Create a file named:

`PROJECT_ANALYSIS.md`

Document:

- Existing project structure.
- Existing functionality.
- Incomplete functions.
- Dataset details.
- Identified implementation gaps.
- Proposed implementation plan.
- Python and dependency compatibility.

After the analysis, proceed with implementation without waiting for approval, unless an essential external credential or account action is required.

# 4. DATASET REQUIREMENTS

Dataset:

`data/census.csv`

The dataset contains US Census Bureau information.

The task is to predict income categories.

Expected classification labels are:

- `<=50K`
- `>50K`

First verify the actual labels in the CSV.

Requirements:

1. Load the original Census dataset.
2. Inspect the columns and data types.
3. Remove unwanted leading and trailing whitespace from categorical values.
4. Handle missing and invalid values appropriately.
5. Preserve original CSV column names.
6. Do not rename columns just to make them valid Python variable names.
7. Do not modify the original dataset destructively.
8. Document preprocessing decisions.
9. Use reproducible preprocessing.

Pay special attention to columns containing hyphens, such as:

- `marital-status`
- `education-num`
- `capital-gain`
- `capital-loss`
- `hours-per-week`
- `native-country`

Use actual columns discovered in the dataset.

# 5. MACHINE LEARNING IMPLEMENTATION

Complete the existing machine learning implementation inside:

`starter/ml/model.py`

And:

`starter/ml/data.py`

Implement the following capabilities.

## A. Data loading

Implement the required data-loading functionality.

It must:

- Load the Census CSV.
- Clean the data.
- Separate features and target.
- Identify categorical columns.
- Identify numerical columns.
- Return the expected data structures.

Preserve existing starter function signatures wherever possible.

## B. Model training

Develop a classification model using Scikit-learn.

Recommended approach:

- Logistic Regression as a baseline.
- Random Forest as an alternative if appropriate.
- Use Pipeline and ColumnTransformer.
- Use StandardScaler for numerical data where appropriate.
- Use OneHotEncoder for categorical features.
- Use `handle_unknown="ignore"`.

Use a reproducible train-test split.

Recommended configuration:

- Test size: 20%.
- Random state: 42.
- Stratification based on target labels.

Select a suitable model based on actual evaluation results.

Do not invent or hardcode performance results.

## C. Required model functions

Implement functions equivalent to:

```python
train_model(...)
save_model(...)
load_model(...)
inference(...)
compute_model_metrics(...)
```

Also implement any other functions already stubbed in the starter repository.

Requirements:

- Model training must be reproducible.
- Model inference must work on new input data.
- Model saving and loading must work.
- Predictions must contain valid classification labels.
- All preprocessing artifacts must be retained.
- The saved artifacts must work without retraining.

Prefer saving the complete fitted preprocessing and classification pipeline as one Joblib artifact.

If separate encoders or preprocessing artifacts are required by the existing starter implementation, save and include them too.

Save the final model under:

`model/`

For example:

`model/model.pkl`

The exact filename should remain consistent throughout training, inference, tests, and deployment.

# 6. MODEL EVALUATION

Implement classification metrics:

- Accuracy
- Precision
- Recall
- F1-score

Use appropriate handling for class imbalance and undefined precision/recall.

Use the actual model predictions and test data.

Generate a clear model evaluation report.

Include:

- Training sample count.
- Test sample count.
- Selected algorithm.
- Feature information.
- Classification metrics.
- Model limitations.

# 7. MODEL PERFORMANCE ON DATA SLICES

This is a mandatory Udacity rubric requirement.

Implement a function that evaluates model performance on individual categorical feature values.

For example, evaluate model performance across education categories.

The function should:

1. Identify all unique categories of the selected feature.
2. Filter the evaluation dataset for each category.
3. Calculate accuracy.
4. Calculate precision.
5. Calculate recall.
6. Calculate F1-score.
7. Print results for every unique category.
8. Handle small sample sizes and single-class slices safely.

Use a categorical feature such as `education` if it exists in the actual dataset.

Implement this in the existing model package or an appropriate dedicated module.

Create a script or training-stage functionality to run slice evaluation.

MANDATORY OUTPUT:

`slice_output.txt`

The file must contain the actual calculated metrics for every category.

Do not manually enter example values.

The file must be generated when the evaluation script runs.

# 8. MODEL CARD

Use the existing:

`model_card_template.md`

Create the completed:

`model_card.md`

Do not replace the template with a short generic document.

Complete every section of the supplied template.

Include:

- Model details.
- Model type.
- Intended use.
- Training data.
- Evaluation data.
- Features.
- Training procedure.
- Evaluation metrics.
- Actual performance results.
- Model limitations.
- Ethical considerations.
- Potential demographic bias.
- Intended users.
- Risks and limitations.

Write complete sentences.

Use actual calculated model metrics.

Include observations from `slice_output.txt`.

Do not invent performance results or claim that the model is fair simply because slice metrics were calculated.

# 9. MODEL UNIT TESTING

Create:

`tests/test_model.py`

Implement at least three meaningful model unit tests.

Required coverage:

1. Training function returns a valid trained model.
2. Model saving and loading works.
3. Inference returns valid prediction values.

Additional tests are encouraged.

Use pytest fixtures where appropriate.

Tests must use temporary directories for temporary model files.

Avoid retraining the entire model unnecessarily in every test.

Use the trained artifact or lightweight fixtures appropriately.

# 10. FASTAPI APPLICATION

Complete the existing root-level:

`main.py`

Build a REST API using FastAPI.

The API must expose the following endpoints.

## GET /

Implement a welcome endpoint.

Example response:

```json
{
  "message": "Welcome to the Census Income Prediction API"
}
```

HTTP status must be 200.

## POST /model

This endpoint must perform machine learning inference.

Requirements:

1. Accept JSON request data.
2. Validate input using Pydantic.
3. Load or access the saved model.
4. Convert request data into the expected DataFrame.
5. Preserve feature order and column names.
6. Execute model inference.
7. Return a JSON prediction.
8. Handle invalid input appropriately.
9. Return useful error messages.
10. Use Python type hints.

Example response:

```json
{
  "prediction": ">50K"
}
```

The prediction must come from the actual trained model.

# 11. PYDANTIC FIELD ALIASES

This is an important Udacity requirement.

Some Census column names contain hyphens.

Python variable names cannot contain hyphens.

Do not rename the CSV columns.

Use Pydantic field aliases.

For example:

```python
from pydantic import BaseModel, Field, ConfigDict

class CensusInput(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True
    )

    education_num: int = Field(
        alias="education-num",
        examples=[13]
    )

    marital_status: str = Field(
        alias="marital-status",
        examples=["Married-civ-spouse"]
    )
```

This is only an illustration.

Create the complete Pydantic request model using every actual feature required by the trained model.

Ensure the API can map the request data to the exact CSV feature names.

Do not omit any required model input.

# 12. FASTAPI SWAGGER DOCUMENTATION

Swagger must display:

- GET endpoint.
- POST endpoint.
- Correct request schema.
- Example JSON values.
- All required request features.
- Correct field aliases.
- Response structure.

Use Pydantic examples or the supported FastAPI request-body example configuration.

Verify:

`http://127.0.0.1:8000/docs`

The example values must be visible in Swagger UI.

Create the screenshot:

`screenshots/example.png`

Do not generate fake screenshots.

Capture the actual running Swagger interface.

# 13. API UNIT TESTS

Create:

`tests/test_api.py`

Use FastAPI TestClient.

Write at least three tests.

## Test 1: GET endpoint

Verify:

- HTTP status code is 200.
- Response contains the expected welcome message.

## Test 2: POST endpoint – First prediction

Submit a valid complete Census input that has been verified to produce:

`<=50K`

Verify:

- HTTP status code is 200.
- Prediction equals the expected first class.

## Test 3: POST endpoint – Second prediction

Submit a valid complete Census input that has been verified to produce:

`>50K`

Verify:

- HTTP status code is 200.
- Prediction equals the expected second class.

Important:

Do not guess which input will produce which prediction.

Run the trained model to identify two valid examples and verify their outputs before creating the test fixtures.

Additional API tests should cover:

- Missing required fields.
- Invalid input types.
- Unknown categorical values where appropriate.
- Invalid request bodies.

The completed project must have at least six passing pytest tests in total.

# 14. PROJECT SANITY CHECK

The repository contains:

`sanitycheck.py`

Execute:

```bash
python sanitycheck.py
```

Inspect every reported issue.

Fix genuine problems.

If the checker produces a false positive, inspect the implementation against the actual Udacity rubric and document the reason.

Run the script again.

Do not ignore the sanity checker.

# 15. DEPENDENCIES

Inspect the existing:

`requirements.txt`

Update it carefully.

Include all runtime and development dependencies required by the project.

Potential packages:

- pandas
- numpy
- scikit-learn
- fastapi
- uvicorn
- pydantic
- joblib
- requests
- pytest
- httpx
- flake8

Do not blindly install incompatible package versions.

Inspect:

`PYTHON_3_13_UPDATES.md`

Determine the supported Python version.

Use one consistent Python version locally and in GitHub Actions.

Pin compatible versions in the dependency file when appropriate.

Verify that the trained model can be loaded with the deployed Scikit-learn version.

# 16. LOCAL APPLICATION EXECUTION

The completed application must work on macOS.

Create or update README instructions with exact commands.

Typical setup:

```bash
python3 -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

pip install -r requirements.txt

pip install -e .
```

Run model training using the existing training script:

```bash
python starter/train_model.py
```

Adjust the command if the existing package structure requires it.

Verify that model artifacts are generated.

Start FastAPI:

```bash
uvicorn main:app --reload
```

Test:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/docs
```

Also document how to run model evaluation and slice evaluation.

# 17. PYTEST AND FLAKE8

Run:

```bash
pytest -v
```

The completed project must have at least six passing tests.

Run:

```bash
flake8 .
```

Resolve genuine lint errors.

Avoid suppressing lint errors across the whole project just to obtain a successful result.

If configuration exclusions are needed, make them specific and justified.

Also run:

```bash
python sanitycheck.py
```

All checks must be validated locally before pushing code.

# 18. GITHUB REPOSITORY

Use GitHub as the source repository.

Do not switch to Azure DevOps.

Prepare the repository for my GitHub account.

Do not create or assume my GitHub credentials.

Create meaningful commits only when authorized and when Git remote configuration is available.

If no remote exists, explain how I can create the GitHub repository and connect it.

Include the GitHub repository URL in README.md after it becomes known.

# 19. GITHUB ACTIONS CI

Create:

`.github/workflows/ci.yml`

Requirements:

1. Trigger on pushes to `main`.
2. Trigger on pull requests targeting `main`.
3. Set up the same Python version used locally.
4. Install dependencies.
5. Install the local package if required.
6. Execute pytest.
7. Execute Flake8.
8. Fail the workflow if any check fails.

Use an appropriate GitHub Actions workflow.

Use supported action versions.

Ensure that the workflow executes from the correct project root.

Do not assume the repository root and package root are identical without inspection.

CI must successfully execute at least six tests.

Do not configure deployment to happen if the CI job fails.

# 20. GITHUB BRANCH PROTECTION

Document how to protect the main branch.

The branch protection configuration should:

- Require successful CI checks before merging pull requests.
- Prevent accidental unvalidated changes.
- Require the appropriate status check.

If GitHub account permissions are available, inspect whether the setting can be configured.

Otherwise, provide exact manual instructions.

# 21. RENDER CLOUD DEPLOYMENT

Prepare the application for Render.

Website:

https://render.com/

The API must be deployed as a Python Web Service.

Ensure:

- The application binds to `0.0.0.0`.
- The application uses the port provided by Render.
- The saved model is available in the deployment.
- Dependencies are correctly installed.
- The application uses the correct module path.
- No local absolute file paths are used.
- The API starts without retraining the model.
- The public GET endpoint works.
- The public POST endpoint works.

Use an appropriate start command, for example:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Adjust it to the actual package structure.

Create a Render deployment guide:

`DEPLOYMENT.md`

Include:

1. Render account setup.
2. Connecting GitHub.
3. Creating a Web Service.
4. Build command.
5. Start command.
6. Environment variables.
7. Model artifact requirements.
8. Deploy-hook setup.
9. Testing live endpoints.

Do not invent a deployed URL.

# 22. CONTINUOUS DEPLOYMENT

Mandatory requirement:

Deployment must happen only after successful CI.

Use GitHub Actions and a Render deploy hook.

Recommended architecture:

```text
Developer pushes to main
        |
        v
GitHub Actions
        |
        v
Install dependencies
        |
        v
Run pytest
        |
        v
Run Flake8
        |
        v
All checks successful?
        |
        +---- NO ----> Stop deployment
        |
        +---- YES ---> Deployment job
                           |
                           v
                    Read GitHub Secret
                    RENDER_DEPLOY_HOOK_URL
                           |
                           v
                    Trigger Render deployment
                           |
                           v
                    Live application
```

Implement deployment as a separate GitHub Actions job.

Requirements:

- Deployment job depends on the successful CI job.
- Deployment runs only on pushes to `main`.
- Deployment credentials must be stored as GitHub Secrets.
- Never expose the deploy-hook URL.
- Never commit credentials.
- Do not allow failed tests to trigger deployment.

Disable independent automatic deployment on Render if necessary to enforce this tested-code-only deployment workflow.

Create a clear setup guide explaining how I must configure the Render deploy hook and GitHub secret manually.

Do not claim continuous deployment is configured until it has been verified.

# 23. LIVE API TESTING

Create:

`request_live.py`

Use the Python `requests` library.

The script must:

1. Read the live API base URL from an environment variable.
2. Prepare a complete valid Census request payload.
3. Send one POST request to the live `/model` endpoint.
4. Print the HTTP status code.
5. Print the model inference result.
6. Handle HTTP errors.
7. Handle connection failures.
8. Clearly show that the request was sent to the deployed API, not localhost.

Example:

```python
import os
import requests

API_URL = os.getenv("API_URL")

if not API_URL:
    raise ValueError("API_URL environment variable is required")

payload = {
    # Complete Census feature values
}

response = requests.post(
    f"{API_URL.rstrip('/')}/model",
    json=payload,
    timeout=30
)

print("HTTP Status:", response.status_code)
print("Inference Result:", response.json())

response.raise_for_status()
```

Create the final working payload based on the Pydantic request schema.

# 24. REQUIRED SCREENSHOTS

The Udacity rubric requires exactly these five named evidence screenshots.

Create the directory:

`screenshots/`

Required files:

| Filename | Evidence |
|---|---|
| example.png | FastAPI Swagger POST documentation with request example |
| continuous_integration.png | Successful GitHub Actions CI run |
| continuous_deployment.png | Successful deployment or evidence of enabled continuous deployment |
| live_get.png | Browser showing successful live GET response |
| live_post.png | Live POST inference result and HTTP status |

Important:

- Capture actual screenshots.
- Do not create synthetic screenshots.
- Do not use placeholder images.
- Do not rename the required filenames.
- If browser interaction or account authentication is necessary, provide exact manual instructions.
- Verify all five screenshots exist before submission.
- Ensure they are included in Git despite the starter `.gitignore` excluding screenshots.

Use:

```bash
git add -f screenshots/example.png

git add -f screenshots/continuous_integration.png

git add -f screenshots/continuous_deployment.png

git add -f screenshots/live_get.png

git add -f screenshots/live_post.png
```

# 25. REQUIRED MODEL ARTIFACTS IN GIT

The starter `.gitignore` excludes generated model files.

The reviewer must receive the trained model and all fitted preprocessing artifacts needed for inference.

Do not remove the ignore rules unnecessarily.

Explicitly stage required model artifacts:

```bash
git add -f model/model.pkl
```

Adjust this path for the actual saved model.

If other artifacts are required, stage them individually.

Verify:

```bash
git diff --cached --name-only
```

Do not force-add the entire model directory.

# 26. README DOCUMENTATION

Update the existing:

`README.md`

Include:

1. Project overview.
2. Problem statement.
3. Dataset description.
4. Technology stack.
5. Project architecture.
6. Repository structure.
7. Python environment setup.
8. Dependency installation.
9. Data cleaning.
10. Model training.
11. Model evaluation.
12. Model slice evaluation.
13. Running FastAPI locally.
14. Swagger documentation.
15. Running unit tests.
16. Running Flake8.
17. Running sanitycheck.py.
18. GitHub Actions CI.
19. Render deployment.
20. Live API testing.
21. Screenshot evidence.
22. Model artifact details.
23. Known limitations.
24. GitHub repository URL.

Include exact commands that actually work with the final repository.

Do not include false claims about deployment or passing tests.

# 27. ADDITIONAL QUALITY IMPROVEMENTS

After all mandatory requirements pass, implement sensible improvements where they do not interfere with the starter project or rubric.

Potential enhancements:

- Structured logging.
- Better exception handling.
- Input validation.
- Model artifact existence checks.
- API response schemas.
- Dependency pinning.
- Model version metadata.
- Basic API health endpoint if it does not replace or alter required endpoints.
- Test coverage reporting.

Do not spend time building a frontend or adding unrelated functionality before all mandatory requirements are complete.

# 28. FINAL PROJECT VALIDATION

Before declaring completion, execute all applicable commands from the correct project root.

```bash
python -m pip install -r requirements.txt

python -m pip install -e .

python starter/train_model.py

pytest -v

flake8 .

python sanitycheck.py
```

Adjust the training command if necessary to match the existing starter implementation.

Verify:

- The model is saved.
- The preprocessing pipeline is saved.
- The model can be loaded in a fresh Python process.
- Inference works without retraining.
- Slice metrics are generated.
- `slice_output.txt` exists.
- `model_card.md` is complete.
- FastAPI starts successfully.
- GET `/` works.
- POST `/model` works.
- Swagger displays request examples.
- All six or more tests pass.
- Flake8 passes.
- Sanity checker passes or documented false positives are verified against the rubric.
- GitHub Actions workflow is correct.
- Deployment is gated behind successful CI.
- All five screenshots exist.
- Model artifacts are included in the repository.
- No credentials are committed.

Also perform a clean-environment verification where practical, using the saved model without rerunning training.

# 29. FINAL DELIVERABLES

The final project should retain the existing starter structure and contain all required implementation files.

Expected additional files include:

```text
tests/
    test_model.py
    test_api.py

.github/
    workflows/
        ci.yml

model/
    model.pkl

screenshots/
    example.png
    continuous_integration.png
    continuous_deployment.png
    live_get.png
    live_post.png

model_card.md
slice_output.txt
PROJECT_ANALYSIS.md
DEPLOYMENT.md
request_live.py
README.md
```

Do not create duplicate files if equivalent functionality already exists.

Keep the original starter files.

# 30. FINAL EXECUTION REPORT

When implementation is finished, generate:

`FINAL_IMPLEMENTATION_REPORT.md`

Use the following sections:

## A. Project implementation
List all completed features and modified files.

## B. Machine learning results
Show actual:

- Model algorithm.
- Training samples.
- Test samples.
- Accuracy.
- Precision.
- Recall.
- F1-score.

## C. Slice evaluation
Summarize actual performance across categories.

## D. API verification
Show:

- GET endpoint result.
- POST endpoint result.
- Swagger documentation verification.

## E. Test results
Show:

- Total pytest tests.
- Passed tests.
- Failed tests.
- Flake8 result.
- Sanity checker result.

## F. CI/CD
Show:

- GitHub workflow status.
- Deployment gating implementation.
- Render configuration status.

## G. Submission evidence
List all five required screenshots and all model artifacts.

## H. Remaining manual steps
Explicitly identify actions requiring my credentials or account access, including:

- GitHub repository creation if needed.
- GitHub Secrets configuration.
- Render account configuration.
- Render deploy-hook creation.
- Final cloud deployment.
- Screenshot capture requiring browser authentication.

## I. Final rubric assessment
Create a table:

| Rubric requirement | Status | Evidence |
|---|---|---|
| Git and CI setup | Complete/Pending | Actual evidence |
| Six passing pytest tests | Complete/Pending | Test output |
| Flake8 | Complete/Pending | Command output |
| ML model | Complete/Pending | Model artifact |
| Model evaluation | Complete/Pending | Metrics |
| Slice evaluation | Complete/Pending | slice_output.txt |
| Model card | Complete/Pending | model_card.md |
| FastAPI | Complete/Pending | main.py |
| Pydantic examples | Complete/Pending | Swagger screenshot |
| API tests | Complete/Pending | pytest output |
| Cloud deployment | Complete/Pending | Live URL |
| Continuous deployment | Complete/Pending | Workflow and deployment evidence |
| Live GET | Complete/Pending | live_get.png |
| Live POST | Complete/Pending | live_post.png |
| Model artifacts submitted | Complete/Pending | Git tracking evidence |
| Repository documentation | Complete/Pending | README.md |

Never mark a requirement Complete without actual evidence.

---

# 31. EXECUTION RULES FOR CURSOR AGENT

Follow these rules throughout implementation:

1. Work directly in the opened repository.
2. Inspect before modifying.
3. Preserve the existing starter architecture.
4. Implement one logical phase at a time.
5. Execute relevant commands after each phase.
6. Fix errors before moving to dependent phases.
7. Do not fabricate model metrics, predictions, test results, screenshots, or deployment URLs.
8. Do not use mock inference in production code.
9. Do not hardcode credentials.
10. Do not commit secrets.
11. Do not silently skip rubric requirements.
12. Do not stop after generating code.
13. Actually execute the tests and verify the application.
14. Keep the implementation reproducible.
15. Document any manual action requiring my authorization.
16. Do not claim successful cloud deployment without verifying the live service.
17. Keep the project suitable for a Udacity reviewer to clone and execute.
18. Prioritize mandatory rubric compliance over optional improvements.

**MOST IMPORTANT:**

I want a fully implemented, executable, tested, and deployment-ready project, not merely a generated codebase.

Start by inspecting the existing repository and creating `PROJECT_ANALYSIS.md`.

Then implement the complete project phase by phase.

Continue automatically through all tasks that can be performed locally. Stop only when an external account, credential, approval, or user interaction is genuinely required.

At the end, provide the exact commands I should execute and the remaining manual steps required to submit the project successfully.