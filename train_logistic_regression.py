import os
import json
import joblib

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    top_k_accuracy_score
)

from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score


# ============================================================
# CONFIGURATION
# ============================================================

TRAIN_FILE = "data/train.csv"
VALIDATION_FILE = "data/validation.csv"
TEST_FILE = "data/test.csv"

MODEL_DIR = "models"

TEXT_COLUMN = "ML_Text"
TARGET_COLUMN = "Suggested_Career_Path"

RANDOM_STATE = 42


# ============================================================
# CREATE MODEL DIRECTORY
# ============================================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("MILESTONE 1 - BASELINE LOGISTIC REGRESSION")
print("=" * 70)


# ============================================================
# CHECK FILES
# ============================================================

print("\nChecking dataset files...")

required_files = [
    TRAIN_FILE,
    VALIDATION_FILE,
    TEST_FILE
]

for file_path in required_files:

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"\nRequired file not found: {file_path}\n"
            f"Run Step 1 dataset preparation first."
        )

    print(
        f"✓ {file_path}"
    )


# ============================================================
# LOAD DATASETS
# ============================================================

print("\n" + "=" * 70)
print("LOADING DATASETS")
print("=" * 70)

train_df = pd.read_csv(
    TRAIN_FILE
)

validation_df = pd.read_csv(
    VALIDATION_FILE
)

test_df = pd.read_csv(
    TEST_FILE
)


print(
    f"\nTraining shape   : {train_df.shape}"
)

print(
    f"Validation shape : {validation_df.shape}"
)

print(
    f"Test shape       : {test_df.shape}"
)


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

print("\nChecking required columns...")

for df_name, df in [
    ("Training", train_df),
    ("Validation", validation_df),
    ("Test", test_df)
]:

    if TEXT_COLUMN not in df.columns:

        raise ValueError(
            f"{TEXT_COLUMN} missing from {df_name} dataset."
        )

    if TARGET_COLUMN not in df.columns:

        raise ValueError(
            f"{TARGET_COLUMN} missing from {df_name} dataset."
        )

print("✓ Required columns found")


# ============================================================
# CLEAN TEXT
# ============================================================

print("\nCleaning text data...")


def clean_text(series):

    return (
        series
        .fillna("")
        .astype(str)
        .str.strip()
    )


X_train_text = clean_text(
    train_df[TEXT_COLUMN]
)

X_validation_text = clean_text(
    validation_df[TEXT_COLUMN]
)

X_test_text = clean_text(
    test_df[TEXT_COLUMN]
)


# ============================================================
# REMOVE EMPTY TRAINING RECORDS
# ============================================================

train_mask = (
    X_train_text.str.len() > 0
)

validation_mask = (
    X_validation_text.str.len() > 0
)

test_mask = (
    X_test_text.str.len() > 0
)


X_train_text = (
    X_train_text[train_mask]
    .reset_index(drop=True)
)

X_validation_text = (
    X_validation_text[validation_mask]
    .reset_index(drop=True)
)

X_test_text = (
    X_test_text[test_mask]
    .reset_index(drop=True)
)


y_train_text = (
    train_df.loc[
        train_mask,
        TARGET_COLUMN
    ]
    .astype(str)
    .str.strip()
    .reset_index(drop=True)
)

y_validation_text = (
    validation_df.loc[
        validation_mask,
        TARGET_COLUMN
    ]
    .astype(str)
    .str.strip()
    .reset_index(drop=True)
)

y_test_text = (
    test_df.loc[
        test_mask,
        TARGET_COLUMN
    ]
    .astype(str)
    .str.strip()
    .reset_index(drop=True)
)


print(
    f"Training records   : {len(X_train_text)}"
)

print(
    f"Validation records : {len(X_validation_text)}"
)

print(
    f"Test records       : {len(X_test_text)}"
)


# ============================================================
# LABEL ENCODING
# ============================================================

print("\n" + "=" * 70)
print("CAREER LABEL ENCODING")
print("=" * 70)


label_encoder = LabelEncoder()

# IMPORTANT:
# Fit the encoder only on training labels.

label_encoder.fit(
    y_train_text
)


y_train = label_encoder.transform(
    y_train_text
)


# Check that validation/test labels exist
# in the training classes.

known_classes = set(
    label_encoder.classes_
)


unknown_validation = (
    set(y_validation_text)
    - known_classes
)

unknown_test = (
    set(y_test_text)
    - known_classes
)


if unknown_validation:

    raise ValueError(
        "Validation contains career classes "
        "not present in training:\n"
        f"{unknown_validation}"
    )


if unknown_test:

    raise ValueError(
        "Test contains career classes "
        "not present in training:\n"
        f"{unknown_test}"
    )


y_validation = label_encoder.transform(
    y_validation_text
)

y_test = label_encoder.transform(
    y_test_text
)


print(
    f"\nNumber of career classes: "
    f"{len(label_encoder.classes_)}"
)


print("\nCareer classes:")

for index, career in enumerate(
    label_encoder.classes_
):

    print(
        f"{index:02d} -> {career}"
    )


