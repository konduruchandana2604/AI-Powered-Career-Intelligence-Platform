from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from skill_gap_analyzer import CAREER_SKILLS, analyze_skill_gap


app = FastAPI(
    title="CareerCast API",
    description="Career prediction, recommendation, and skill-gap analysis service.",
    version="3.0.0",
)


class ResumeRequest(BaseModel):
    resume_text: str = Field(
        ...,
        min_length=20,
        description="Resume or candidate profile text.",
    )


class RecommendationRequest(ResumeRequest):
    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of career recommendations to return.",
    )


class GapReportRequest(ResumeRequest):
    career: Optional[str] = Field(
        default=None,
        description="Target career. If omitted, the top career is selected.",
    )


def calculate_score(resume_text: str, career: str) -> float:
    """Calculate a career score based on matched required skills."""
    report = analyze_skill_gap(resume_text, career)
    return round(report["completion_percentage"] / 100, 4)


def recommend_careers(
    resume_text: str,
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """Return careers ranked by skill-match score."""
    results = [
        {
            "career": career,
            "hybrid_score": calculate_score(resume_text, career),
        }
        for career in CAREER_SKILLS
    ]

    return sorted(
        results,
        key=lambda item: item["hybrid_score"],
        reverse=True,
    )[:top_k]


@app.get("/")
def root() -> Dict[str, str]:
    return {
        "message": "CareerCast API is running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "healthy"}


@app.post("/predict")
def predict(request: ResumeRequest) -> Dict[str, Any]:
    """Return the highest-scoring career prediction."""
    recommendations = recommend_careers(
        resume_text=request.resume_text,
        top_k=1,
    )

    if not recommendations:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed.",
        )

    return {
        "success": True,
        "prediction": recommendations[0],
    }


@app.post("/recommend")
def recommend(request: RecommendationRequest) -> Dict[str, Any]:
    """Return ranked career recommendations."""
    return {
        "success": True,
        "recommendations": recommend_careers(
            resume_text=request.resume_text,
            top_k=request.top_k,
        ),
    }


@app.post("/gap-report")
def gap_report(request: GapReportRequest) -> Dict[str, Any]:
    """Generate a skill-gap report for a selected or predicted career."""
    recommendations = recommend_careers(
        resume_text=request.resume_text,
        top_k=5,
    )

    if not recommendations:
        raise HTTPException(
            status_code=500,
            detail="Unable to determine a career.",
        )

    selected_career = request.career or recommendations[0]["career"]

    if selected_career not in CAREER_SKILLS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported career: {selected_career}. "
                f"Choose one of: {list(CAREER_SKILLS.keys())}"
            ),
        )

    try:
        report = analyze_skill_gap(
            resume_text=request.resume_text,
            career=selected_career,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return {
        "success": True,
        "career": selected_career,
        "report": report,
        "recommendations": recommendations,
    }