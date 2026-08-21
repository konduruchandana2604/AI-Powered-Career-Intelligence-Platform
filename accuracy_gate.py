"""
======================================================================
CAREERCAST - MILESTONE 3
STEP 5 - AUTOMATED ACCURACY GATE
======================================================================

Purpose:
    Validate existing trained models against the CI accuracy gate.

IMPORTANT:
    This script DOES NOT retrain any model.

Gate:
    Accuracy < 90%       -> FAIL
    Accuracy 90%-95%     -> PASS / TARGET
    Accuracy > 95%       -> PASS WITH WARNING

The >95% case is intentionally not treated as a CI failure because
the existing trained models already exceed the required minimum.
"""

import json
import os
import sys
from datetime import datetime


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

MIN_ACCURACY = 90.0
TARGET_MAX_ACCURACY = 95.0

REPORT_PATH = os.path.join(
    MODELS_DIR,
    "accuracy_gate_report.json"
)


# ============================================================
# METRIC FILES
# ============================================================

MODEL_CONFIG = {
    "Logistic Regression": {
        "file": "logistic_regression_metrics.json",
        "paths": [
            ["test_accuracy"]
        ]
    },

    "Random Forest": {
        "file": "random_forest_metrics.json",
        "paths": [
            ["test_metrics", "top_1_accuracy"],
            ["verification", "reloaded_test_accuracy"]
        ]
    },

    "XGBoost": {
        "file": "xgboost_metrics.json",
        "paths": [
            ["test", "top_1_accuracy"]
        ]
    }
}


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("CAREERCAST - MILESTONE 3")
print("STEP 5 - AUTOMATED ACCURACY GATE")
print("=" * 70)

print()
print("Accuracy gate configuration:")
print(f"Minimum required accuracy : {MIN_ACCURACY:.0f}%")
print(f"Target accuracy range     : {MIN_ACCURACY:.0f}% - {TARGET_MAX_ACCURACY:.0f}%")
print(f"Above {TARGET_MAX_ACCURACY:.0f}%           : PASS WITH WARNING")
print()
print("Existing model metrics will be checked.")
print("NO MODEL WILL BE RETRAINED.")
print()


# ============================================================
# HELPER: READ JSON
# ============================================================

def load_json(path):
    """Load a JSON file."""

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Metrics file not found: {path}"
        )

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# HELPER: NESTED VALUE
# ============================================================

def get_nested_value(data, path):
    """
    Read a nested JSON value.

    Example:

    path = ["test", "top_1_accuracy"]

    Reads:

    {
        "test": {
            "top_1_accuracy": 0.995
        }
    }
    """

    current = data

    for key in path:

        if not isinstance(current, dict):
            return None

        if key not in current:
            return None

        current = current[key]

    return current


# ============================================================
# FIND TEST ACCURACY
# ============================================================

def find_test_accuracy(metrics, paths):

    for path in paths:

        value = get_nested_value(
            metrics,
            path
        )

        if value is not None:

            try:
                value = float(value)
            except (TypeError, ValueError):
                continue

            return value

    raise KeyError(
        "Could not find test accuracy in metrics file."
    )


# ============================================================
# CLASSIFY RESULT
# ============================================================

def evaluate_accuracy(accuracy):

    if accuracy < MIN_ACCURACY:

        return {
            "status": "FAIL",
            "severity": "ERROR",
            "message": (
                f"Accuracy below minimum requirement "
                f"of {MIN_ACCURACY:.0f}%."
            )
        }

    elif accuracy <= TARGET_MAX_ACCURACY:

        return {
            "status": "PASS",
            "severity": "SUCCESS",
            "message": (
                f"Accuracy is within the target range "
                f"{MIN_ACCURACY:.0f}%-{TARGET_MAX_ACCURACY:.0f}%."
            )
        }

    else:

        return {
            "status": "PASS_WITH_WARNING",
            "severity": "WARNING",
            "message": (
                f"Accuracy exceeds the target maximum of "
                f"{TARGET_MAX_ACCURACY:.0f}%. "
                f"Existing model is retained without retraining."
            )
        }


# ============================================================
# RESULTS
# ============================================================

