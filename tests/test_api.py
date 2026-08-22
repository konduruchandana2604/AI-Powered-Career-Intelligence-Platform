"""
Automated tests for CareerCast FastAPI.

Tests:
    - Health endpoint
    - Prediction endpoint
    - Recommendation endpoint
    - Skill gap endpoint
    - Gap report endpoint
    - Invalid request handling
"""

import pytest
from fastapi.testclient import TestClient

from api.main import app


# ============================================================
# TEST CLIENT
# ============================================================

client = TestClient(app)


# ============================================================
# SAMPLE DATA
# ============================================================

SAMPLE_TEXT = (
    "Python pandas numpy SQL statistics "
    "machine learning data visualization"
)

SAMPLE_SKILLS = [
    "python",
    "pandas",
    "numpy",
    "sql",
]


# ============================================================
# 1. HEALTH TEST
# ============================================================

def test_health_endpoint():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "CareerCast FastAPI"


# ============================================================
# 2. ROOT ENDPOINT
# ============================================================

def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert "message" in data
    assert "docs" in data


# ============================================================
# 3. PREDICTION ENDPOINT
# ============================================================

def test_prediction_endpoint():

    response = client.post(
        "/predict",
        json={
            "text": SAMPLE_TEXT,
            "top_k": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert data["model"] == (
        "Random Forest + XGBoost"
    )

    assert "predictions" in data

    assert len(data["predictions"]) == 5

    for prediction in data["predictions"]:

        assert "career" in prediction
        assert "confidence" in prediction

        assert isinstance(
            prediction["career"],
            str
        )

        assert 0 <= prediction["confidence"] <= 100


# ============================================================
# 4. TOP-K PREDICTION TEST
# ============================================================

@pytest.mark.parametrize(
    "top_k",
    [1, 3, 5]
)
def test_prediction_top_k(top_k):

    response = client.post(
        "/predict",
        json={
            "text": SAMPLE_TEXT,
            "top_k": top_k
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["predictions"]) == top_k


# ============================================================
# 5. RECOMMENDATION ENDPOINT
# ============================================================

def test_recommendation_endpoint():

    response = client.post(
        "/recommend",
        json={
            "text": SAMPLE_TEXT,
            "top_k": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert "recommendations" in data

    assert len(data["recommendations"]) == 5

    for recommendation in data["recommendations"]:

        assert "career" in recommendation
        assert "confidence" in recommendation
        assert "skill_alignment" in recommendation
        assert "matched_skills" in recommendation
        assert "missing_skills" in recommendation

        assert isinstance(
            recommendation["career"],
            str
        )

        assert 0 <= recommendation["confidence"] <= 100

        assert (
            0 <= recommendation["skill_alignment"] <= 100
        )

        assert isinstance(
            recommendation["matched_skills"],
            list
        )

        assert isinstance(
            recommendation["missing_skills"],
            list
        )


# ============================================================
# 6. SKILL GAP ENDPOINT
# ============================================================

def test_skill_gap_endpoint():

    response = client.post(
        "/skill-gap",
        json={
            "skills": SAMPLE_SKILLS,
            "career": "Data Scientist"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert data["career"] == "Data Scientist"

    assert "required_skills" in data
    assert "matched_skills" in data
    assert "missing_skills" in data
    assert "extra_skills" in data
    assert "skill_alignment" in data
    assert "skill_gap_count" in data
    assert "recommendations" in data

    assert isinstance(
        data["required_skills"],
        list
    )

    assert isinstance(
        data["matched_skills"],
        list
    )

    assert isinstance(
        data["missing_skills"],
        list
    )

    assert 0 <= data["skill_alignment"] <= 100

    assert data["skill_gap_count"] == len(
        data["missing_skills"]
    )


# ============================================================
# 7. SKILL GAP — ALL SKILLS
# ============================================================

def test_skill_gap_all_skills():

    all_data_scientist_skills = [
        "python",
        "sql",
        "statistics",
        "machine learning",
        "deep learning",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "data visualization",
    ]

    response = client.post(
        "/skill-gap",
        json={
            "skills": all_data_scientist_skills,
            "career": "Data Scientist"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["skill_alignment"] == 100.0

    assert data["missing_skills"] == []


# ============================================================
# 8. GAP REPORT ENDPOINT
# ============================================================

def test_gap_report_endpoint():

    response = client.post(
        "/gap-report",
        json={
            "text": SAMPLE_TEXT,
            "skills": SAMPLE_SKILLS,
            "career": "Data Scientist",
            "top_k": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert "candidate_skills" in data
    assert "predicted_career" in data
    assert "predictions" in data
    assert "skill_gap" in data

    assert data["predicted_career"] == "Data Scientist"

    assert len(data["predictions"]) == 5

    assert data["skill_gap"] is not None

    assert (
        data["skill_gap"]["career"]
        == "Data Scientist"
    )


# ============================================================
# 9. GAP REPORT WITHOUT TARGET CAREER
# ============================================================

def test_gap_report_auto_predicts_career():

    response = client.post(
        "/gap-report",
        json={
            "text": SAMPLE_TEXT,
            "skills": SAMPLE_SKILLS,
            "top_k": 3
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert data["predicted_career"] is not None

    assert isinstance(
        data["predicted_career"],
        str
    )

    assert len(data["predictions"]) == 3

    assert data["skill_gap"] is not None


# ============================================================
# 10. INVALID CAREER
# ============================================================

def test_invalid_career():

    response = client.post(
        "/skill-gap",
        json={
            "skills": SAMPLE_SKILLS,
            "career": "Invalid Career"
        }
    )

    assert response.status_code == 400


# ============================================================
# 11. EMPTY PREDICTION TEXT
# ============================================================

def test_empty_prediction_text():

    response = client.post(
        "/predict",
        json={
            "text": "",
            "top_k": 5
        }
    )

    assert response.status_code == 422


# ============================================================
# 12. INVALID TOP-K
# ============================================================

def test_invalid_top_k():

    response = client.post(
        "/predict",
        json={
            "text": SAMPLE_TEXT,
            "top_k": 20
        }
    )

    assert response.status_code == 422


# ============================================================
# 13. INVALID SKILL GAP REQUEST
# ============================================================

def test_invalid_skill_gap_request():

    response = client.post(
        "/skill-gap",
        json={
            "skills": [],
            "career": "Data Scientist"
        }
    )

    assert response.status_code == 422