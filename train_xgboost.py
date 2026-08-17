"""
======================================================================
MILESTONE 2 - STEP 2
XGBOOST WITH CROSS-VALIDATED HYPERPARAMETER TUNING
======================================================================

Inputs:
    data/train.csv
    data/validation.csv
    data/test.csv

Outputs:
    models/xgboost.pkl
    models/xgboost_tfidf.pkl
    models/xgboost_label_encoder.pkl
    models/xgboost_metrics.json
======================================================================
"""

import os
import json
import pickle
import time
import warnings

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

from xgboost import XGBClassifier

warnings.filterwarnings("ignore")


# ======================================================================
# CONFIGURATION
# ======================================================================

TRAIN_FILE = "data/train.csv"
VALIDATION_FILE = "data/validation.csv"
TEST_FILE = "data/test.csv"

MODEL_DIR = "models"

MODEL_FILE = os.path.join(MODEL_DIR, "xgboost.pkl")
TFIDF_FILE = os.path.join(MODEL_DIR, "xgboost_tfidf.pkl")
LABEL_ENCODER_FILE = os.path.join(
    MODEL_DIR, "xgboost_label_encoder.pkl"
)
METRICS_FILE = os.path.join(
    MODEL_DIR, "xgboost_metrics.json"
)

TEXT_COLUMN = "ML_Text"
TARGET_COLUMN = "Suggested_Career_Path"


# ======================================================================
# HELPER FUNCTIONS
# ======================================================================

def print_header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def save_pickle_verified(obj, filepath):
    """
    Save a Python object using pickle and immediately verify
    that the saved file can be reloaded.
    """

    with open(filepath, "wb") as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)

    # Verify immediately
    with open(filepath, "rb") as f:
        reloaded = pickle.load(f)

    if type(reloaded) is not type(obj):
        raise RuntimeError(
            f"Verification failed for {filepath}"
        )

    print(f"✓ Saved and verified: {filepath}")


def load_pickle(filepath):
    """
    Safely load a pickle file.
    """

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"File not found: {filepath}"
        )

    with open(filepath, "rb") as f:
        return pickle.load(f)


def top_k_accuracy(model, X, y, k=3):
    """
    Calculate Top-K accuracy.
    """

    probabilities = model.predict_proba(X)

    top_k_predictions = np.argsort(
        probabilities,
        axis=1
    )[:, -k:]

    correct = [
        y[i] in top_k_predictions[i]
        for i in range(len(y))
    ]

    return float(np.mean(correct))


def evaluate_model(model, X, y, label_encoder, dataset_name):
    """
    Evaluate model using Top-1, Top-3, Top-5 and
    classification metrics.
    """

    print_header(f"{dataset_name.upper()} EVALUATION")

    predictions = model.predict(X)

    top1 = accuracy_score(y, predictions)

    top3 = top_k_accuracy(
        model,
        X,
        y,
        k=3
    )

    top5 = top_k_accuracy(
        model,
        X,
        y,
        k=5
    )

    precision = precision_score(
        y,
        predictions,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y,
        predictions,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y,
        predictions,
        average="weighted",
        zero_division=0
    )

    print(f"Top-1 Accuracy : {top1 * 100:.2f}%")
    print(f"Top 3 Accuracy : {top3 * 100:.2f}%")
    print(f"Top 5 Accuracy : {top5 * 100:.2f}%")
    print(f"Precision      : {precision * 100:.2f}%")
    print(f"Recall         : {recall * 100:.2f}%")
    print(f"F1 Score       : {f1 * 100:.2f}%")

    print("\nClassification Report")

    report = classification_report(
        y,
        predictions,
        target_names=label_encoder.classes_,
        zero_division=0
    )

    print(report)

    print("Confusion Matrix")

    cm = confusion_matrix(
        y,
        predictions
    )

    print(cm)

    return {
        "top_1_accuracy": float(top1),
        "top_3_accuracy": float(top3),
        "top_5_accuracy": float(top5),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "classification_report": classification_report(
            y,
            predictions,
            target_names=label_encoder.classes_,
            zero_division=0,
            output_dict=True
        ),
        "confusion_matrix": cm.tolist()
    }


# ======================================================================
# MAIN
# ======================================================================

