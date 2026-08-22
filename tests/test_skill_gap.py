from skill_gap import (
    analyze_skill_gap,
    get_skill_gap_summary
)


def test_data_scientist_skill_gap():

    result = analyze_skill_gap(
        [
            "python",
            "pandas",
            "numpy",
            "sql"
        ],
        "Data Scientist"
    )

    assert result["status"] == "success"

    assert result["career"] == "Data Scientist"

    assert "python" in result["matched_skills"]

    assert "pandas" in result["matched_skills"]

    assert "machine learning" in result[
        "missing_skills"
    ]

    assert result["skill_alignment"] > 0

    assert result["skill_alignment"] < 100


def test_all_skills_match():

    skills = [
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
        "data visualization"
    ]

    result = analyze_skill_gap(
        skills,
        "Data Scientist"
    )

    assert result["skill_alignment"] == 100.0

    assert result["missing_skills"] == []


def test_no_skills():

    result = analyze_skill_gap(
        [],
        "Data Scientist"
    )

    assert result["skill_alignment"] == 0.0

    assert len(
        result["missing_skills"]
    ) > 0


def test_skill_aliases():

    result = analyze_skill_gap(
        [
            "py",
            "sklearn",
            "ml",
            "pandas"
        ],
        "Data Scientist"
    )

    assert "python" in result[
        "matched_skills"
    ]

    assert "scikit-learn" in result[
        "matched_skills"
    ]

    assert "machine learning" in result[
        "matched_skills"
    ]


def test_unknown_career():

    result = analyze_skill_gap(
        [
            "python",
            "sql"
        ],
        "Unknown Career"
    )

    assert result[
        "status"
    ] == "career_not_found"

    assert result[
        "skill_alignment"
    ] == 0.0


def test_summary():

    result = get_skill_gap_summary(
        [
            "python",
            "pandas"
        ],
        "Data Scientist"
    )

    assert "career" in result

    assert "skill_alignment" in result

    assert "matched_skills" in result

    assert "missing_skills" in result

    assert "recommendations" in result