results = {}

hard_failure = False


# ============================================================
# PROCESS MODELS
# ============================================================

for model_name, config in MODEL_CONFIG.items():

    print("=" * 70)
    print(model_name)
    print("-" * 70)

    metrics_path = os.path.join(
        MODELS_DIR,
        config["file"]
    )

    print(f"Metrics file: {metrics_path}")

    try:

        metrics = load_json(
            metrics_path
        )

        accuracy = find_test_accuracy(
            metrics,
            config["paths"]
        )

        accuracy_percent = accuracy * 100.0

        evaluation = evaluate_accuracy(
            accuracy_percent
        )

        results[model_name] = {
            "metrics_file": metrics_path,
            "test_accuracy": round(
                accuracy_percent,
                4
            ),
            "minimum_required": MIN_ACCURACY,
            "target_maximum": TARGET_MAX_ACCURACY,
            "status": evaluation["status"],
            "message": evaluation["message"]
        }

        print(
            f"Test Accuracy : {accuracy_percent:.2f}%"
        )

        if evaluation["status"] == "PASS":

            print(
                "✓ PASS - Accuracy is within target range"
            )

        elif evaluation["status"] == "PASS_WITH_WARNING":

            print(
                f"⚠ PASS WITH WARNING - Accuracy above "
                f"{TARGET_MAX_ACCURACY:.0f}%"
            )

        else:

            print(
                f"✗ FAIL - Accuracy below "
                f"{MIN_ACCURACY:.0f}%"
            )

            hard_failure = True

    except Exception as error:

        results[model_name] = {
            "metrics_file": metrics_path,
            "status": "ERROR",
            "error": str(error)
        }

        print(
            f"✗ ERROR: {error}"
        )

        hard_failure = True


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 70)
print("ACCURACY GATE SUMMARY")
print("=" * 70)

for model_name, result in results.items():

    status = result["status"]

    accuracy = result.get(
        "test_accuracy"
    )

    if accuracy is not None:

        if status == "PASS":

            print(
                f"{model_name:<22} : "
                f"{accuracy:.2f}% -> PASS"
            )

        elif status == "PASS_WITH_WARNING":

            print(
                f"{model_name:<22} : "
                f"{accuracy:.2f}% -> PASS WITH WARNING"
            )

        else:

            print(
                f"{model_name:<22} : "
                f"{accuracy:.2f}% -> FAIL"
            )

    else:

        print(
            f"{model_name:<22} : "
            f"{status}"
        )


# ============================================================
# OVERALL STATUS
# ============================================================

if hard_failure:

    overall_status = "FAILED"

else:

    overall_status = "PASSED"


# ============================================================
# REPORT
# ============================================================

report = {
    "project": "CareerCast",
    "milestone": "Milestone 3",
    "step": "Step 5 - Automated Accuracy Gate",

    "timestamp": datetime.now().isoformat(),

    "configuration": {
        "minimum_required_accuracy": MIN_ACCURACY,
        "target_maximum_accuracy": TARGET_MAX_ACCURACY,
        "above_target_behavior": "PASS_WITH_WARNING",
        "retraining_performed": False
    },

    "models": results,

    "overall_status": overall_status,

    "ci_gate": {
        "passed": not hard_failure
    }
}


# ============================================================
# SAVE REPORT
# ============================================================

os.makedirs(
    MODELS_DIR,
    exist_ok=True
)

with open(
    REPORT_PATH,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        report,
        file,
        indent=4
    )


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 70)

if hard_failure:

    print("✗ ACCURACY GATE FAILED")
    print("CI pipeline should stop.")

else:

    print("✓ ACCURACY GATE PASSED")

    print()
    print(
        "All existing models satisfy the minimum "
        f"accuracy requirement of {MIN_ACCURACY:.0f}%."
    )

    print()
    print(
        "Models above 95% are reported as "
        "PASS WITH WARNING."
    )

print()
print("Accuracy gate report saved:")
print(REPORT_PATH)

print("=" * 70)


# ============================================================
# EXIT CODE
# ============================================================

if hard_failure:
    sys.exit(1)

sys.exit(0)