def main():

    start_time = time.time()

    print_header(
        "MILESTONE 2 - STEP 2\n"
        "XGBOOST WITH CROSS-VALIDATED HYPERPARAMETER TUNING"
    )

    # ==================================================================
    # CREATE MODEL DIRECTORY
    # ==================================================================

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    # ==================================================================
    # CHECK DATASET FILES
    # ==================================================================

    print_header("CHECKING DATASET FILES")

    for filepath in [
        TRAIN_FILE,
        VALIDATION_FILE,
        TEST_FILE
    ]:

        if os.path.exists(filepath):
            print(f"✓ {filepath}")
        else:
            raise FileNotFoundError(
                f"Missing dataset: {filepath}"
            )

    # ==================================================================
    # LOAD DATASETS
    # ==================================================================

    print_header("LOADING DATASETS")

    train_df = pd.read_csv(TRAIN_FILE)
    validation_df = pd.read_csv(VALIDATION_FILE)
    test_df = pd.read_csv(TEST_FILE)

    print(
        f"Training shape   : {train_df.shape}"
    )

    print(
        f"Validation shape : {validation_df.shape}"
    )

    print(
        f"Test shape       : {test_df.shape}"
    )

    # ==================================================================
    # CHECK REQUIRED COLUMNS
    # ==================================================================

    print_header("CHECKING REQUIRED COLUMNS")

    for df_name, df in [
        ("Training", train_df),
        ("Validation", validation_df),
        ("Test", test_df)
    ]:

        if TEXT_COLUMN not in df.columns:
            raise ValueError(
                f"{TEXT_COLUMN} missing from {df_name} dataset"
            )

        if TARGET_COLUMN not in df.columns:
            raise ValueError(
                f"{TARGET_COLUMN} missing from {df_name} dataset"
            )

    print(f"✓ {TEXT_COLUMN}")
    print(f"✓ {TARGET_COLUMN}")

    # ==================================================================
    # CLEAN TEXT
    # ==================================================================

    print_header("PREPARING TEXT DATA")

    def clean_dataframe(df):

        df = df.copy()

        df[TEXT_COLUMN] = (
            df[TEXT_COLUMN]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        df[TARGET_COLUMN] = (
            df[TARGET_COLUMN]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        df = df[
            (df[TEXT_COLUMN] != "") &
            (df[TARGET_COLUMN] != "")
        ]

        return df.reset_index(drop=True)

    train_df = clean_dataframe(train_df)
    validation_df = clean_dataframe(validation_df)
    test_df = clean_dataframe(test_df)

    print(
        f"Training records   : {len(train_df)}"
    )

    print(
        f"Validation records : {len(validation_df)}"
    )

    print(
        f"Test records       : {len(test_df)}"
    )

    # ==================================================================
    # TEXT AND LABELS
    # ==================================================================

    X_train_text = train_df[TEXT_COLUMN]
    X_validation_text = validation_df[TEXT_COLUMN]
    X_test_text = test_df[TEXT_COLUMN]

    y_train_text = train_df[TARGET_COLUMN]
    y_validation_text = validation_df[TARGET_COLUMN]
    y_test_text = test_df[TARGET_COLUMN]

    # ==================================================================
    # LABEL ENCODING
    # ==================================================================

    print_header("CAREER LABEL ENCODING")

    label_encoder = LabelEncoder()

    y_train = label_encoder.fit_transform(
        y_train_text
    )

    y_validation = label_encoder.transform(
        y_validation_text
    )

    y_test = label_encoder.transform(
        y_test_text
    )

    print(
        f"Number of career classes: "
        f"{len(label_encoder.classes_)}"
    )

    for index, career in enumerate(
        label_encoder.classes_
    ):
        print(
            f"{index:02d} -> {career}"
        )

    # ==================================================================
    # TF-IDF
    # ==================================================================

    print_header("TF-IDF FEATURE EXTRACTION")

    print(
        "Fitting TF-IDF on TRAINING data only..."
    )

    tfidf = TfidfVectorizer(
        max_features=3000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,
        sublinear_tf=True
    )

    X_train = tfidf.fit_transform(
        X_train_text
    )

    print(
        "Transforming validation data..."
    )

    X_validation = tfidf.transform(
        X_validation_text
    )

    print(
        "Transforming test data..."
    )

    X_test = tfidf.transform(
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

    # ==================================================================
    # XGBOOST BASE MODEL
    # ==================================================================

    print_header(
        "XGBOOST HYPERPARAMETER TUNING"
    )

    number_of_classes = len(
        label_encoder.classes_
    )

    print(
        f"Number of classes: {number_of_classes}"
    )

    print(
        "Starting 5-fold cross-validated "
        "GridSearchCV..."
    )

    print(
        "This may take several minutes."
    )

    # IMPORTANT:
    # objective is multiclass classification
    # num_class is the number of careers

    base_model = XGBClassifier(
        objective="multi:softprob",
        num_class=number_of_classes,

        eval_metric="mlogloss",

        tree_method="hist",

        random_state=42,

        n_jobs=-1,

        verbosity=0
    )

    # ==================================================================
    # PARAMETER GRID
    # ==================================================================

    param_grid = {

        "n_estimators": [
            200,
            300
        ],

        "max_depth": [
            6,
            8
        ],

        "learning_rate": [
            0.05,
            0.10
        ],

        "subsample": [
            0.8
        ],

        "colsample_bytree": [
            0.8
        ]
    }

    # ==================================================================
    # GRID SEARCH
    # ==================================================================

    grid_search = GridSearchCV(

        estimator=base_model,

        param_grid=param_grid,

        scoring="accuracy",

        cv=5,

        n_jobs=1,

        verbose=2,

        return_train_score=True
    )

    grid_start = time.time()

    grid_search.fit(
        X_train,
        y_train
    )

    grid_time = time.time() - grid_start

    # ==================================================================
    # BEST MODEL
    # ==================================================================

    best_model = grid_search.best_estimator_

    print_header(
        "BEST XGBOOST MODEL"
    )

    print("Best parameters:")

    for key, value in (
        grid_search.best_params_.items()
    ):
        print(
            f"{key}: {value}"
        )

    print(
        f"\nBest CV Accuracy: "
        f"{grid_search.best_score_ * 100:.2f}%"
    )

    print(
        f"Training time: "
        f"{grid_time:.2f} seconds"
    )

    # ==================================================================
    # TRAINING PERFORMANCE
    # ==================================================================

    print_header(
        "TRAINING PERFORMANCE"
    )

    train_predictions = best_model.predict(
        X_train
    )

    training_accuracy = accuracy_score(
        y_train,
        train_predictions
    )

    print(
        f"Training Accuracy: "
        f"{training_accuracy * 100:.2f}%"
    )

    # ==================================================================
    # VALIDATION
    # ==================================================================

    validation_metrics = evaluate_model(
        best_model,
        X_validation,
        y_validation,
        label_encoder,
        "Validation"
    )

    # ==================================================================
    # TEST
    # ==================================================================

    test_metrics = evaluate_model(
        best_model,
        X_test,
        y_test,
        label_encoder,
        "Test"
    )

    # ==================================================================
    # SAVE XGBOOST MODEL
    # ==================================================================

    print_header(
        "SAVING MODEL FILES"
    )

    save_pickle_verified(
        best_model,
        MODEL_FILE
    )

    save_pickle_verified(
        tfidf,
        TFIDF_FILE
    )

    save_pickle_verified(
        label_encoder,
        LABEL_ENCODER_FILE
    )

    # ==================================================================
    # FINAL MODEL FILE VERIFICATION
    # ==================================================================

    print_header(
        "FINAL MODEL FILE VERIFICATION"
    )

    # Reload XGBoost model
    reloaded_model = load_pickle(
        MODEL_FILE
    )

    print(
        f"✓ Verified: {MODEL_FILE}"
    )

    # Reload TF-IDF
    reloaded_tfidf = load_pickle(
        TFIDF_FILE
    )

    print(
        f"✓ Verified: {TFIDF_FILE}"
    )

    # Reload label encoder
    reloaded_label_encoder = load_pickle(
        LABEL_ENCODER_FILE
    )

    print(
        f"✓ Verified: "
        f"{LABEL_ENCODER_FILE}"
    )

    # ==================================================================
    # RELOAD TEST
    # ==================================================================

    reloaded_test_predictions = (
        reloaded_model.predict(
            X_test
        )
    )

    reloaded_test_accuracy = (
        accuracy_score(
            y_test,
            reloaded_test_predictions
        )
    )

    print(
        f"\nReloaded model test accuracy: "
        f"{reloaded_test_accuracy * 100:.2f}%"
    )

    if abs(
        reloaded_test_accuracy -
        test_metrics["top_1_accuracy"]
    ) > 1e-10:

        raise RuntimeError(
            "Reloaded model accuracy does not "
            "match original model."
        )

    print(
        "✓ Reloaded model produces "
        "identical test performance."
    )

    # ==================================================================
    # VERIFY TF-IDF
    # ==================================================================

    reloaded_test_features = (
        reloaded_tfidf.transform(
            X_test_text
        )
    )

    if (
        reloaded_test_features.shape
        != X_test.shape
    ):

        raise RuntimeError(
            "Reloaded TF-IDF feature shape "
            "does not match."
        )

    print(
        "✓ Reloaded TF-IDF verified."
    )

    # ==================================================================
    # VERIFY LABEL ENCODER
    # ==================================================================

    if not np.array_equal(
        reloaded_label_encoder.classes_,
        label_encoder.classes_
    ):

        raise RuntimeError(
            "Reloaded Label Encoder "
            "does not match."
        )

    print(
        "✓ Reloaded Label Encoder verified."
    )

    # ==================================================================
    # SAVE METRICS
    # ==================================================================

    total_time = time.time() - start_time

    metrics = {

        "milestone": "Milestone 2",

        "step": "Step 2 - XGBoost",

        "model": "XGBoost",

        "dataset": {
            "train_samples": int(len(train_df)),
            "validation_samples": int(
                len(validation_df)
            ),
            "test_samples": int(
                len(test_df)
            )
        },

        "number_of_classes": int(
            number_of_classes
        ),

        "classes": (
            label_encoder.classes_.tolist()
        ),

        "tfidf_features": int(
            X_train.shape[1]
        ),

        "best_parameters": {
            str(k): (
                v.item()
                if hasattr(v, "item")
                else v
            )
            for k, v in
            grid_search.best_params_.items()
        },

        "training_accuracy": float(
            training_accuracy
        ),

        "best_cv_accuracy": float(
            grid_search.best_score_
        ),

        "validation": {
            "top_1_accuracy":
                validation_metrics[
                    "top_1_accuracy"
                ],

            "top_3_accuracy":
                validation_metrics[
                    "top_3_accuracy"
                ],

            "top_5_accuracy":
                validation_metrics[
                    "top_5_accuracy"
                ],

            "precision":
                validation_metrics[
                    "precision"
                ],

            "recall":
                validation_metrics[
                    "recall"
                ],

            "f1_score":
                validation_metrics[
                    "f1_score"
                ]
        },

        "test": {
            "top_1_accuracy":
                test_metrics[
                    "top_1_accuracy"
                ],

            "top_3_accuracy":
                test_metrics[
                    "top_3_accuracy"
                ],

            "top_5_accuracy":
                test_metrics[
                    "top_5_accuracy"
                ],

            "precision":
                test_metrics[
                    "precision"
                ],

            "recall":
                test_metrics[
                    "recall"
                ],

            "f1_score":
                test_metrics[
                    "f1_score"
                ]
        },

        "training_time_seconds": float(
            grid_time
        ),

        "total_execution_time_seconds":
            float(total_time)
    }

    with open(
        METRICS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metrics,
            f,
            indent=4
        )

    print(
        f"✓ Saved: {METRICS_FILE}"
    )

    # ==================================================================
    # FINAL SUMMARY
    # ==================================================================

    print_header(
        "MILESTONE 2 - STEP 2 COMPLETE"
    )

    print(
        f"Training Accuracy : "
        f"{training_accuracy * 100:.2f}%"
    )

    print(
        f"CV Mean Accuracy  : "
        f"{grid_search.best_score_ * 100:.2f}%"
    )

    print(
        f"Validation Top-1 : "
        f"{validation_metrics['top_1_accuracy'] * 100:.2f}%"
    )

    print(
        f"Validation Top-3 : "
        f"{validation_metrics['top_3_accuracy'] * 100:.2f}%"
    )

    print(
        f"Validation Top-5 : "
        f"{validation_metrics['top_5_accuracy'] * 100:.2f}%"
    )

    print(
        f"Test Top-1       : "
        f"{test_metrics['top_1_accuracy'] * 100:.2f}%"
    )

    print(
        f"Test Top-3       : "
        f"{test_metrics['top_3_accuracy'] * 100:.2f}%"
    )

    print(
        f"Test Top-5       : "
        f"{test_metrics['top_5_accuracy'] * 100:.2f}%"
    )

    print(
        f"Test F1          : "
        f"{test_metrics['f1_score'] * 100:.2f}%"
    )

    print("\nVerified files:")

    print(
        f"  ✓ {MODEL_FILE}"
    )

    print(
        f"  ✓ {TFIDF_FILE}"
    )

    print(
        f"  ✓ {LABEL_ENCODER_FILE}"
    )

    print(
        f"  ✓ {METRICS_FILE}"
    )

    print(
        f"\nTotal execution time: "
        f"{total_time:.2f} seconds"
    )

    print(
        "\n✓ XGBOOST MODEL VERIFIED"
    )

    print(
        "✓ MILESTONE 2 - STEP 2 COMPLETED"
    )

    print("=" * 70)


# ======================================================================
# RUN
# ======================================================================

if __name__ == "__main__":
    main()