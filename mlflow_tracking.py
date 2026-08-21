import os
import json
import joblib

import mlflow
import mlflow.sklearn
import mlflow.xgboost


# ============================================================
# CAREERCAST - MILESTONE 3
# STEP 4 - MLFLOW MODEL REGISTRY
# ============================================================

print("=" * 70)
print("CAREERCAST - MILESTONE 3")
print("STEP 4 - MLFLOW MODEL REGISTRY")
print("=" * 70)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

MLFLOW_DB = os.path.join(
    BASE_DIR,
    "mlflow.db"
)

EXPERIMENT_NAME = "CareerCast-Milestone3"


# ============================================================
# MLFLOW TRACKING CONFIGURATION
# ============================================================

TRACKING_URI = (
    "sqlite:///"
    + MLFLOW_DB
)

mlflow.set_tracking_uri(
    TRACKING_URI
)

mlflow.set_experiment(
    EXPERIMENT_NAME
)


print()
print("MLflow tracking backend:")
print(TRACKING_URI)

print()
print("Experiment:")
print(EXPERIMENT_NAME)

print()
print("=" * 70)


# ============================================================
# FILE HELPER
# ============================================================

def model_file(filename):

    return os.path.join(
        MODEL_DIR,
        filename
    )


# ============================================================
# JSON METRICS LOADER
# ============================================================

def load_metrics(filename):

    path = model_file(
        filename
    )

    if not os.path.exists(path):

        print(
            f"⚠ Metrics file not found: {filename}"
        )

        return {}

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, dict):

            return data

        return {}

    except Exception as error:

        print(
            f"⚠ Could not load {filename}: {error}"
        )

        return {}


# ============================================================
# SAFE METRIC LOGGER
# ============================================================

def log_numeric_metrics(metrics):

    if not isinstance(
        metrics,
        dict
    ):

        return

    for key, value in metrics.items():

        # Ignore nested dictionaries/lists
        if isinstance(
            value,
            bool
        ):

            continue

        if isinstance(
            value,
            (int, float)
        ):

            try:

                mlflow.log_metric(
                    str(key),
                    float(value)
                )

            except Exception as error:

                print(
                    f"⚠ Could not log metric "
                    f"{key}: {error}"
                )


# ============================================================
# LOG COMMON PARAMETERS
# ============================================================

def log_common_parameters(
    model_type,
    model_filename
):

    mlflow.log_param(
        "project",
        "CareerCast"
    )

    mlflow.log_param(
        "milestone",
        "Milestone 3"
    )

    mlflow.log_param(
        "model_type",
        model_type
    )

    mlflow.log_param(
        "model_file",
        model_filename
    )

    mlflow.log_param(
        "python_environment",
        "Python 3.12"
    )


# ============================================================
# 1. LOGISTIC REGRESSION
# ============================================================

def register_logistic_regression():

    print()
    print(
        "REGISTERING LOGISTIC REGRESSION"
    )
    print("-" * 70)

    filename = "logistic_regression.pkl"

    path = model_file(
        filename
    )

    # --------------------------------------------------------
    # CHECK EXISTING MODEL
    # --------------------------------------------------------

    if not os.path.exists(path):

        print(
            f"✗ Model not found: {path}"
        )

        return False

    try:

        # ----------------------------------------------------
        # LOAD EXISTING MODEL
        # ----------------------------------------------------

        model = joblib.load(
            path
        )

        print(
            "✓ Existing Logistic Regression model loaded"
        )

        print(
            "Model type:",
            type(model)
        )

        # ----------------------------------------------------
        # LOAD EXISTING METRICS
        # ----------------------------------------------------

        metrics = load_metrics(
            "logistic_regression_metrics.json"
        )

        # ----------------------------------------------------
        # CREATE MLFLOW RUN
        # ----------------------------------------------------

        with mlflow.start_run(
            run_name="Logistic-Regression"
        ) as run:

            log_common_parameters(
                "Logistic Regression",
                filename
            )

            # ------------------------------------------------
            # LOG EXISTING METRICS
            # ------------------------------------------------

            log_numeric_metrics(
                metrics
            )

            # ------------------------------------------------
            # LOG EXISTING MODEL
            #
            # IMPORTANT:
            # We explicitly use PICKLE serialization.
            #
            # This does NOT retrain the model.
            # It simply registers the existing .pkl model.
            # ------------------------------------------------

            mlflow.sklearn.log_model(
                sk_model=model,
                name="logistic_regression",
                serialization_format="pickle",
                registered_model_name=(
                    "CareerCast-LogisticRegression"
                )
            )

            print()
            print(
                "✓ Logistic Regression registered"
            )

            print(
                "Run ID:",
                run.info.run_id
            )

            return True

    except Exception as error:

        print()
        print(
            "✗ Logistic Regression registration failed"
        )

        print(
            "Error:",
            error
        )

        return False


# ============================================================
# 2. RANDOM FOREST
# ============================================================

