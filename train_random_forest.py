import os
import json
import pickle
import shutil
import time

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


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
# UTILITY FUNCTIONS
# ============================================================

def print_header(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def atomic_pickle_save(obj, final_path):
    """
    Save pickle to temporary file first.
    Verify that temporary file can be loaded.
    Only then replace the final file.
    """

    temp_path = final_path + ".tmp"

    # Remove stale temporary file
    if os.path.exists(temp_path):
        os.remove(temp_path)

    # Write temporary pickle
    with open(temp_path, "wb") as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)

    # Verify temporary pickle
    try:
        with open(temp_path, "rb") as f:
            pickle.load(f)
    except Exception as e:
        print(f"ERROR: Temporary file verification failed: {e}")

        if os.path.exists(temp_path):
            os.remove(temp_path)

        raise RuntimeError(
            f"Could not verify saved object: {final_path}"
        )

    # Atomic replacement
    os.replace(temp_path, final_path)

    print(f"✓ Saved and verified: {final_path}")


def load_pickle_verified(path):
    """
    Load and verify a pickle file.
    """

    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(path, "rb") as f:
        obj = pickle.load(f)

    print(f"✓ Verified: {path}")

    return obj


def evaluate_model(model, X, y, label_encoder, dataset_name):
    """
    Evaluate model using Top-1, Top-3 and Top-5.
    """

    print_header(f"{dataset_name.upper()} EVALUATION")

    predictions = model.predict(X)

    top1_accuracy = accuracy_score(y, predictions)

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

    # Probability-based Top-K
    probabilities = model.predict_proba(X)

    top_k_results = {}

    for k in [3, 5]:

        k = min(k, probabilities.shape[1])

        top_k_indices = np.argsort(
            probabilities,
            axis=1
        )[:, -k:]

        correct = np.array([
            y[i] in top_k_indices[i]
            for i in range(len(y))
        ])

        top_k_results[f"top_{k}_accuracy"] = float(
            np.mean(correct)
        )

    print(f"Top-1 Accuracy : {top1_accuracy * 100:.2f}%")

    for key, value in top_k_results.items():
        print(
            f"{key.replace('_', ' ').title()} : "
            f"{value * 100:.2f}%"
        )

    print(f"Precision      : {precision * 100:.2f}%")
    print(f"Recall         : {recall * 100:.2f}%")
    print(f"F1 Score       : {f1 * 100:.2f}%")

    print()
    print("Classification Report")
    print(
        classification_report(
            y,
            predictions,
            target_names=label_encoder.classes_,
            zero_division=0
        )
    )

    print("Confusion Matrix")
    print(confusion_matrix(y, predictions))

    return {
        "top_1_accuracy": float(top1_accuracy),
        **top_k_results,
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1)
    }


# ============================================================
# MAIN
# ============================================================

