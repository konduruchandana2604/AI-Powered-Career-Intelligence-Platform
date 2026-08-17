"""
======================================================================
MILESTONE 2 - STEP 5
BENCHMARK VALIDATION
======================================================================

Validates the CareerCast recommendation system on:
1. Internal test dataset
2. SemEval career benchmark (when available)
3. LinkedIn career transition dataset (when available)

IMPORTANT:
Do not create or claim external benchmark results unless the actual
benchmark datasets are available.
======================================================================
"""

import os
import json
import pickle
import time

import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# =====================================================================
# CONFIGURATION
# =====================================================================

TEST_FILE = "data/test.csv"
SEMEVAL_FILE = "data/semeval_career.csv"
LINKEDIN_FILE = "data/linkedin_transitions.csv"

XGBOOST_MODEL = "models/xgboost.pkl"
XGBOOST_TFIDF = "models/xgboost_tfidf.pkl"
XGBOOST_ENCODER = "models/xgboost_label_encoder.pkl"

OUTPUT_FILE = "models/benchmark_validation_results.json"


# =====================================================================
# HEADER
# =====================================================================

print("=" * 70)
print("MILESTONE 2 - STEP 5")
print("BENCHMARK VALIDATION")
print("=" * 70)


# =====================================================================
# CHECK MODEL FILES
# =====================================================================

print("\n" + "=" * 70)
print("CHECKING REQUIRED MODEL FILES")
print("=" * 70)

required_models = [
    XGBOOST_MODEL,
    XGBOOST_TFIDF,
    XGBOOST_ENCODER
]

for file_path in required_models:
    if os.path.exists(file_path):
        print(f"✓ {file_path}")
    else:
        print(f"✗ Missing: {file_path}")
        raise FileNotFoundError(
            f"Required model file not found: {file_path}"
        )


# =====================================================================
# LOAD MODELS
# =====================================================================

print("\n" + "=" * 70)
print("LOADING XGBOOST MODEL")
print("=" * 70)

with open(XGBOOST_MODEL, "rb") as f:
    xgb_model = pickle.load(f)

with open(XGBOOST_TFIDF, "rb") as f:
    tfidf = pickle.load(f)

with open(XGBOOST_ENCODER, "rb") as f:
    label_encoder = pickle.load(f)

print("✓ XGBoost model loaded")
print("✓ TF-IDF vectorizer loaded")
print("✓ Label encoder loaded")

print(f"\nNumber of career classes: {len(label_encoder.classes_)}")

for i, career in enumerate(label_encoder.classes_):
    print(f"{i:02d} -> {career}")


# =====================================================================
# METRIC FUNCTION
# =====================================================================

def calculate_metrics(y_true, y_pred, probabilities=None):
    """
    Calculate Top-1, Top-3, Top-5 and classification metrics.
    """

    results = {}

    # ---------------------------------------------------------------
    # Top-1
    # ---------------------------------------------------------------

    results["top_1_accuracy"] = float(
        accuracy_score(y_true, y_pred)
    )

    # ---------------------------------------------------------------
    # Top-K
    # ---------------------------------------------------------------

    if probabilities is not None:

        # Top 3
        top3_indices = np.argsort(
            probabilities,
            axis=1
        )[:, -3:]

        top3_correct = sum(
            y_true[i] in top3_indices[i]
            for i in range(len(y_true))
        )

        results["top_3_accuracy"] = float(
            top3_correct / len(y_true)
        )

        # Top 5
        top5_indices = np.argsort(
            probabilities,
            axis=1
        )[:, -5:]

        top5_correct = sum(
            y_true[i] in top5_indices[i]
            for i in range(len(y_true))
        )

        results["top_5_accuracy"] = float(
            top5_correct / len(y_true)
        )

    # ---------------------------------------------------------------
    # Precision
    # ---------------------------------------------------------------

    results["precision"] = float(
        precision_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0
        )
    )

    # ---------------------------------------------------------------
    # Recall
    # ---------------------------------------------------------------

    results["recall"] = float(
        recall_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0
        )
    )

    # ---------------------------------------------------------------
    # F1
    # ---------------------------------------------------------------

    results["f1_score"] = float(
        f1_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0
        )
    )

    return results


# =====================================================================
# DATASET VALIDATION FUNCTION
# =====================================================================

