"""
CareerCast - MLflow Experiment Tracking

Tracks:
- Model name
- Accuracy
- Precision
- Recall
- F1 score
- Model parameters
- Model artifact
"""

import os
import joblib
import mlflow
import mlflow.sklearn

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

MODELS_DIR = os.path.join(PROJECT_ROOT, "models")

MLFLOW_DIR = os.path.join(PROJECT_ROOT, "mlruns")

MODEL_PATH = os.path.join(
    MODELS_DIR,
    "random_forest.pkl"
)

TEST_DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "test.csv"
)


# ============================================================
# MLflow configuration
# ============================================================

mlflow.set_tracking_uri(
    "sqlite:///mlflow.db"
)

mlflow.set_experiment(
    "CareerCast Career Prediction"
)


# ============================================================
# Load model
# ============================================================

print("\nLoading Random Forest model...")

model = joblib.load(MODEL_PATH)

print("Model loaded successfully.")
print(type(model))


# ============================================================
# Inspect model
# ============================================================

print("\nModel information:")

print("Model type:", type(model).__name__)

if hasattr(model, "get_params"):
    params = model.get_params()

    print("\nModel parameters:")

    for key, value in params.items():
        print(f"{key}: {value}")


# ============================================================
# NOTE
# ============================================================

print(
    "\nMLflow model registration requires the same "
    "evaluation pipeline used during model training."
)

print(
    "First we will verify the existing model artifacts "
    "and metrics before registering the model."
)


# ============================================================
# Start MLflow run
# ============================================================

with mlflow.start_run(
    run_name="Random Forest - Milestone 3"
) as run:

    print("\nMLflow Run Started")

    print("Run ID:", run.info.run_id)

    # --------------------------------------------------------
    # Log model type
    # --------------------------------------------------------

    mlflow.log_param(
        "model_type",
        "Random Forest"
    )

    mlflow.log_param(
        "milestone",
        "Milestone 3"
    )

    mlflow.log_param(
        "framework",
        "scikit-learn"
    )

    # --------------------------------------------------------
    # Log model parameters
    # --------------------------------------------------------

    if hasattr(model, "get_params"):

        params = model.get_params()

        for key, value in params.items():

            try:
                mlflow.log_param(
                    key,
                    str(value)
                )
            except Exception:
                pass

    # --------------------------------------------------------
    # Log model artifact
    # --------------------------------------------------------

    mlflow.sklearn.log_model(
        model,
        artifact_path="random_forest_model"
    )

    print(
        "\nRandom Forest model logged successfully."
    )

    # --------------------------------------------------------
    # Log local model file
    # --------------------------------------------------------

    if os.path.exists(MODEL_PATH):

        mlflow.log_artifact(
            MODEL_PATH,
            artifact_path="model_files"
        )

        print(
            "Model file logged successfully."
        )

    print("\nMLflow tracking completed.")