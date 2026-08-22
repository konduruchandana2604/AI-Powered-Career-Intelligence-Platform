"""
CareerCast prediction and recommendation services.

Uses the existing Milestone 2:
    - Random Forest
    - XGBoost
    - TF-IDF vectorizers
    - Label encoders

Also integrates:
    - Skill Gap Analysis Engine
"""

from pathlib import Path
from typing import List, Dict, Any

import joblib


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_DIR = PROJECT_ROOT / "models"


# ============================================================
# MODEL FILES
# ============================================================

RF_MODEL_PATH = MODEL_DIR / "random_forest.pkl"
RF_TFIDF_PATH = MODEL_DIR / "random_forest_tfidf.pkl"
RF_ENCODER_PATH = MODEL_DIR / "random_forest_label_encoder.pkl"

XGB_MODEL_PATH = MODEL_DIR / "xgboost.pkl"
XGB_TFIDF_PATH = MODEL_DIR / "xgboost_tfidf.pkl"
XGB_ENCODER_PATH = MODEL_DIR / "xgboost_label_encoder.pkl"


# ============================================================
# MODEL LOADING
# ============================================================

def load_models():
    """
    Load the existing CareerCast Milestone 2 models.
    """

    required_files = [
        RF_MODEL_PATH,
        RF_TFIDF_PATH,
        RF_ENCODER_PATH,
        XGB_MODEL_PATH,
        XGB_TFIDF_PATH,
        XGB_ENCODER_PATH,
    ]

    missing_files = [
        str(path)
        for path in required_files
        if not path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Missing required model files:\n"
            + "\n".join(missing_files)
        )

    rf_model = joblib.load(RF_MODEL_PATH)
    rf_tfidf = joblib.load(RF_TFIDF_PATH)
    rf_encoder = joblib.load(RF_ENCODER_PATH)

    xgb_model = joblib.load(XGB_MODEL_PATH)
    xgb_tfidf = joblib.load(XGB_TFIDF_PATH)
    xgb_encoder = joblib.load(XGB_ENCODER_PATH)

    return {
        "rf_model": rf_model,
        "rf_tfidf": rf_tfidf,
        "rf_encoder": rf_encoder,
        "xgb_model": xgb_model,
        "xgb_tfidf": xgb_tfidf,
        "xgb_encoder": xgb_encoder,
    }


# ============================================================
# LOAD MODELS ONCE
# ============================================================

MODELS = load_models()


# ============================================================
# RANDOM FOREST PREDICTION
# ============================================================

def predict_random_forest(
    text: str,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Generate top-K Random Forest career predictions.
    """

    model = MODELS["rf_model"]
    vectorizer = MODELS["rf_tfidf"]
    encoder = MODELS["rf_encoder"]

    X = vectorizer.transform([text])

    probabilities = model.predict_proba(X)[0]

    top_indices = probabilities.argsort()[::-1][:top_k]

    results = []

    for index in top_indices:

        career = encoder.inverse_transform([index])[0]

        confidence = float(probabilities[index] * 100)

        results.append({
            "career": career,
            "confidence": round(confidence, 2)
        })

    return results


# ============================================================
# XGBOOST PREDICTION
# ============================================================

def predict_xgboost(
    text: str,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Generate top-K XGBoost career predictions.
    """

    model = MODELS["xgb_model"]
    vectorizer = MODELS["xgb_tfidf"]
    encoder = MODELS["xgb_encoder"]

    X = vectorizer.transform([text])

    probabilities = model.predict_proba(X)[0]

    top_indices = probabilities.argsort()[::-1][:top_k]

    results = []

    for index in top_indices:

        career = encoder.inverse_transform([index])[0]

        confidence = float(probabilities[index] * 100)

        results.append({
            "career": career,
            "confidence": round(confidence, 2)
        })

    return results


# ============================================================
# HYBRID PREDICTION
# ============================================================

def predict_careers(
    text: str,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Combine Random Forest and XGBoost probabilities.

    Each model contributes 50%.
    """

    rf_model = MODELS["rf_model"]
    rf_vectorizer = MODELS["rf_tfidf"]
    rf_encoder = MODELS["rf_encoder"]

    xgb_model = MODELS["xgb_model"]
    xgb_vectorizer = MODELS["xgb_tfidf"]
    xgb_encoder = MODELS["xgb_encoder"]

    rf_X = rf_vectorizer.transform([text])
    xgb_X = xgb_vectorizer.transform([text])

    rf_probabilities = rf_model.predict_proba(rf_X)[0]
    xgb_probabilities = xgb_model.predict_proba(xgb_X)[0]

    # Both models use the same career ordering.
    if list(rf_encoder.classes_) != list(xgb_encoder.classes_):
        raise ValueError(
            "Random Forest and XGBoost label encoders "
            "contain different career classes."
        )

    hybrid_probabilities = (
        0.5 * rf_probabilities
        + 0.5 * xgb_probabilities
    )

    top_indices = (
        hybrid_probabilities
        .argsort()[::-1][:top_k]
    )

    results = []

    for index in top_indices:

        career = rf_encoder.inverse_transform([index])[0]

        confidence = float(
            hybrid_probabilities[index] * 100
        )

        results.append({
            "career": career,
            "confidence": round(confidence, 2)
        })

    return results


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract known skills from resume/profile text.

    This is intentionally deterministic for the first
    FastAPI version.
    """

    from skill_gap.skill_database import (
        CAREER_SKILLS,
        normalize_skill
    )

    normalized_text = text.lower()

    all_skills = set()

    for skills in CAREER_SKILLS.values():

        for skill in skills:
            all_skills.add(normalize_skill(skill))

    detected = []

    for skill in sorted(all_skills):

        if skill in normalized_text:
            detected.append(skill)

    return detected


# ============================================================
# RECOMMENDATIONS
# ============================================================

def generate_recommendations(
    text: str,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Generate career recommendations with skill alignment.
    """

    from skill_gap import analyze_skill_gap

    predictions = predict_careers(
        text=text,
        top_k=top_k
    )

    candidate_skills = extract_skills_from_text(text)

    recommendations = []

    for prediction in predictions:

        career = prediction["career"]

        gap = analyze_skill_gap(
            candidate_skills,
            career
        )

        recommendations.append({
            "career": career,
            "confidence": prediction["confidence"],
            "skill_alignment": gap["skill_alignment"],
            "matched_skills": gap["matched_skills"],
            "missing_skills": gap["missing_skills"],
        })

    return recommendations


# ============================================================
# GAP REPORT
# ============================================================

def generate_gap_report(
    text: str,
    skills: List[str],
    career: str = None,
    top_k: int = 5
) -> Dict[str, Any]:
    """
    Generate complete career + skill gap report.
    """

    from skill_gap import analyze_skill_gap

    predictions = predict_careers(
        text=text,
        top_k=top_k
    )

    detected_skills = extract_skills_from_text(text)

    combined_skills = list(
        set(
            detected_skills
            + skills
        )
    )

    predicted_career = career

    if predicted_career is None and predictions:
        predicted_career = predictions[0]["career"]

    skill_gap = None

    if predicted_career:

        skill_gap = analyze_skill_gap(
            combined_skills,
            predicted_career
        )

    return {
        "status": "success",
        "candidate_skills": combined_skills,
        "predicted_career": predicted_career,
        "predictions": predictions,
        "skill_gap": skill_gap,
    }