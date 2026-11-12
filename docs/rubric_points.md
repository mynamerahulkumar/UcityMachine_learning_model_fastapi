Use this project rubric to understand and assess the project criteria.

git
Criteria	Submission Requirements
Set up Git-based version control and continuous integration using either GitHub Actions or Azure Pipelines.

The project uses one of the following platform workflows:

GitHub: The repository contains a GitHub Actions workflow under .github/workflows/.
Azure DevOps: The repository contains an azure-pipelines.yml pipeline definition and the project is stored in Azure Repos.
For either workflow, continuous integration must:

run when code is pushed to main or master;
use the same Python version used during development;
run pytest and flake8;
pass pytest with at least six tests in the completed project; and
pass flake8 without errors.
The submission must include reviewable evidence of the successful continuous-integration run:

GitHub: Include either an accessible GitHub repository URL or a screenshot of the passing CI run named continuous_integration.png.
Azure DevOps: Include continuous_integration.png, showing the successful Azure Pipeline run, and upload a complete-repository ZIP created from a fresh clone of the final Azure Repos repository. The ZIP must contain the .git directory and azure-pipelines.yml.
For Azure DevOps, the private Azure Repos URL should also be recorded in README.md, but the URL does not need to be accessible to the reviewer. The learner must not be required to invite a reviewer to the Azure DevOps organization, make the project public, or weaken its security controls.

Model building
Criteria	Submission Requirements
Create a machine learning model.

The model should train on the provided data. The data should either be split to have a train-test split or use cross-validation on the entire dataset.
Implement all stubbed functions in the starter code or create equivalents. At a minimum, there should be functions to:
train, save and load the model and any categorical encoders
model inference
determine the classification metrics.
Write a script that takes in the data, processes it, trains the model, and saves it and the encoder. This script must use the functions you have written.
Write unit tests.

Write at least 3 unit tests. Unit testing ML can be hard due to the stochasticity -- at least test if any ML functions return the expected type.
Write a function that computes model metrics on slices of the data.

Write a function that computes performance on model slices. I.e. a function that computes the performance metrics when the value of a given feature is held fixed. E.g. for education, it would print out the model metrics for each slice of data that has a particular value for education. You should have one set of outputs for every single unique value in education.
Complete the stubbed function or write a new one that for a given categorical variable computes the metrics when its value is held fixed.
Write a script that runs this function (or include it as part of the training script) that iterates through the distinct values in one of the features and prints out the model metrics for each value.
Output the printout to a file named slice_output.txt.
Write a model card.

The model card should address every section of the template. Please use the provided Model Card Template(opens in a new tab).
The model card should be written in complete sentences and include metrics on model performance. Please include both the metrics used and your model's performance on those metrics.
API Creation
Criteria	Submission Requirements
Create a REST API.

The API must implement GET and POST. GET must be on the root domain and give a greeting and POST on a different path that does model inference.
Use Python type hints such that FastAPI creates the automatic documentation.
Use a Pydantic model to ingest the body of the POST. This should implement an example (hint: Pydantic/FastAPI provides multiple ways to do this, see the docs for more information: https://fastapi.tiangolo.com/tutorial/schema-extra-example/(opens in a new tab)).
Include a screenshot of the docs that shows the example and name it example.png.
The starter .gitignore excludes images in screenshots/. Explicitly commit every screenshot required by this rubric using git add -f <path-to-image>, and verify that all required images are included in the submitted repository or ZIP.

Create tests for an API.

You should write at least three test cases -

A test case for the GET method. This MUST test both the status code as well as the contents of the request object.
One test case for EACH of the possible inferences (results/outputs) of the ML model.
API Deployment
Criteria	Submission Requirements
Deploy the FastAPI application to a cloud application platform using continuous deployment from either GitHub or Azure DevOps.

The application is deployed from the protected main or master branch using one of the following workflows:

GitHub: Deploy from the GitHub repository using a cloud provider integration or a GitHub Actions deployment workflow.
Azure DevOps: Deploy using an Azure Pipelines deployment stage that depends on the successful continuous-integration stage and runs only for the protected main branch.
For either workflow:

deployment must occur only after pytest and flake8 pass;
automatic or continuous deployment must be enabled;
deployment credentials must be stored as secrets and must not appear in source files, Git history, screenshots, or pipeline YAML;
the submission must include a screenshot showing that continuous deployment is enabled or that the deployment stage completed successfully, named continuous_deployment.png; and
the submission must include a screenshot showing a browser successfully receiving the response from the implemented GET endpoint on the live root domain, named live_get.png.
The learner may use Render, Heroku, PythonAnywhere, or another cloud application platform that satisfies these requirements. For Render with Azure Pipelines, a secret deploy-hook URL may be called from the deployment stage. For Heroku with Azure Pipelines, the tested commit may be pushed to the Heroku Git remote using an API key stored as a secret pipeline variable. The deployment destination does not replace GitHub or Azure Repos as the project's source repository.

Query the live API.

Write a script that:

sends a POST request to the live API using the requests module;
prints the model inference result;
prints the HTTP status code; and
successfully receives a response from the deployed API rather than a locally running API.
Include a screenshot showing the script's inference result and HTTP status code. Name the screenshot live_post.png.

Suggestions to Make Your Project Stand Out
Use codecov or equivalent to measure the test coverage (then write more tests and try to hit 100% coverage!).
Implement FastAPI’s advanced features such as authentication.
Create a front end for the API.