# ============================================================
# CLASS DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("TRAINING CLASS DISTRIBUTION")
print("=" * 70)


class_distribution = (
    y_train_text
    .value_counts()
    .sort_index()
)


print(
    class_distribution.to_string()
)


# ============================================================
# TF-IDF
# ============================================================

print("\n" + "=" * 70)
print("TF-IDF FEATURE EXTRACTION")
print("=" * 70)


vectorizer = TfidfVectorizer(

    lowercase=True,

    strip_accents="unicode",

    # Unigrams + bigrams
    ngram_range=(1, 2),

    # Ignore extremely rare words
    min_df=2,

    # Ignore words appearing in almost every document
    max_df=0.98,

    # Gives slightly more weight to informative terms
    sublinear_tf=True,

    # Prevent extremely large feature matrices
    max_features=100000
)


print(
    "\nFitting TF-IDF on TRAINING data only..."
)


X_train = vectorizer.fit_transform(
    X_train_text
)


print(
    "Transforming validation data..."
)


X_validation = vectorizer.transform(
    X_validation_text
)


print(
    "Transforming test data..."
)


X_test = vectorizer.transform(
    X_test_text
)


print(
    f"\nTraining feature matrix   : "
    f"{X_train.shape}"
)

print(
    f"Validation feature matrix : "
    f"{X_validation.shape}"
)

print(
    f"Test feature matrix       : "
    f"{X_test.shape}"
)


# ============================================================
# BASELINE LOGISTIC REGRESSION
# ============================================================

print("\n" + "=" * 70)
print("TRAINING BASELINE LOGISTIC REGRESSION")
print("=" * 70)


model = LogisticRegression(

    # Baseline regularization
    C=1.0,

    max_iter=3000,

    solver="lbfgs",

    # Balanced weighting helps if classes aren't perfectly equal
    class_weight="balanced",

    random_state=RANDOM_STATE
)


print("\nTraining...")


model.fit(
    X_train,
    y_train
)


print(
    "✓ Training completed"
)


# ============================================================
# TRAINING ACCURACY
# ============================================================

train_predictions = model.predict(
    X_train
)


train_accuracy = accuracy_score(
    y_train,
    train_predictions
)


print(
    f"\nTraining accuracy: "
    f"{train_accuracy * 100:.2f}%"
)


# ============================================================
# VALIDATION PREDICTION
# ============================================================

print("\n" + "=" * 70)
print("VALIDATION EVALUATION")
print("=" * 70)


validation_predictions = model.predict(
    X_validation
)

validation_probabilities = (
    model.predict_proba(
        X_validation
    )
)


validation_accuracy = accuracy_score(
    y_validation,
    validation_predictions
)

validation_precision = precision_score(
    y_validation,
    validation_predictions,
    average="weighted",
    zero_division=0
)

validation_recall = recall_score(
    y_validation,
    validation_predictions,
    average="weighted",
    zero_division=0
)

validation_f1 = f1_score(
    y_validation,
    validation_predictions,
    average="weighted",
    zero_division=0
)


# Top-K
all_labels = np.arange(
    len(label_encoder.classes_)
)


validation_top3 = top_k_accuracy_score(

    y_validation,

    validation_probabilities,

    k=3,

    labels=all_labels
)


validation_top5 = top_k_accuracy_score(

    y_validation,

    validation_probabilities,

    k=5,

    labels=all_labels
)


print(
    f"\nValidation Top-1 Accuracy : "
    f"{validation_accuracy * 100:.2f}%"
)

print(
    f"Validation Top-3 Accuracy : "
    f"{validation_top3 * 100:.2f}%"
)

print(
    f"Validation Top-5 Accuracy : "
    f"{validation_top5 * 100:.2f}%"
)

print(
    f"Validation Precision      : "
    f"{validation_precision * 100:.2f}%"
)

print(
    f"Validation Recall         : "
    f"{validation_recall * 100:.2f}%"
)

print(
    f"Validation F1 Score       : "
    f"{validation_f1 * 100:.2f}%"
)


# ============================================================
# 5-FOLD CROSS VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("5-FOLD CROSS-VALIDATION")
print("=" * 70)


cv = StratifiedKFold(

    n_splits=5,

    shuffle=True,

    random_state=RANDOM_STATE
)


cv_scores = cross_val_score(

    model,

    X_train,

    y_train,

    cv=cv,

    scoring="accuracy",

    n_jobs=-1
)


print("\nCross-validation results:")


for index, score in enumerate(
    cv_scores,
    start=1
):

    print(
        f"Fold {index}: "
        f"{score * 100:.2f}%"
    )


cv_mean = cv_scores.mean()

cv_std = cv_scores.std()


print(
    f"\nMean CV Accuracy : "
    f"{cv_mean * 100:.2f}%"
)

print(
    f"CV Std Dev       : "
    f"{cv_std * 100:.2f}%"
)


# ============================================================
# FINAL TEST EVALUATION
# ============================================================

print("\n" + "=" * 70)
print("FINAL TEST EVALUATION")
print("=" * 70)


test_predictions = model.predict(
    X_test
)

test_probabilities = (
    model.predict_proba(
        X_test
    )
)


