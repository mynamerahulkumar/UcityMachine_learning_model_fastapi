# Model Card

For additional information see the Model Card paper: https://arxiv.org/pdf/1810.03993.pdf

## Model Details

This model predicts whether a person's Census income is above $50,000. It is a scikit-learn `RandomForestClassifier` trained with `random_state=42` and the library default of 100 trees. The saved artifact is `model/model.pkl`. That file contains the fitted forest, the fitted `OneHotEncoder`, the fitted `LabelBinarizer`, the categorical feature names, and the feature column order. The positive class is `>50K` (`LabelBinarizer` code 1). The negative class is `<=50K` (code 0).

A logistic regression baseline, with `StandardScaler` fit on the same encoded training matrix, was trained on the same split. Its test F1 was 0.6637. The random forest test F1 was 0.6750, so the forest is the saved model. These figures were produced by `python starter/train_model.py` and stored in `model/metrics.json`. They were not entered by hand.

## Intended Use

The model is a teaching artifact for a FastAPI deployment project. It is meant to show training, slice evaluation, and JSON inference on the Census Income data. Intended users are reviewers and students who call `GET /` and `POST /model`.

It is not a tool for hiring, lending, insurance, housing, benefits, or any other decision about a real person. Income recorded in a historical survey is not a measure of merit, and the model does not explain why a person is in either class.

## Training Data

The source file is `data/census.csv`, the UCI Adult / Census Income extract shipped with this starter. It has 32,561 rows and 14 input columns plus the `salary` label. The original file was not edited.

Cleaning happens in memory. `skipinitialspace=True` removes the space after each comma. String fields are stripped. The token `?` is treated as missing. That token appears in `workclass` (1,836 rows), `occupation` (1,843 rows), and `native-country` (583 rows). Dropping any row with a `?` removes 2,399 rows and leaves 30,162 rows. Of those, 22,654 are `<=50K` and 7,508 are `>50K`. Twenty-four exact duplicate rows in the raw file are kept.

The stratified split uses 80% for training and 20% for testing, `random_state=42`. The training set has 24,129 rows. Numeric inputs are `age`, `fnlgt`, `education-num`, `capital-gain`, `capital-loss`, and `hours-per-week`. Categorical inputs are `workclass`, `education`, `marital-status`, `occupation`, `relationship`, `race`, `sex`, and `native-country`. The weight column in this file is named `fnlgt`.

## Evaluation Data

The evaluation set is the held-out 20% split: 6,033 rows from the cleaned data. The same encoder and label binarizer fitted on the training split are applied to the test split. The model is not refit on the test rows. Slice metrics use this same test set, grouped by `education`.

## Metrics

Precision, recall, and F1 are computed for the positive class `>50K`, with `zero_division=1`. Accuracy counts both classes.

On the 6,033 test rows the saved random forest scored:

- Accuracy: 0.8497
- Precision: 0.7308
- Recall: 0.6272
- F1: 0.6750

The scaled logistic regression baseline scored accuracy 0.8472, precision 0.7339, recall 0.6059, and F1 0.6637.

About one quarter of cleaned rows are `>50K`, so accuracy stays high if the model predicts `<=50K` often. Recall of 0.6272 means a substantial share of people above $50,000 are still predicted as `<=50K`.

Slice performance on `education` is in `slice_output.txt`. Larger slices differ in a way accuracy alone hides. `HS-grad` has 2,023 test rows and an F1 of 0.4750, with recall 0.3891: most high-school graduates who are actually above $50,000 are missed. `Bachelors` (1,010 rows) has F1 0.7565. `Masters` (334 rows) has F1 0.8098. `Prof-school` (108 rows) has F1 0.9213, but 85 of those 108 rows are already `>50K`, so a high score is partly the base rate.

Sparse slices are not evidence of equal performance. `1st-4th` has 27 test rows, zero actual `>50K` labels, and zero `>50K` predictions. Its precision, recall, and F1 are all 1.0000 only because `zero_division=1` fills in a divide-by-zero. `Preschool` has 8 rows, zero actual `>50K` labels, and one `>50K` prediction, so precision is 0 and the reported recall of 1.0000 is the same zero-division fill. `9th` and `5th-6th` have no positive predictions, so their precision of 1.0000 is also that fill, while recall is 0. `12th` has three actual `>50K` rows and a precision and recall of 0.

## Ethical Considerations

The training labels come from a 1994 US Census extract. Income patterns by sex, race, and country of origin in that extract reflect historical inequality, labor-market discrimination, and who was counted. This model uses `sex`, `race`, and `native-country` as inputs, so it can reproduce those patterns in its predictions. That is a reason not to use it to rank or screen people.

Education slices already show uneven error. People whose highest reported schooling is high school are much more likely to have a true `>50K` label missed than people with a bachelor's or master's degree. Calculating those slices does not make the model fair. No equalized-odds or demographic-parity claim is made here. `aequitas` is listed in the environment for optional study and was not used to certify this model.

Missing `workclass`, `occupation`, and `native-country` values were dropped rather than modeled. People with incomplete records are absent from both training and the reported metrics.

## Caveats and Recommendations

Do not treat a prediction as a determination of income. The feature `capital-gain` is capped in the source data, including the value 99999, and `fnlgt` is a survey weight rather than a personal trait. Categories with few test rows, especially `Preschool` and `1st-4th`, do not support a stable score.

Serve only the saved artifact. Retraining without the same seed, split, and cleaning will change predictions and will invalidate the examples in the API tests. Review `slice_output.txt` before describing performance to someone else, and keep the limitation on the `>50K` recall next to the accuracy number.
