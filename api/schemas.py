"""
Pydantic request and response schemas for CareerCast FastAPI.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


# ============================================================
# PREDICTION REQUEST
# ============================================================

class PredictionRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Resume text, profile text, or candidate skill description."
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of top career predictions."
    )


# ============================================================
# CAREER PREDICTION
# ============================================================

class CareerPrediction(BaseModel):
    career: str
    confidence: float


class PredictionResponse(BaseModel):
    status: str
    model: str
    predictions: List[CareerPrediction]


# ============================================================
# RECOMMENDATION REQUEST
# ============================================================

class RecommendationRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Candidate resume/profile text."
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10
    )


# ============================================================
# RECOMMENDATION
# ============================================================

class CareerRecommendation(BaseModel):
    career: str
    confidence: float
    skill_alignment: Optional[float] = None
    matched_skills: List[str] = []
    missing_skills: List[str] = []


class RecommendationResponse(BaseModel):
    status: str
    recommendations: List[CareerRecommendation]


# ============================================================
# SKILL GAP REQUEST
# ============================================================

class SkillGapRequest(BaseModel):
    skills: List[str] = Field(
        ...,
        min_length=1,
        description="Candidate skills."
    )

    career: str = Field(
        ...,
        min_length=1,
        description="Target career."
    )


# ============================================================
# SKILL GAP RESPONSE
# ============================================================

class SkillGapResponse(BaseModel):
    status: str
    career: str
    required_skills: List[str]
    matched_skills: List[str]
    missing_skills: List[str]
    extra_skills: List[str]
    skill_alignment: float
    skill_gap_count: int
    recommendations: list


# ============================================================
# COMPLETE GAP REPORT REQUEST
# ============================================================

class GapReportRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1
    )

    skills: List[str] = Field(
        default=[]
    )

    career: Optional[str] = None

    top_k: int = Field(
        default=5,
        ge=1,
        le=10
    )


# ============================================================
# GAP REPORT RESPONSE
# ============================================================

class GapReportResponse(BaseModel):
    status: str
    candidate_skills: List[str]
    predicted_career: Optional[str]
    predictions: List[CareerPrediction]
    skill_gap: Optional[SkillGapResponse]