test_accuracy = accuracy_score(
    y_test,
    test_predictions
)

test_precision = precision_score(
    y_test,
    test_predictions,
    average="weighted",
    zero_division=0
)

test_recall = recall_score(
    y_test,
    test_predictions,
    average="weighted",
    zero_division=0
)

test_f1 = f1_score(
    y_test,
    test_predictions,
    average="weighted",
    zero_division=0
)


test_top3 = top_k_accuracy_score(

    y_test,

    test_probabilities,

    k=3,

    labels=all_labels
)


test_top5 = top_k_accuracy_score(

    y_test,

    test_probabilities,

    k=5,

    labels=all_labels
)


print(
    f"\nTest Top-1 Accuracy : "
    f"{test_accuracy * 100:.2f}%"
)

print(
    f"Test Top-3 Accuracy : "
    f"{test_top3 * 100:.2f}%"
)

print(
    f"Test Top-5 Accuracy : "
    f"{test_top5 * 100:.2f}%"
)

print(
    f"Test Precision      : "
    f"{test_precision * 100:.2f}%"
)

print(
    f"Test Recall         : "
    f"{test_recall * 100:.2f}%"
)

print(
    f"Test F1 Score       : "
    f"{test_f1 * 100:.2f}%"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\n" + "=" * 70)
print("CLASSIFICATION REPORT")
print("=" * 70)


classification_report_text = (
    classification_report(

        y_test,

        test_predictions,

        target_names=label_encoder.classes_,

        zero_division=0
    )
)


print(
    classification_report_text
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print("\n" + "=" * 70)
print("CONFUSION MATRIX")
print("=" * 70)


confusion = confusion_matrix(

    y_test,

    test_predictions
)


print(
    confusion
)


# ============================================================
# SAVE MODELS
# ============================================================

print("\n" + "=" * 70)
print("SAVING MODEL FILES")
print("=" * 70)


model_file = os.path.join(
    MODEL_DIR,
    "logistic_regression.pkl"
)

tfidf_file = os.path.join(
    MODEL_DIR,
    "tfidf.pkl"
)

encoder_file = os.path.join(
    MODEL_DIR,
    "label_encoder.pkl"
)


joblib.dump(
    model,
    model_file
)

joblib.dump(
    vectorizer,
    tfidf_file
)

joblib.dump(
    label_encoder,
    encoder_file
)


print(
    f"✓ {model_file}"
)

print(
    f"✓ {tfidf_file}"
)

print(
    f"✓ {encoder_file}"
)


# ============================================================
# SAVE METRICS
# ============================================================

metrics = {

    "model":
        "Baseline Logistic Regression",

    "random_state":
        RANDOM_STATE,

    "training_samples":
        int(len(X_train_text)),

    "validation_samples":
        int(len(X_validation_text)),

    "test_samples":
        int(len(X_test_text)),

    "number_of_classes":
        int(len(label_encoder.classes_)),

    "tfidf_features":
        int(X_train.shape[1]),

    "training_accuracy":
        float(train_accuracy),

    "cv_mean_accuracy":
        float(cv_mean),

    "cv_std":
        float(cv_std),

    "validation_accuracy":
        float(validation_accuracy),

    "validation_top3_accuracy":
        float(validation_top3),

    "validation_top5_accuracy":
        float(validation_top5),

    "validation_precision":
        float(validation_precision),

    "validation_recall":
        float(validation_recall),

    "validation_f1":
        float(validation_f1),

    "test_accuracy":
        float(test_accuracy),

    "test_top3_accuracy":
        float(test_top3),

    "test_top5_accuracy":
        float(test_top5),

    "test_precision":
        float(test_precision),

    "test_recall":
        float(test_recall),

    "test_f1":
        float(test_f1),

    "career_classes":
        label_encoder.classes_.tolist()
}


metrics_file = os.path.join(
    MODEL_DIR,
    "logistic_regression_metrics.json"
)


with open(
    metrics_file,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        metrics,
        file,
        indent=4
    )


print(
    f"✓ {metrics_file}"
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("BASELINE LOGISTIC REGRESSION COMPLETE")
print("=" * 70)


print(
    f"\nTraining Accuracy : "
    f"{train_accuracy * 100:.2f}%"
)

print(
    f"CV Mean Accuracy  : "
    f"{cv_mean * 100:.2f}%"
)

print(
    f"Validation Top-1  : "
    f"{validation_accuracy * 100:.2f}%"
)

print(
    f"Test Top-1        : "
    f"{test_accuracy * 100:.2f}%"
)

print(
    f"Test Top-3        : "
    f"{test_top3 * 100:.2f}%"
)

print(
    f"Test Top-5        : "
    f"{test_top5 * 100:.2f}%"
)

print(
    f"Test F1            : "
    f"{test_f1 * 100:.2f}%"
)


print("\nSaved files:")

print(
    "  models/logistic_regression.pkl"
)

print(
    "  models/tfidf.pkl"
)

print(
    "  models/label_encoder.pkl"
)

print(
    "  models/logistic_regression_metrics.json"
)


print(
    "\nStep 2 completed successfully."
)