def main():

    total_start = time.time()

    print_header(
        "MILESTONE 2 - STEP 1\n"
        "RANDOM FOREST WITH CROSS-VALIDATED HYPERPARAMETER TUNING"
    )

    # --------------------------------------------------------
    # Create model directory
    # --------------------------------------------------------

    os.makedirs(MODEL_DIR, exist_ok=True)

    # --------------------------------------------------------
    # Check datasets
    # --------------------------------------------------------

    print_header("CHECKING DATASET FILES")

    for file_path in [
        TRAIN_FILE,
        VALIDATION_FILE,
        TEST_FILE
    ]:

        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            raise FileNotFoundError(
                f"Required dataset not found: {file_path}"
            )

    # --------------------------------------------------------
    # Load datasets
    # --------------------------------------------------------

    print_header("LOADING DATASETS")

    train_df = pd.read_csv(TRAIN_FILE)
    validation_df = pd.read_csv(VALIDATION_FILE)
    test_df = pd.read_csv(TEST_FILE)

    print(f"Training shape   : {train_df.shape}")
    print(f"Validation shape : {validation_df.shape}")
    print(f"Test shape       : {test_df.shape}")

    # --------------------------------------------------------
    # Check columns
    # --------------------------------------------------------

    print_header("CHECKING REQUIRED COLUMNS")

    for df_name, df in [
        ("Training", train_df),
        ("Validation", validation_df),
        ("Test", test_df)
    ]:

        if TEXT_COLUMN not in df.columns:
            raise ValueError(
                f"{TEXT_COLUMN} missing from {df_name}"
            )

        if TARGET_COLUMN not in df.columns:
            raise ValueError(
                f"{TARGET_COLUMN} missing from {df_name}"
            )

    print(f"✓ {TEXT_COLUMN}")
    print(f"✓ {TARGET_COLUMN}")

    # --------------------------------------------------------
    # Prepare text
    # --------------------------------------------------------

    print_header("PREPARING TEXT DATA")

    train_df[TEXT_COLUMN] = (
        train_df[TEXT_COLUMN]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    validation_df[TEXT_COLUMN] = (
        validation_df[TEXT_COLUMN]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    test_df[TEXT_COLUMN] = (
        test_df[TEXT_COLUMN]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Remove empty training records
    train_df = train_df[
        train_df[TEXT_COLUMN].str.len() > 0
    ].copy()

    validation_df = validation_df[
        validation_df[TEXT_COLUMN].str.len() > 0
    ].copy()

    test_df = test_df[
        test_df[TEXT_COLUMN].str.len() > 0
    ].copy()

    print(f"Training records   : {len(train_df)}")
    print(f"Validation records : {len(validation_df)}")
    print(f"Test records       : {len(test_df)}")

    # --------------------------------------------------------
    # Label encoding
    # --------------------------------------------------------

    print_header("CAREER LABEL ENCODING")

    label_encoder = LabelEncoder()

    y_train = label_encoder.fit_transform(
        train_df[TARGET_COLUMN]
    )

    y_validation = label_encoder.transform(
        validation_df[TARGET_COLUMN]
    )

    y_test = label_encoder.transform(
        test_df[TARGET_COLUMN]
    )

    print(
        f"Number of career classes: "
        f"{len(label_encoder.classes_)}"
    )

    print()

    for index, career in enumerate(label_encoder.classes_):
        print(f"{index:02d} -> {career}")

    # --------------------------------------------------------
    # TF-IDF
    # --------------------------------------------------------

    print_header("TF-IDF FEATURE EXTRACTION")

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000,
        sublinear_tf=True
    )

    print("Fitting TF-IDF on TRAINING data only...")

    X_train = vectorizer.fit_transform(
        train_df[TEXT_COLUMN]
    )

    print("Transforming validation data...")

    X_validation = vectorizer.transform(
        validation_df[TEXT_COLUMN]
    )

    print("Transforming test data...")

    X_test = vectorizer.transform(
        test_df[TEXT_COLUMN]
    )

    print()
    print(f"Training feature matrix   : {X_train.shape}")
    print(
        f"Validation feature matrix : "
        f"{X_validation.shape}"
    )
    print(f"Test feature matrix       : {X_test.shape}")

    # --------------------------------------------------------
    # Random Forest
    # --------------------------------------------------------

    print_header(
        "RANDOM FOREST HYPERPARAMETER TUNING"
    )

    rf = RandomForestClassifier(
        random_state=RANDOM_STATE,
        n_jobs=-1,
        class_weight=None
    )

    # Controlled grid
    param_grid = {
        "n_estimators": [200, 300],
        "max_depth": [None, 30],
        "min_samples_split": [2, 5],
        "min_samples_leaf": [1, 2],
        "max_features": ["sqrt"]
    }

    # This gives 16 combinations.
    #
    # 5-fold CV = 80 fits.

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE
    )

    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        scoring="accuracy",
        cv=cv,
        n_jobs=-1,
        verbose=2,
        return_train_score=True
    )

    print(
        "Starting 5-fold cross-validated "
        "GridSearchCV..."
    )

    print(
        "This may take several minutes."
    )

    training_start = time.time()

    grid_search.fit(
        X_train,
        y_train
    )

    training_time = time.time() - training_start

    # --------------------------------------------------------
    # Best model
    # --------------------------------------------------------

    print_header("BEST RANDOM FOREST MODEL")

    best_model = grid_search.best_estimator_

    print("Best parameters:")

    for parameter, value in (
        grid_search.best_params_.items()
    ):
        print(f"{parameter}: {value}")

    print(
        f"\nBest CV Accuracy: "
        f"{grid_search.best_score_ * 100:.2f}%"
    )

    print(
        f"Training time: "
        f"{training_time:.2f} seconds"
    )

    # --------------------------------------------------------
    # Training performance
    # --------------------------------------------------------

    print_header("TRAINING PERFORMANCE")

    train_predictions = best_model.predict(X_train)

    train_accuracy = accuracy_score(
        y_train,
        train_predictions
    )

    print(
        f"Training Accuracy: "
        f"{train_accuracy * 100:.2f}%"
    )

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    validation_metrics = evaluate_model(
        best_model,
        X_validation,
        y_validation,
        label_encoder,
        "Validation"
    )

    # --------------------------------------------------------
    # Test
    # --------------------------------------------------------

    test_metrics = evaluate_model(
        best_model,
        X_test,
        y_test,
        label_encoder,
        "Test"
    )

    # --------------------------------------------------------
    # Save model files
    # --------------------------------------------------------

    print_header("SAVING MODEL FILES")

    model_path = os.path.join(
        MODEL_DIR,
        "random_forest.pkl"
    )

    tfidf_path = os.path.join(
        MODEL_DIR,
        "random_forest_tfidf.pkl"
    )

    encoder_path = os.path.join(
        MODEL_DIR,
        "random_forest_label_encoder.pkl"
    )

    metrics_path = os.path.join(
        MODEL_DIR,
        "random_forest_metrics.json"
    )

    # Save and verify model
    atomic_pickle_save(
        best_model,
        model_path
    )

    # Save and verify TF-IDF
    atomic_pickle_save(
        vectorizer,
        tfidf_path
    )

    # Save and verify Label Encoder
    atomic_pickle_save(
        label_encoder,
        encoder_path
    )

    # --------------------------------------------------------
    # Verify saved objects AGAIN
    # --------------------------------------------------------

    print_header(
        "FINAL MODEL FILE VERIFICATION"
    )

    verified_model = load_pickle_verified(
        model_path
    )

    verified_tfidf = load_pickle_verified(
        tfidf_path
    )

    verified_encoder = load_pickle_verified(
        encoder_path
    )

    # Test the loaded model
    verification_predictions = (
        verified_model.predict(X_test)
    )

    verification_accuracy = accuracy_score(
        y_test,
        verification_predictions
    )

    print(
        f"\nReloaded model test accuracy: "
        f"{verification_accuracy * 100:.2f}%"
    )

    if abs(
        verification_accuracy
        - test_metrics["top_1_accuracy"]
    ) > 1e-10:

        raise RuntimeError(
            "Reloaded model accuracy does not "
            "match original model accuracy."
        )

    print(
        "✓ Reloaded model produces identical "
        "test performance."
    )

    # Verify TF-IDF
    transformed_test = verified_tfidf.transform(
        test_df[TEXT_COLUMN]
    )

    if transformed_test.shape != X_test.shape:
        raise RuntimeError(
            "Reloaded TF-IDF produced a different "
            "feature shape."
        )

    print("✓ Reloaded TF-IDF verified.")

    # Verify encoder
    if not np.array_equal(
        verified_encoder.classes_,
        label_encoder.classes_
    ):
        raise RuntimeError(
            "Reloaded Label Encoder does not match."
        )

    print("✓ Reloaded Label Encoder verified.")

    # --------------------------------------------------------
    # Metrics JSON
    # --------------------------------------------------------

    metrics = {

        "milestone": "Milestone 2",

        "step": "Step 1 - Random Forest",

        "model": "Random Forest",

        "random_state": RANDOM_STATE,

        "dataset": {
            "train_samples": int(len(train_df)),
            "validation_samples": int(
                len(validation_df)
            ),
            "test_samples": int(len(test_df))
        },

        "features": {
            "text_column": TEXT_COLUMN,
            "target_column": TARGET_COLUMN,
            "tfidf_features": int(
                X_train.shape[1]
            )
        },

        "career_classes": [
            str(x)
            for x in label_encoder.classes_
        ],

        "hyperparameter_tuning": {

            "cv_folds": 5,

            "best_parameters": {
                key: (
                    value.item()
                    if hasattr(value, "item")
                    else value
                )
                for key, value
                in grid_search.best_params_.items()
            },

            "best_cv_accuracy": float(
                grid_search.best_score_
            ),

            "training_time_seconds": float(
                training_time
            )
        },

        "training_metrics": {
            "accuracy": float(train_accuracy)
        },

        "validation_metrics":
            validation_metrics,

        "test_metrics":
            test_metrics,

        "verification": {
            "model_reload_success": True,
            "tfidf_reload_success": True,
            "label_encoder_reload_success": True,
            "reloaded_test_accuracy": float(
                verification_accuracy
            )
        }
    }

    # JSON is written atomically too
    temp_metrics = metrics_path + ".tmp"

    with open(
        temp_metrics,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metrics,
            f,
            indent=4
        )

    os.replace(
        temp_metrics,
        metrics_path
    )

    print(
        f"✓ Saved: {metrics_path}"
    )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    total_time = time.time() - total_start

    print_header(
        "MILESTONE 2 - STEP 1 COMPLETE"
    )

    print(
        f"Training Accuracy : "
        f"{train_accuracy * 100:.2f}%"
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

    print()
    print("Verified files:")

    print(
        "  ✓ models/random_forest.pkl"
    )

    print(
        "  ✓ models/random_forest_tfidf.pkl"
    )

    print(
        "  ✓ models/random_forest_label_encoder.pkl"
    )

    print(
        "  ✓ models/random_forest_metrics.json"
    )

    print()
    print(
        f"Total execution time: "
        f"{total_time:.2f} seconds"
    )

    print()
    print(
        "✓ RANDOM FOREST MODEL VERIFIED"
    )

    print(
        "✓ MILESTONE 2 - STEP 1 COMPLETED"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()