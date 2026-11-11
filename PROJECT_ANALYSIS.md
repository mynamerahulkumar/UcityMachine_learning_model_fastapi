# Project Analysis

Inspection of the Udacity starter in this directory before implementation. Dataset figures below come from a local Pandas read of `data/census.csv` on 11 November 2026. The CSV file was not modified.

## Existing project structure

The project directory is the intended application root (`main.py`, `requirements.txt`, `data/census.csv`, `starter/`). It is not its own Git repository. It sits inside `/Users/rahulkumar/Documents/GitHub/ucityproject-alls`, whose `main` branch has no commits and whose `origin/main` ref is gone. The parent remote is `https://github.com/mynamerahulkumar/ucityproject-alls.git`. GitHub Actions only loads workflows from a repository root, so this project needs its own GitHub repository before CI can run.

```text
.
├── .github/dependabot.yml
├── data/census.csv
├── model/.gitkeep
├── screenshots/.gitkeep
├── starter/ml/data.py
├── starter/ml/model.py
├── starter/train_model.py
├── main.py
├── sanitycheck.py
├── setup.py
├── requirements.txt
├── README.md
├── model_card_template.md
└── PYTHON_3_13_UPDATES.md
```

There is no `tests/` directory, no `.github/workflows/ci.yml`, no trained model, no `slice_output.txt`, and no completed `model_card.md`.

## Python and dependencies

- Project target: Python 3.13, per `README.md` and `PYTHON_3_13_UPDATES.md`.
- `/opt/homebrew/bin/python3.13` is installed. The default `python3` on this machine is 3.14.6, so the virtual environment must be created with Python 3.13.
- `requirements.txt` pins a September 2025 stack (FastAPI 0.117.1, scikit-learn 1.7.2, pandas 2.3.2, pytest 8.4.2). `joblib` is only an indirect scikit-learn dependency. `flake8` is not listed.
- `aequitas==0.42.0`, `Flask==0.12.2`, and `Flask-Bootstrap` are not required by the training or API path. They stay in the requirements file unless installation on Python 3.13 fails.
- `starter/ml/data.py` already uses `OneHotEncoder(sparse_output=False)`, which matches current scikit-learn.

## Dataset

`data/census.csv` loaded with `skipinitialspace=True`.

| Item | Value |
|---|---|
| Rows | 32561 |
| Duplicate rows | 24 (kept; they are not invalid) |
| Pandas nulls | 0 in every column |
| Target | `salary` |
| `<=50K` | 24720 |
| `>50K` | 7841 |

Columns, in file order:

`age`, `workclass`, `fnlgt`, `education`, `education-num`, `marital-status`, `occupation`, `relationship`, `race`, `sex`, `capital-gain`, `capital-loss`, `hours-per-week`, `native-country`, `salary`.

The census weight column in this file is `fnlgt`, not `fnlwgt`. Hyphenated names are preserved.

Numeric features: `age`, `fnlgt`, `education-num`, `capital-gain`, `capital-loss`, `hours-per-week`.

Categorical features used by the starter: `workclass`, `education`, `marital-status`, `occupation`, `relationship`, `race`, `sex`, `native-country`.

The raw file separates fields with `", "` (comma plus space). `skipinitialspace=True` removes that leading space. After that load, categorical values have no extra leading or trailing whitespace. `?` is the missing-value marker, not a Pandas null:

| Column | `?` count | Distinct values including `?` |
|---|---|---|
| workclass | 1836 | 9 |
| occupation | 1843 | 15 |
| native-country | 583 | 42 |
| education | 0 | 16 |

Rows with `?` in any categorical column: 2399. Rows remaining if those rows are dropped: 30162 (`<=50K`: 22654, `>50K`: 7508). Cleaning will happen in memory. The original CSV stays unchanged.

## Existing functionality

`starter/ml/data.py` `process_data` is implemented. It splits off the label, one-hot encodes categorical columns with `handle_unknown="ignore"`, binarizes the label, and concatenates numeric columns with the encoded categories. It does not strip whitespace, drop `?`, or scale numeric columns.

`starter/ml/model.py` `compute_model_metrics` returns precision, recall, and F-beta (beta = 1) with `zero_division=1`. `train_model` and `inference` are stubs (`pass`). The `train_model` docstring names `RandomForestClassifier`.

`starter/train_model.py` reads the CSV, splits 80/20 without `random_state` or stratification, processes the training split, and stops. It does not process the test split, train, save, or evaluate slices. Training code runs at import time.

`main.py` contains only a comment. `sanitycheck.py` is an interactive rubric heuristic: it prompts for a test-file path and scans test source for `.get(`, `.post(`, `.status_code`, and `.json`. The `test_dir` argument is unused.

`model_card_template.md` has empty sections. `.gitignore` ignores `*.pkl`, `*.joblib`, and `screenshots/*.{png,jpg,jpeg}` while keeping `data/census.csv` and `screenshots/.gitkeep`.

## Implementation gaps

1. Clean `?` and whitespace in memory, then use a stratified, seeded split.
2. Implement training, inference, save/load, accuracy, and per-category slice metrics.
3. Compare Random Forest with a logistic regression baseline on the same processed arrays and save the better test F1.
4. Write `model/model.pkl`, `slice_output.txt`, and `model_card.md` from measured results.
5. Serve `GET /` and `POST /model` with Pydantic aliases for hyphenated fields.
6. Add at least three model tests and three API tests, including one verified example of each salary label.
7. Pass pytest, Flake8, and `sanitycheck.py`.
8. Add GitHub Actions CI and a deploy job gated on that CI, plus Render and README documentation.
9. Capture the local Swagger screenshot. Live deployment screenshots require GitHub and Render accounts.

## Proposed implementation

Keep `process_data` and the `starter.ml` package. Add `clean_data` beside it. Train from `starter/train_model.py` under `if __name__ == "__main__"` so imports do not retrain. Save one joblib artifact containing the fitted model, encoder, label binarizer, categorical feature names, and feature column order. Slice metrics use the `education` column on the held-out test set. The API rebuilds a one-row frame with the original column names and calls the same preprocessing with `training=False`.