def register_random_forest():

    print()
    print(
        "REGISTERING RANDOM FOREST"
    )
    print("-" * 70)

    filename = "random_forest.pkl"

    path = model_file(
        filename
    )

    # --------------------------------------------------------
    # CHECK EXISTING MODEL
    # --------------------------------------------------------

    if not os.path.exists(path):

        print(
            f"✗ Model not found: {path}"
        )

        return False

    try:

        # ----------------------------------------------------
        # LOAD EXISTING MODEL
        # ----------------------------------------------------

        model = joblib.load(
            path
        )

        print(
            "✓ Existing Random Forest model loaded"
        )

        print(
            "Model type:",
            type(model)
        )

        # ----------------------------------------------------
        # LOAD EXISTING METRICS
        # ----------------------------------------------------

        metrics = load_metrics(
            "random_forest_metrics.json"
        )

        # ----------------------------------------------------
        # CREATE MLFLOW RUN
        # ----------------------------------------------------

        with mlflow.start_run(
            run_name="Random-Forest"
        ) as run:

            log_common_parameters(
                "Random Forest",
                filename
            )

            # ------------------------------------------------
            # LOG EXISTING METRICS
            # ------------------------------------------------

            log_numeric_metrics(
                metrics
            )

            # ------------------------------------------------
            # LOG EXISTING MODEL
            #
            # No retraining.
            # ------------------------------------------------

            mlflow.sklearn.log_model(
                sk_model=model,
                name="random_forest",
                serialization_format="pickle",
                registered_model_name=(
                    "CareerCast-RandomForest"
                )
            )

            print()
            print(
                "✓ Random Forest registered"
            )

            print(
                "Run ID:",
                run.info.run_id
            )

            return True

    except Exception as error:

        print()
        print(
            "✗ Random Forest registration failed"
        )

        print(
            "Error:",
            error
        )

        return False


# ============================================================
# 3. XGBOOST
# ============================================================

def register_xgboost():

    print()
    print(
        "REGISTERING XGBOOST"
    )
    print("-" * 70)

    filename = "xgboost.pkl"

    path = model_file(
        filename
    )

    # --------------------------------------------------------
    # CHECK EXISTING MODEL
    # --------------------------------------------------------

    if not os.path.exists(path):

        print(
            f"✗ Model not found: {path}"
        )

        return False

    try:

        import xgboost

        # ----------------------------------------------------
        # LOAD EXISTING XGBOOST MODEL
        # ----------------------------------------------------

        model = joblib.load(
            path
        )

        print(
            "✓ Existing XGBoost model loaded"
        )

        print(
            "Model type:",
            type(model)
        )

        print(
            "XGBoost version:",
            xgboost.__version__
        )

        # ----------------------------------------------------
        # LOAD EXISTING METRICS
        # ----------------------------------------------------

        metrics = load_metrics(
            "xgboost_metrics.json"
        )

        # ----------------------------------------------------
        # CREATE MLFLOW RUN
        # ----------------------------------------------------

        with mlflow.start_run(
            run_name="XGBoost"
        ) as run:

            log_common_parameters(
                "XGBoost",
                filename
            )

            mlflow.log_param(
                "xgboost_version",
                xgboost.__version__
            )

            mlflow.log_param(
                "serialization",
                "native_xgboost"
            )

            mlflow.log_param(
                "model_format",
                "json"
            )

            # ------------------------------------------------
            # LOG EXISTING METRICS
            # ------------------------------------------------

            log_numeric_metrics(
                metrics
            )

            # ------------------------------------------------
            # XGBOOST NATIVE MLFLOW FLAVOR
            #
            # This avoids the skops trusted-type problem.
            #
            # No retraining.
            # ------------------------------------------------

            mlflow.xgboost.log_model(
                xgb_model=model,
                name="xgboost",
                model_format="json",
                registered_model_name=(
                    "CareerCast-XGBoost"
                )
            )

            print()
            print(
                "✓ XGBoost registered"
            )

            print(
                "Run ID:",
                run.info.run_id
            )

            return True

    except Exception as error:

        print()
        print(
            "✗ XGBoost registration failed"
        )

        print(
            "Error:",
            error
        )

        return False


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print()

    # ========================================================
    # CHECK MODEL DIRECTORY
    # ========================================================

    if not os.path.exists(
        MODEL_DIR
    ):

        print(
            "✗ Models directory not found:"
        )

        print(
            MODEL_DIR
        )

        raise SystemExit(1)

    print(
        "Model directory:"
    )

    print(
        MODEL_DIR
    )

    print()
    print(
        "Existing trained models will be loaded."
    )

    print(
        "NO MODEL WILL BE RETRAINED."
    )

    print()
    print("=" * 70)

    # ========================================================
    # REGISTER MODELS
    # ========================================================

    logistic_success = (
        register_logistic_regression()
    )

    random_forest_success = (
        register_random_forest()
    )

    xgboost_success = (
        register_xgboost()
    )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print()
    print("=" * 70)
    print(
        "MLFLOW MODEL REGISTRATION SUMMARY"
    )
    print("=" * 70)

    print(
        "Logistic Regression :",
        "✓ SUCCESS"
        if logistic_success
        else "✗ FAILED"
    )

    print(
        "Random Forest       :",
        "✓ SUCCESS"
        if random_forest_success
        else "✗ FAILED"
    )

    print(
        "XGBoost             :",
        "✓ SUCCESS"
        if xgboost_success
        else "✗ FAILED"
    )

    print()
    print(
        "MLflow database:"
    )

    print(
        MLFLOW_DB
    )

    print()
    print("=" * 70)

    if (
        logistic_success
        and
        random_forest_success
        and
        xgboost_success
    ):

        print(
            "✓ ALL THREE MODELS REGISTERED SUCCESSFULLY"
        )

        print(
            "✓ NO MODEL RETRAINING WAS PERFORMED"
        )

    else:

        print(
            "⚠ ONE OR MORE MODELS FAILED REGISTRATION"
        )

        print(
            "Check the error shown above."
        )

    print("=" * 70)