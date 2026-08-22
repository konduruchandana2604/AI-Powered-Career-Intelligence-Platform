"""
CareerCast FastAPI REST API.

Endpoints:
    GET  /
    GET  /health
    POST /predict
    POST /recommend
    POST /skill-gap
    POST /gap-report
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
#from rich.prompt import result

from api.schemas import (
    PredictionRequest,
    PredictionResponse,
    RecommendationRequest,
    RecommendationResponse,
    SkillGapRequest,
    SkillGapResponse,
    GapReportRequest,
    GapReportResponse,
)

from api.services import (
    predict_careers,
    generate_recommendations,
    generate_gap_report,
)

from skill_gap import analyze_skill_gap


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="CareerCast AI Career Intelligence API",
    description=(
        "REST API for career prediction, recommendations "
        "and skill gap analysis."
    ),
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "CareerCast FastAPI",
        "version": "1.0.0",
    }


# ============================================================
# PREDICT
# ============================================================

@app.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(request: PredictionRequest):

    try:

        predictions = predict_careers(
            text=request.text,
            top_k=request.top_k,
        )

        return {
            "status": "success",
            "model": "Random Forest + XGBoost",
            "predictions": predictions,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# RECOMMEND
# ============================================================

@app.post(
    "/recommend",
    response_model=RecommendationResponse,
)
def recommend(request: RecommendationRequest):

    try:

        recommendations = generate_recommendations(
            text=request.text,
            top_k=request.top_k,
        )

        return {
            "status": "success",
            "recommendations": recommendations,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# SKILL GAP
# ============================================================


@app.post(
    "/skill-gap",
    response_model=SkillGapResponse
)
def skill_gap(request: SkillGapRequest):

    try:
        result = analyze_skill_gap(
            skills=request.skills,
            career=request.career
        )

        if result.get("status") == "career_not_found":
            raise HTTPException(
                status_code=400,
                detail=result.get(
                    "message",
                    f"Unknown career: {request.career}"
                )
            )

        return result

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Skill gap analysis failed: {str(exc)}"
        )
    
# ============================================================
# GAP REPORT
# ============================================================

@app.post(
    "/gap-report",
    response_model=GapReportResponse
)
def gap_report(request: GapReportRequest):

    try:

        # --------------------------------------------
        # Step 1: Predict careers
        # --------------------------------------------

        predictions = predict_careers(
            text=request.text,
            top_k=request.top_k
        )

        if not predictions:
            raise HTTPException(
                status_code=500,
                detail="No career predictions generated."
            )

        # --------------------------------------------
        # Step 2: Determine career
        # --------------------------------------------

        predicted_career = request.career

        # If user did not provide a career,
        # use the top predicted career.
        if predicted_career is None:
            predicted_career = predictions[0]["career"]

        # --------------------------------------------
        # Step 3: Candidate skills
        # --------------------------------------------

        candidate_skills = request.skills

        # --------------------------------------------
        # Step 4: Analyze skill gap
        # --------------------------------------------

        skill_gap_result = analyze_skill_gap(
            skills=candidate_skills,
            career=predicted_career
        )

        # --------------------------------------------
        # Step 5: Validate career
        # --------------------------------------------

        if skill_gap_result.get("status") == "career_not_found":
            raise HTTPException(
                status_code=400,
                detail=skill_gap_result.get(
                    "message",
                    f"Unknown career: {predicted_career}"
                )
            )

        # --------------------------------------------
        # Step 6: Return complete report
        # --------------------------------------------

        return {
            "status": "success",
            "candidate_skills": candidate_skills,
            "predicted_career": predicted_career,
            "predictions": predictions,
            "skill_gap": skill_gap_result
        }

    except HTTPException:
        raise

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Gap report generation failed: {str(exc)}"
        )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "CareerCast API is running",
        "docs": "/docs",
        "health": "/health"
    }