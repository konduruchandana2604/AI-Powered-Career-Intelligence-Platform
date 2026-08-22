#cat > skill_gap/analyzer.py <<'PY'
"""
CareerCast Skill Gap Analysis Engine.

Provides:
    - career validation
    - required skill lookup
    - skill normalization and aliases
    - matched/missing/extra skill analysis
    - skill alignment score
    - actionable recommendations
    - summary/report generation
"""

from typing import Dict, List, Any

from .skill_database import CAREER_SKILLS


# ============================================================
# VALID CAREERS
# ============================================================

VALID_CAREERS = set(CAREER_SKILLS.keys())


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {
    "py": "python",
    "python3": "python",

    "postgres": "postgresql",
    "postgres sql": "postgresql",

    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",

    "tf": "tensorflow",

    "pytorch framework": "pytorch",

    "ml": "machine learning",
    "machine-learning": "machine learning",

    "dl": "deep learning",
    "deep-learning": "deep learning",

    "data viz": "data visualization",
    "data visualisation": "data visualization",

    "js": "javascript",
    "javascript programming": "javascript",

    "ts": "typescript",

    "reactjs": "react",
    "react.js": "react",

    "nodejs": "node.js",
    "node": "node.js",

    "powerbi": "power bi",
    "power-bi": "power bi",

    "ms excel": "excel",
    "microsoft excel": "excel",
}


# ============================================================
# RECOMMENDATION DATABASE
# ============================================================

SKILL_RECOMMENDATIONS = {

    "python": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Practice Python through data processing, automation, "
            "APIs and machine learning projects."
        ),
    },

    "sql": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Practice joins, subqueries, CTEs, window functions, "
            "indexing and database optimization."
        ),
    },

    "statistics": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Study probability, distributions, hypothesis testing, "
            "correlation and regression."
        ),
    },

    "machine learning": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Build classification, regression and clustering "
            "projects using real datasets."
        ),
    },

    "deep learning": {
        "level": "Advanced",
        "priority": "High",
        "action": (
            "Learn neural networks, CNNs, optimization and modern "
            "deep learning architectures."
        ),
    },

    "pandas": {
        "level": "Intermediate",
        "priority": "Medium",
        "action": (
            "Practice data cleaning, transformation, grouping, "
            "merging and exploratory data analysis with Pandas."
        ),
    },

    "numpy": {
        "level": "Intermediate",
        "priority": "Medium",
        "action": (
            "Practice numerical arrays, vectorization, broadcasting "
            "and mathematical operations using NumPy."
        ),
    },

    "scikit-learn": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Build complete ML pipelines using preprocessing, "
            "training, evaluation and hyperparameter tuning."
        ),
    },

    "tensorflow": {
        "level": "Intermediate → Advanced",
        "priority": "Medium",
        "action": (
            "Build neural networks and practice training, "
            "validation and model deployment."
        ),
    },

    "pytorch": {
        "level": "Intermediate → Advanced",
        "priority": "High",
        "action": (
            "Practice tensors, datasets, neural networks, "
            "training loops and model deployment."
        ),
    },

    "data visualization": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Create effective visualizations using Matplotlib, "
            "Plotly, Power BI or Tableau."
        ),
    },

    "javascript": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Build interactive web applications using modern "
            "JavaScript, DOM APIs and asynchronous programming."
        ),
    },

    "react": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Build component-based applications using React, "
            "state management and API integration."
        ),
    },

    "java": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Practice object-oriented programming, collections, "
            "exception handling and backend development."
        ),
    },

    "git": {
        "level": "Intermediate",
        "priority": "Medium",
        "action": (
            "Practice Git branching, merging, pull requests and "
            "collaborative version control workflows."
        ),
    },

    "docker": {
        "level": "Intermediate",
        "priority": "Medium",
        "action": (
            "Containerize applications and practice Dockerfiles, "
            "images, containers and networking."
        ),
    },

    "aws": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Learn core AWS services and deploy a small production "
            "application using cloud infrastructure."
        ),
    },

    "power bi": {
        "level": "Intermediate",
        "priority": "Medium",
        "action": (
            "Create dashboards, data models and interactive reports "
            "using Power BI."
        ),
    },

    "tableau": {
        "level": "Intermediate",
        "priority": "Medium",
        "action": (
            "Build interactive dashboards and practice data "
            "visualization using Tableau."
        ),
    },
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_skill(skill: str) -> str:
    """
    Normalize a single skill.

    Example:
        'Python3' -> 'python'
        'SKLearn' -> 'scikit-learn'
    """

    if not isinstance(skill, str):
        return ""

    normalized = skill.strip().lower()

    normalized = " ".join(normalized.split())

    return SKILL_ALIASES.get(
        normalized,
        normalized
    )


