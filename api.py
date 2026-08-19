from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

from career_recommendation_engine import recommend_careers


# ============================================================
# CAREERCAST MILESTONE 3
# FASTAPI REST SERVICE
# ============================================================

app = FastAPI(
    title="CareerCast AI Career Intelligence API",
    description=(
        "REST API for career prediction, career recommendation "
        "and skill gap analysis."
    ),
    version="3.0.0"
)


# ============================================================
# REQUEST MODELS
# ============================================================

class ResumeRequest(BaseModel):

    resume_text: str = Field(
        ...,
        min_length=20,
        description="Resume text or candidate profile"
    )


class RecommendationRequest(BaseModel):

    resume_text: str = Field(
        ...,
        min_length=20,
        description="Resume text or candidate profile"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of career recommendations"
    )


class GapRequest(BaseModel):

    resume_text: str = Field(
        ...,
        min_length=20,
        description="Resume text or candidate profile"
    )

    career: Optional[str] = Field(
        default=None,
        description="Target career. If omitted, top recommended career is used."
    )


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "application": "CareerCast",
        "module": "Milestone 3",
        "service": "FastAPI REST API",
        "version": "3.0.0",
        "status": "running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "CareerCast FastAPI",
        "milestone": "Milestone 3"
    }


# ============================================================
# PREDICTION ENDPOINT
# ============================================================

@app.post("/predict")
def predict(request: ResumeRequest):

    try:

        recommendations = recommend_careers(
            request.resume_text,
            top_k=5
        )

        if not recommendations:

            raise HTTPException(
                status_code=500,
                detail="No career prediction generated."
            )

        top_prediction = recommendations[0]

        return {
            "success": True,
            "prediction": {
                "career": top_prediction["career"],
                "confidence": top_prediction["hybrid_score"]
            },
            "recommendations": recommendations
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# RECOMMENDATION ENDPOINT
# ============================================================

@app.post("/recommend")
def recommend(request: RecommendationRequest):

    try:

        recommendations = recommend_careers(
            request.resume_text,
            top_k=request.top_k
        )

        return {
            "success": True,
            "count": len(recommendations),
            "recommendations": recommendations
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# SKILL GAP ENDPOINT
# ============================================================

@app.post("/gap-report")
def gap_report(request: GapRequest):

    try:

        recommendations = recommend_careers(
            request.resume_text,
            top_k=5
        )

        if not recommendations:

            raise HTTPException(
                status_code=500,
                detail="Unable to determine career."
            )

        selected_career = request.career

        if not selected_career:

            selected_career = recommendations[0]["career"]

        return {
            "success": True,
            "career": selected_career,
            "message": (
                "Skill gap analysis endpoint is active. "
                "Detailed skill gap module will be integrated "
                "in Milestone 3 Step 2."
            ),
            "recommendations": recommendations
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# API INFORMATION
# ============================================================

@app.get("/api-info")
def api_info():

    return {
        "application": "CareerCast",
        "version": "3.0.0",
        "milestone": "Milestone 3",
        "endpoints": [
            "GET /",
            "GET /health",
            "POST /predict",
            "POST /recommend",
            "POST /gap-report"
        ]
    }