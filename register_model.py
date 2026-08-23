"""
CareerCast - MLflow Model Registry

Registers the best Random Forest model in the MLflow Model Registry.

Requirements:
    - mlflow_tracking.py must have been executed successfully
    - mlflow.db must exist
    - Random Forest model must already be logged
"""

import mlflow
from mlflow.tracking import MlflowClient


# ============================================================
# CONFIGURATION
# ============================================================

TRACKING_URI = "sqlite:///mlflow.db"

EXPERIMENT_NAME = "CareerCast Career Prediction"

MODEL_NAME = "CareerCast-RandomForest"


# ============================================================
# MLflow configuration
# ============================================================

print("\n========================================")
print("CAREERCAST MLflow MODEL REGISTRY")
print("========================================")

print("\nSetting MLflow tracking URI...")

mlflow.set_tracking_uri(TRACKING_URI)

print("Tracking URI:", TRACKING_URI)


# ============================================================
# Get experiment
# ============================================================

print("\nSearching for MLflow experiment...")

experiment = mlflow.get_experiment_by_name(
    EXPERIMENT_NAME
)

if experiment is None:

    raise RuntimeError(
        f"MLflow experiment not found: {EXPERIMENT_NAME}"
    )


print("Experiment found:")
print("Experiment ID:", experiment.experiment_id)
print("Experiment name:", experiment.name)


# ============================================================
# Find latest successful run
# ============================================================

print("\nSearching for Random Forest runs...")

client = MlflowClient()

runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["start_time DESC"]
)


if not runs:

    raise RuntimeError(
        "No MLflow runs found."
    )


# ============================================================
# Select Random Forest run
# ============================================================

random_forest_run = None

for run in runs:

    params = run.data.params

    model_type = params.get(
        "model_type",
        ""
    )

    if model_type.lower() == "random forest":

        random_forest_run = run

        break


if random_forest_run is None:

    raise RuntimeError(
        "No Random Forest MLflow run was found."
    )


run_id = random_forest_run.info.run_id


print("\nRandom Forest run found.")

print("Run ID:", run_id)

print(
    "Run status:",
    random_forest_run.info.status
)


# ============================================================
# Display metrics
# ============================================================

metrics = random_forest_run.data.metrics

print("\nModel metrics:")

for metric_name, metric_value in metrics.items():

    print(
        f"{metric_name}: {metric_value}"
    )


# ============================================================
# Verify model artifact
# ============================================================

print("\nChecking model artifact...")

artifact_uri = (
    f"runs:/{run_id}/random_forest_model"
)

print(
    "Model artifact URI:",
    artifact_uri
)


# ============================================================
# Create registered model
# ============================================================

print("\nChecking Model Registry...")

try:

    registered_model = client.get_registered_model(
        MODEL_NAME
    )

    print(
        "Registered model already exists:",
        MODEL_NAME
    )

except Exception:

    print(
        "Registered model does not exist."
    )

    print(
        "Creating registered model..."
    )

    registered_model = client.create_registered_model(
        MODEL_NAME,
        description=(
            "CareerCast Random Forest career "
            "prediction model for Milestone 3."
        )
    )

    print(
        "Registered model created successfully."
    )


# ============================================================
# Create model version
# ============================================================

print("\nCreating model version...")

model_version = client.create_model_version(
    name=MODEL_NAME,
    source=artifact_uri,
    run_id=run_id
)


print("\n========================================")
print("MODEL REGISTRATION SUCCESSFUL")
print("========================================")

print(
    "Model name:",
    MODEL_NAME
)

print(
    "Model version:",
    model_version.version
)

print(
    "Run ID:",
    run_id
)

print(
    "Source:",
    model_version.source
)

print("========================================")


# ============================================================
# Add model version description
# ============================================================

client.update_model_version(
    name=MODEL_NAME,
    version=model_version.version,
    description=(
        "Random Forest career prediction model "
        "registered from the CareerCast Milestone 3 "
        "MLflow experiment."
    )
)


# ============================================================
# Final verification
# ============================================================

print("\nVerifying registered model...")

versions = client.search_model_versions(
    f"name='{MODEL_NAME}'"
)


print(
    f"\nTotal registered versions: {len(versions)}"
)

for version in versions:

    print(
        f"Version {version.version} | "
        f"Run ID: {version.run_id} | "
        f"Status: {version.status}"
    )


print("\n========================================")
print("MLflow Model Registry completed.")
print("========================================")