def normalize_skills(skills: List[str]) -> List[str]:
    """
    Normalize and deduplicate skills.
    """

    result = []

    for skill in skills:

        normalized = normalize_skill(skill)

        if normalized and normalized not in result:
            result.append(normalized)

    return result


# ============================================================
# CAREER LOOKUP
# ============================================================

def get_required_skills(career: str) -> List[str]:
    """
    Return required skills for a valid career.

    This function raises ValueError for invalid careers.

    The public analyze_skill_gap() function catches that error
    and returns a structured response.
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
# RECOMMENDATION GENERATOR
# ============================================================

def generate_skill_recommendations(
    missing_skills: List[str]
) -> List[Dict[str, str]]:
    """
    Generate actionable recommendations for missing skills.
    """

    recommendations = []

    for skill in missing_skills:

        recommendation = SKILL_RECOMMENDATIONS.get(
            skill,
            {
                "level": "Beginner → Intermediate",
                "priority": "Medium",
                "action": (
                    f"Learn {skill} through structured courses, "
                    f"hands-on projects and practical exercises."
                ),
            }
        )

        recommendations.append(
            {
                "skill": skill,
                "level": recommendation["level"],
                "priority": recommendation["priority"],
                "action": recommendation["action"],
            }
        )

    return recommendations


# ============================================================
# SUMMARY
# ============================================================

def get_skill_gap_summary(
    skills: List[str],
    career: str
) -> Dict[str, Any]:
    """
    Return a structured skill-gap summary.

    IMPORTANT:
    This function intentionally returns a dictionary because
    the test suite expects keys such as:

        career
        skill_alignment
        matched_skills
        missing_skills
        recommendations
    """

    result = analyze_skill_gap(
        skills,
        career
    )

    return result


# ============================================================
# MAIN ANALYSIS
# ============================================================

def analyze_skill_gap(
    skills: List[str],
    career: str
) -> Dict[str, Any]:
    """
    Analyze candidate skills against a target career.

    Invalid careers do NOT raise an exception here.

    Instead:

        {
            "status": "career_not_found",
            ...
        }

    This allows the API layer and direct Python tests to use
    the same stable contract.
    """

    # --------------------------------------------------------
    # Validate career
    # --------------------------------------------------------

    try:

        required_skills = get_required_skills(
            career
        )

    except ValueError as exc:

        return {
            "status": "career_not_found",
            "career": career,
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "extra_skills": normalize_skills(
                skills if isinstance(skills, list) else []
            ),
            "skill_alignment": 0.0,
            "skill_gap_count": 0,
            "recommendations": [],
            "summary": str(exc),
        }

    # --------------------------------------------------------
    # Normalize candidate skills
    # --------------------------------------------------------

    candidate_skills = normalize_skills(
        skills
    )

    required_set = set(
        required_skills
    )

    candidate_set = set(
        candidate_skills
    )

    # --------------------------------------------------------
    # Matching
    # --------------------------------------------------------

    matched_skills = sorted(
        candidate_set.intersection(
            required_set
        )
    )

    missing_skills = sorted(
        required_set.difference(
            candidate_set
        )
    )

    extra_skills = sorted(
        candidate_set.difference(
            required_set
        )
    )

    # --------------------------------------------------------
    # Alignment
    # --------------------------------------------------------

    if not required_set:

        skill_alignment = 0.0

    else:

        skill_alignment = round(
            (
                len(matched_skills)
                /
                len(required_set)
            )
            * 100,
            2
        )

    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    recommendations = generate_skill_recommendations(
        missing_skills
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    if skill_alignment >= 90:

        summary = (
            f"Excellent skill alignment for the "
            f"{career} career."
        )

    elif skill_alignment >= 70:

        summary = (
            f"Good skill alignment for the "
            f"{career} career. "
            f"Some skill development is recommended."
        )

    elif skill_alignment >= 40:

        summary = (
            f"Moderate skill alignment for the "
            f"{career} career. "
            f"Several skills should be developed."
        )

    else:

        summary = (
            f"Low skill alignment for the "
            f"{career} career. "
            f"Significant skill development is recommended."
        )

    # --------------------------------------------------------
    # Final response
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
        "summary": summary,
    }


# ============================================================
# REPORT ALIAS
# ============================================================

def generate_gap_report(
    skills: List[str],
    career: str
) -> Dict[str, Any]:
    """
    Convenience wrapper for report generation.
    """

    return analyze_skill_gap(
        skills,
        career
    )
