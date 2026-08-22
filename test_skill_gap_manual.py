from skill_gap import analyze_skill_gap


candidate_skills = [
    "Python",
    "Pandas",
    "NumPy",
    "SQL"
]


career = "Data Scientist"


result = analyze_skill_gap(
    candidate_skills,
    career
)


print("\n======================================")
print("       CAREERCAST SKILL GAP TEST")
print("======================================")

print(
    f"\nCareer: {result['career']}"
)

print(
    f"Status: {result['status']}"
)

print(
    f"\nSkill Alignment: "
    f"{result['skill_alignment']}%"
)

print(
    f"Matched Skills: "
    f"{len(result['matched_skills'])}"
)

print(
    f"Missing Skills: "
    f"{len(result['missing_skills'])}"
)


print("\nMatched Skills:")

for skill in result["matched_skills"]:
    print(f"  ✓ {skill}")


print("\nMissing Skills:")

for skill in result["missing_skills"]:
    print(f"  ✗ {skill}")


print("\nRecommendations:")

for item in result["recommendations"]:

    print(
        f"  • {item['skill']} "
        f"[{item['priority']}]"
    )

    print(
        f"    {item['action']}"
    )


print("\n======================================")