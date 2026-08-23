"""
CareerCast - Automated Model Accuracy Gate

Purpose:
    Evaluate the registered/production Random Forest model
    against the CareerCast test dataset.

CI rule:
    Accuracy >= MIN_ACCURACY  -> PASS
    Accuracy <  MIN_ACCURACY  -> FAIL

Exit codes:
    0 = PASS
    1 = FAIL
"""

import json
import os
import sys

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)

MODELS_DIR = os.path.join(
    PROJECT_ROOT,
    "models"
)

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data"
)

MODEL_PATH = os.path.join(
    MODELS_DIR,
    "random_forest.pkl"
)

TFIDF_PATH = os.path.join(
    MODELS_DIR,
    "random_forest_tfidf.pkl"
)

LABEL_ENCODER_PATH = os.path.join(
    MODELS_DIR,
    "random_forest_label_encoder.pkl"
)

TEST_DATA_PATH = os.path.join(
    DATA_DIR,
    "test.csv"
)

METRICS_OUTPUT_PATH = os.path.join(
    MODELS_DIR,
    "accuracy_gate_results.json"
)


# ============================================================
# ACCURACY GATE
# ============================================================

MIN_ACCURACY = 0.90


# ============================================================
# HELPER
# ============================================================

def check_file(path, description):

    if not os.path.exists(path):

        print(
            f"ERROR: Missing {description}: {path}"
        )

        sys.exit(1)

    print(
        f"OK: {description}"
    )


# ============================================================
# START
# ============================================================

print("\n========================================")
print("CAREERCAST AUTOMATED ACCURACY GATE")
print("========================================")


# ============================================================
# CHECK FILES
# ============================================================

print("\nChecking required files...")

check_file(
    MODEL_PATH,
    "Random Forest model"
)

check_file(
    TFIDF_PATH,
    "TF-IDF vectorizer"
)

check_file(
    LABEL_ENCODER_PATH,
    "Label encoder"
)

check_file(
    TEST_DATA_PATH,
    "Test dataset"
)


# ============================================================
# LOAD MODEL
# ============================================================

print("\nLoading Random Forest model...")

model = joblib.load(
    MODEL_PATH
)

print(
    "Model loaded:",
    type(model).__name__
)


# ============================================================
# LOAD TF-IDF
# ============================================================

print("\nLoading TF-IDF vectorizer...")

tfidf = joblib.load(
    TFIDF_PATH
)

print(
    "TF-IDF loaded successfully."
)


# ============================================================
# LOAD LABEL ENCODER
# ============================================================

print("\nLoading label encoder...")

label_encoder = joblib.load(
    LABEL_ENCODER_PATH
)

print(
    "Label encoder loaded successfully."
)


# ============================================================
# LOAD TEST DATA
# ============================================================

print("\nLoading test dataset...")

df = pd.read_csv(
    TEST_DATA_PATH
)

print(
    "Test dataset shape:",
    df.shape
)


# ============================================================
# VALIDATE COLUMNS
# ============================================================

REQUIRED_COLUMNS = [
    "ML_Text",
    "Suggested_Career_Path"
]

for column in REQUIRED_COLUMNS:

    if column not in df.columns:

        print(
            f"ERROR: Required column missing: {column}"
        )

        sys.exit(1)


# ============================================================
# PREPARE DATA
# ============================================================

X_text = (
    df["ML_Text"]
    .fillna("")
    .astype(str)
)

y_text = (
    df["Suggested_Career_Path"]
    .astype(str)
)

print(
    "\nTest samples:",
    len(df)
)


# ============================================================
# TRANSFORM TEST DATA
# ============================================================

print(
    "\nTransforming test data using TF-IDF..."
)

X_test = tfidf.transform(
    X_text
)

print(
    "Test feature matrix:",
    X_test.shape
)


# ============================================================
# ENCODE TARGET
# ============================================================

print(
    "\nEncoding target labels..."
)

try:

    y_test = label_encoder.transform(
        y_text
    )

except Exception as exc:

    print(
        "\nERROR: Failed to encode test labels."
    )

    print(exc)

    sys.exit(1)


# ============================================================
# GENERATE PREDICTIONS
# ============================================================

print(
    "\nGenerating predictions..."
)

y_pred = model.predict(
    X_test
)


# ============================================================
# CALCULATE METRICS
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n========================================")
print("MODEL EVALUATION")
print("========================================")

print(
    f"Accuracy : {accuracy:.4f} "
    f"({accuracy * 100:.2f}%)"
)

print(
    f"Precision: {precision:.4f}"
)

print(
    f"Recall   : {recall:.4f}"
)

print(
    f"F1 Score : {f1:.4f}"
)

print(
    f"Required : {MIN_ACCURACY:.4f} "
    f"({MIN_ACCURACY * 100:.2f}%)"
)

print("========================================")


# ============================================================
# DETERMINE GATE RESULT
# ============================================================

gate_passed = (
    accuracy >= MIN_ACCURACY
)


if gate_passed:

    gate_status = "PASS"

else:

    gate_status = "FAIL"


# ============================================================
# SAVE RESULTS
# ============================================================

results = {

    "gate": {

        "status": gate_status,

        "minimum_accuracy": MIN_ACCURACY,

        "actual_accuracy": float(
            accuracy
        ),

        "passed": bool(
            gate_passed
        )
    },

    "metrics": {

        "accuracy": float(
            accuracy
        ),

        "precision": float(
            precision
        ),

        "recall": float(
            recall
        ),

        "f1_score": float(
            f1
        )
    },

    "dataset": {

        "test_samples": int(
            len(df)
        ),

        "feature_count": int(
            X_test.shape[1]
        )
    },

    "model": {

        "name": "Random Forest",

        "model_path": MODEL_PATH,

        "tfidf_path": TFIDF_PATH,

        "label_encoder_path": LABEL_ENCODER_PATH
    }
}


with open(
    METRICS_OUTPUT_PATH,
    "w"
) as file:

    json.dump(
        results,
        file,
        indent=4
    )


print(
    "\nResults saved to:"
)

print(
    METRICS_OUTPUT_PATH
)


# ============================================================
# FINAL GATE
# ============================================================

print("\n========================================")

if gate_passed:

    print(
        "ACCURACY GATE: PASS"
    )

    print(
        f"Accuracy {accuracy * 100:.2f}% "
        f">= "
        f"{MIN_ACCURACY * 100:.2f}%"
    )

    print(
        "CI pipeline may continue."
    )

    print("========================================")

    sys.exit(0)


else:

    print(
        "ACCURACY GATE: FAIL"
    )

    print(
        f"Accuracy {accuracy * 100:.2f}% "
        f"< "
        f"{MIN_ACCURACY * 100:.2f}%"
    )

    print(
        "CI pipeline must stop."
    )

    print("========================================")

    sys.exit(1)