def validate_dataset(
    file_path,
    dataset_name,
    text_column="ML_Text",
    label_column="Suggested_Career_Path"
):

    print("\n" + "=" * 70)
    print(dataset_name.upper())
    print("=" * 70)

    if not os.path.exists(file_path):
        print(f"⚠ Dataset not found:")
        print(f"  {file_path}")
        print("  Skipping this benchmark.")

        return None

    print(f"✓ Dataset found: {file_path}")

    # ---------------------------------------------------------------
    # Load
    # ---------------------------------------------------------------

    df = pd.read_csv(file_path)

    print(f"Dataset shape: {df.shape}")

    # ---------------------------------------------------------------
    # Check columns
    # ---------------------------------------------------------------

    if text_column not in df.columns:
        print(
            f"✗ Missing text column: {text_column}"
        )

        print("Available columns:")
        print(list(df.columns))

        return None

    if label_column not in df.columns:
        print(
            f"✗ Missing label column: {label_column}"
        )

        print("Available columns:")
        print(list(df.columns))

        return None

    print(f"✓ Text column: {text_column}")
    print(f"✓ Label column: {label_column}")

    # ---------------------------------------------------------------
    # Clean
    # ---------------------------------------------------------------

    df = df[
        [text_column, label_column]
    ].dropna()

    df[text_column] = (
        df[text_column]
        .astype(str)
        .str.strip()
    )

    df[label_column] = (
        df[label_column]
        .astype(str)
        .str.strip()
    )

    df = df[
        (df[text_column] != "") &
        (df[label_column] != "")
    ]

    print(f"Records after cleaning: {len(df)}")

    # ---------------------------------------------------------------
    # Map labels
    # ---------------------------------------------------------------

    known_classes = set(
        label_encoder.classes_
    )

    df = df[
        df[label_column].isin(known_classes)
    ]

    print(
        f"Records matching CareerCast classes: {len(df)}"
    )

    if len(df) == 0:
        print(
            "⚠ No records match the CareerCast career classes."
        )

        return None

    # ---------------------------------------------------------------
    # Transform text
    # ---------------------------------------------------------------

    print("Generating TF-IDF features...")

    X = tfidf.transform(
        df[text_column].values
    )

    # ---------------------------------------------------------------
    # Encode labels
    # ---------------------------------------------------------------

    y = label_encoder.transform(
        df[label_column].values
    )

    # ---------------------------------------------------------------
    # Prediction
    # ---------------------------------------------------------------

    print("Running XGBoost predictions...")

    probabilities = xgb_model.predict_proba(X)

    predictions = np.argmax(
        probabilities,
        axis=1
    )

    # ---------------------------------------------------------------
    # Metrics
    # ---------------------------------------------------------------

    metrics = calculate_metrics(
        y,
        predictions,
        probabilities
    )

    print("\nRESULTS")
    print("-" * 70)

    print(
        f"Top-1 Accuracy : "
        f"{metrics['top_1_accuracy'] * 100:.2f}%"
    )

    print(
        f"Top-3 Accuracy : "
        f"{metrics['top_3_accuracy'] * 100:.2f}%"
    )

    print(
        f"Top-5 Accuracy : "
        f"{metrics['top_5_accuracy'] * 100:.2f}%"
    )

    print(
        f"Precision      : "
        f"{metrics['precision'] * 100:.2f}%"
    )

    print(
        f"Recall         : "
        f"{metrics['recall'] * 100:.2f}%"
    )

    print(
        f"F1 Score       : "
        f"{metrics['f1_score'] * 100:.2f}%"
    )

    # ---------------------------------------------------------------
    # Classification report
    # ---------------------------------------------------------------

    print("\nClassification Report")
    print("-" * 70)

    print(
        classification_report(
            y,
            predictions,
            target_names=label_encoder.classes_,
            zero_division=0
        )
    )

    # ---------------------------------------------------------------
    # Confusion matrix
    # ---------------------------------------------------------------

    cm = confusion_matrix(
        y,
        predictions
    )

    return {
        "dataset": dataset_name,
        "file": file_path,
        "records": int(len(df)),
        "metrics": metrics,
        "confusion_matrix": cm.tolist()
    }


# =====================================================================
# INTERNAL TEST DATASET
# =====================================================================

test_results = validate_dataset(
    TEST_FILE,
    "CareerCast Internal Test Dataset"
)


# =====================================================================
# SEMEVAL
# =====================================================================

semeval_results = validate_dataset(
    SEMEVAL_FILE,
    "SemEval Career Benchmark"
)


# =====================================================================
# LINKEDIN
# =====================================================================

linkedin_results = validate_dataset(
    LINKEDIN_FILE,
    "Curated LinkedIn Transition Dataset"
)


# =====================================================================
# SAVE RESULTS
# =====================================================================

print("\n" + "=" * 70)
print("SAVING VALIDATION RESULTS")
print("=" * 70)

results = {
    "milestone": "Milestone 2",
    "step": "Step 5",
    "model": "XGBoost",
    "career_classes": len(label_encoder.classes_),
    "career_names": label_encoder.classes_.tolist(),
    "internal_test": test_results,
    "semeval": semeval_results,
    "linkedin": linkedin_results,
    "timestamp": time.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
}

os.makedirs(
    "models",
    exist_ok=True
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        results,
        f,
        indent=4
    )

print(f"✓ Saved: {OUTPUT_FILE}")


# =====================================================================
# FINAL SUMMARY
# =====================================================================

print("\n" + "=" * 70)
print("MILESTONE 2 - STEP 5 SUMMARY")
print("=" * 70)

if test_results is not None:

    m = test_results["metrics"]

    print(
        f"Internal Test Top-1 : "
        f"{m['top_1_accuracy'] * 100:.2f}%"
    )

    print(
        f"Internal Test Top-3 : "
        f"{m['top_3_accuracy'] * 100:.2f}%"
    )

    print(
        f"Internal Test Top-5 : "
        f"{m['top_5_accuracy'] * 100:.2f}%"
    )

if semeval_results is None:
    print(
        "SemEval Benchmark   : NOT AVAILABLE"
    )

if linkedin_results is None:
    print(
        "LinkedIn Dataset     : NOT AVAILABLE"
    )

print("\n✓ Step 5 validation framework completed.")
print("=" * 70)