"""
CareerCast Skill Gap Analysis Engine.

Provides:
    - Skill normalization
    - Career skill requirements
    - Skill gap analysis
    - Actionable recommendations
    - Skill gap summary
"""

from typing import List, Dict, Any

from skill_gap.skill_database import (
    CAREER_SKILLS,
    SKILL_RECOMMENDATIONS,
    normalize_skill,
)


VALID_CAREERS = set(CAREER_SKILLS.keys())


# ============================================================
# SKILL NORMALIZATION
# ============================================================

def normalize_skills(skills: List[str]) -> List[str]:
    """
    Normalize and deduplicate candidate skills.
    """

    if not isinstance(skills, list):
        return []

    normalized = []

    for skill in skills:

        if not isinstance(skill, str):
            continue

        value = normalize_skill(skill)

        if value and value not in normalized:
            normalized.append(value)

    return normalized


# ============================================================
# REQUIRED SKILLS
# ============================================================

def get_required_skills(career: str) -> List[str]:
    """
    Return required skills for a valid career.

    Raises ValueError when called directly with an unknown
    career.
    """

    if not isinstance(career, str):
        raise ValueError("Career must be a string.")

    career = career.strip()

    if career not in CAREER_SKILLS:

        raise ValueError(
            f"Unknown career: '{career}'. "
            f"Supported careers: "
            f"{', '.join(sorted(VALID_CAREERS))}"
        )

    return [
        normalize_skill(skill)
        for skill in CAREER_SKILLS[career]
    ]


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

def analyze_skill_gap(
    candidate_skills: List[str],
    career: str,
) -> Dict[str, Any]:
    """
    Analyze candidate skills against a target career.

    For an unknown career, return a structured error result
    instead of raising an exception. This keeps the engine
    usable independently of FastAPI.
    """

    # --------------------------------------------------------
    # Validate career
    # --------------------------------------------------------

    if not isinstance(career, str):

        return {
            "status": "error",
            "career": career,
            "error": "Career must be a string.",
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "extra_skills": [],
            "skill_alignment": 0.0,
            "skill_gap_count": 0,
            "recommendations": [],
            "summary": "Invalid career.",
        }

    career = career.strip()

    if career not in CAREER_SKILLS:

        return {
            "status": "error",
            "career": career,
            "error": (
                f"Unknown career: '{career}'. "
                f"Supported careers: "
                f"{', '.join(sorted(VALID_CAREERS))}"
            ),
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "extra_skills": [],
            "skill_alignment": 0.0,
            "skill_gap_count": 0,
            "recommendations": [],
            "summary": (
                f"Career '{career}' is not available "
                "in the CareerCast skill database."
            ),
        }

    # --------------------------------------------------------
    # Normalize candidate skills
    # --------------------------------------------------------

    candidate = normalize_skills(candidate_skills)

    # --------------------------------------------------------
    # Required career skills
    # --------------------------------------------------------

    required_skills = get_required_skills(career)

    required_set = set(required_skills)
    candidate_set = set(candidate)

    # --------------------------------------------------------
    # Match / gap calculation
    # --------------------------------------------------------

    matched_skills = sorted(
        candidate_set.intersection(required_set)
    )

    missing_skills = sorted(
        required_set.difference(candidate_set)
    )

    extra_skills = sorted(
        candidate_set.difference(required_set)
    )

    # --------------------------------------------------------
    # Skill alignment
    # --------------------------------------------------------

    if required_set:

        skill_alignment = (
            len(matched_skills)
            / len(required_set)
        ) * 100

    else:

        skill_alignment = 0.0

    skill_alignment = round(
        skill_alignment,
        2,
    )

    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    recommendations = []

    for skill in missing_skills:

        recommendation = SKILL_RECOMMENDATIONS.get(
            skill,
            {
                "level": "Intermediate",
                "priority": "Medium",
                "action": (
                    f"Develop practical competency in {skill} "
                    "through courses, projects and "
                    "hands-on practice."
                ),
            },
        )

        recommendations.append(
            {
                "skill": skill,
                "level": recommendation["level"],
                "priority": recommendation["priority"],
                "action": recommendation["action"],
            }
        )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    if skill_alignment >= 90:

        summary_text = (
            "Excellent skill alignment. "
            "The candidate is well prepared "
            "for this career."
        )

    elif skill_alignment >= 70:

        summary_text = (
            "Good skill alignment. "
            "A few additional competencies "
            "should be developed."
        )

    elif skill_alignment >= 50:

        summary_text = (
            "Moderate skill alignment. "
            "Several important competencies "
            "need improvement."
        )

    else:

        summary_text = (
            "Low skill alignment. "
            "Significant skill development "
            "is recommended."
        )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    return {
        "status": "success",
        "career": career,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
        "skill_alignment": skill_alignment,
        "skill_gap_count": len(missing_skills),
        "recommendations": recommendations,
        "summary": summary_text,
    }


# ============================================================
# SKILL GAP SUMMARY
# ============================================================

def get_skill_gap_summary(
    candidate_skills: List[str],
    career: str,
) -> Dict[str, Any]:
    """
    Return a compact structured skill-gap summary.

    This is intentionally a dictionary rather than a plain
    string so it can be consumed by APIs, dashboards and
    report generators.
    """

    result = analyze_skill_gap(
        candidate_skills,
        career,
    )

    return {
        "status": result["status"],
        "career": result.get("career"),
        "skill_alignment": result.get(
            "skill_alignment",
            0.0,
        ),
        "skill_gap_count": result.get(
            "skill_gap_count",
            0,
        ),
        "matched_skills": result.get(
            "matched_skills",
            [],
        ),
        "missing_skills": result.get(
            "missing_skills",
            [],
        ),
        "summary": result.get(
            "summary",
            "",
        ),
    }