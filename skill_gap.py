# ============================================================
# CAREERCAST
# MILESTONE 3 - STEP 3
# SKILL GAP ANALYSIS ENGINE
# ============================================================

from typing import Dict, List, Any


# ============================================================
# CAREER SKILL REQUIREMENTS
# ============================================================

CAREER_SKILLS = {

    "AI Researcher": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn"
    ],

    "Backend Developer": [
        "Python",
        "Java",
        "SQL",
        "Django",
        "Flask",
        "Node.js",
        "Git"
    ],

    "Business Analyst": [
        "SQL",
        "Data Analysis",
        "Data Visualization",
        "Power BI",
        "Tableau",
        "Communication"
    ],

    "Business Manager": [
        "Leadership",
        "Communication",
        "Project Management",
        "Data Analysis",
        "Teamwork"
    ],

    "Cybersecurity Analyst": [
        "Cybersecurity",
        "Networking",
        "Linux",
        "Python",
        "Git"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Data Analysis",
        "Pandas",
        "NumPy",
        "Power BI",
        "Tableau"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Machine Learning",
        "Data Analysis",
        "Pandas",
        "NumPy",
        "Scikit-learn"
    ],

    "Deep Learning Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch"
    ],

    "Digital Marketing Specialist": [
        "Digital Marketing",
        "SEO",
        "Communication",
        "Data Analysis"
    ],

    "Ethical Hacker": [
        "Ethical Hacking",
        "Cybersecurity",
        "Networking",
        "Linux",
        "Python"
    ],

    "Frontend Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Git"
    ],

    "Full Stack Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "SQL",
        "Git"
    ],

    "Graphic Designer": [
        "Graphic Design",
        "Figma",
        "UI/UX"
    ],

    "Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Git"
    ],

    "Marketing Executive": [
        "Communication",
        "Leadership",
        "Digital Marketing",
        "SEO",
        "Teamwork"
    ],

    "Operations Manager": [
        "Leadership",
        "Communication",
        "Project Management",
        "Teamwork",
        "Data Analysis"
    ],

    "Product Designer": [
        "Figma",
        "UI/UX",
        "Graphic Design",
        "Communication"
    ],

    "Project Manager": [
        "Project Management",
        "Leadership",
        "Communication",
        "Teamwork"
    ],

    "Security Engineer": [
        "Cybersecurity",
        "Networking",
        "Linux",
        "Python",
        "AWS",
        "Docker"
    ],

    "Seo Analyst": [
        "SEO",
        "Digital Marketing",
        "Data Analysis",
        "Communication"
    ],

    "Software Engineer": [
        "Python",
        "Java",
        "JavaScript",
        "SQL",
        "Git",
        "Linux"
    ],

    "UI/UX Designer": [
        "UI/UX",
        "Figma",
        "Graphic Design",
        "Communication"
    ]
}


# ============================================================
# ACTIONABLE SKILL IMPROVEMENT SUGGESTIONS
# ============================================================

SKILL_SUGGESTIONS = {

    "Python": {
        "priority": "High",
        "action": "Practice Python programming, OOP, data structures and problem solving.",
        "project": "Build a Python-based application or automation project."
    },

    "Java": {
        "priority": "Medium",
        "action": "Learn Java fundamentals, OOP, collections and exception handling.",
        "project": "Build a Java REST API or backend application."
    },

    "JavaScript": {
        "priority": "High",
        "action": "Strengthen JavaScript fundamentals, ES6+, DOM and asynchronous programming.",
        "project": "Build an interactive web application."
    },

    "SQL": {
        "priority": "High",
        "action": "Practice SQL queries, joins, subqueries, aggregation and database design.",
        "project": "Build a relational database project with analytical queries."
    },

    "HTML": {
        "priority": "Medium",
        "action": "Learn semantic HTML5 and accessible webpage structure.",
        "project": "Create a responsive portfolio website."
    },

    "CSS": {
        "priority": "Medium",
        "action": "Improve CSS layouts, Flexbox, Grid, responsive design and animations.",
        "project": "Create a responsive professional dashboard."
    },

    "React": {
        "priority": "High",
        "action": "Learn React components, hooks, state management and API integration.",
        "project": "Build a React-based career dashboard."
    },

    "Node.js": {
        "priority": "High",
        "action": "Learn Node.js, Express, REST APIs and asynchronous programming.",
        "project": "Build a REST API using Node.js and Express."
    },

    "Django": {
        "priority": "Medium",
        "action": "Learn Django models, views, URLs, authentication and REST APIs.",
        "project": "Build a Django web application."
    },

    "Flask": {
        "priority": "Medium",
        "action": "Learn Flask routing, APIs, templates and database integration.",
        "project": "Build a Flask REST API."
    },

    "Machine Learning": {
        "priority": "High",
        "action": "Study supervised learning, unsupervised learning, feature engineering and model evaluation.",
        "project": "Build an end-to-end machine learning prediction system."
    },

    "Deep Learning": {
        "priority": "High",
        "action": "Study neural networks, CNNs, RNNs, transformers and model optimization.",
        "project": "Build a deep learning image or text classification project."
    },

    "Artificial Intelligence": {
        "priority": "High",
        "action": "Study AI fundamentals, intelligent agents, search, learning and modern generative AI.",
        "project": "Build an AI-powered application."
    },

    "TensorFlow": {
        "priority": "High",
        "action": "Practice TensorFlow model creation, training, evaluation and deployment.",
        "project": "Train and deploy a TensorFlow neural network."
    },

    "PyTorch": {
        "priority": "High",
        "action": "Learn PyTorch tensors, neural networks, training loops and model deployment.",
        "project": "Build and train a PyTorch deep learning model."
    },

    "Scikit-learn": {
        "priority": "High",
        "action": "Practice preprocessing, pipelines, classification, regression and model evaluation.",
        "project": "Create a complete Scikit-learn ML pipeline."
    },

    "Pandas": {
        "priority": "Medium",
        "action": "Practice data cleaning, transformation, grouping and analysis with Pandas.",
        "project": "Perform exploratory analysis on a real-world dataset."
    },

    "NumPy": {
        "priority": "Medium",
        "action": "Learn NumPy arrays, vectorization, mathematical operations and matrix manipulation.",
        "project": "Implement numerical data processing using NumPy."
    },

    "Data Analysis": {
        "priority": "High",
        "action": "Develop skills in data cleaning, exploratory analysis and statistical interpretation.",
        "project": "Complete an end-to-end data analysis project."
    },

    "Data Visualization": {
        "priority": "Medium",
        "action": "Learn effective charts, dashboards and visual storytelling.",
        "project": "Create an interactive analytics dashboard."
    },

    "Power BI": {
        "priority": "Medium",
        "action": "Learn Power BI data modeling, DAX and dashboard development.",
        "project": "Build a business intelligence dashboard."
    },

    "Tableau": {
        "priority": "Medium",
        "action": "Learn Tableau visualization, calculated fields and dashboard design.",
        "project": "Create an interactive Tableau analytics dashboard."
    },

    "AWS": {
        "priority": "High",
        "action": "Learn AWS fundamentals, EC2, S3, IAM and deployment.",
        "project": "Deploy a web application on AWS."
    },

    "Docker": {
        "priority": "Medium",
        "action": "Learn Docker images, containers, Dockerfiles and networking.",
        "project": "Containerize a machine learning API."
    },

    "Git": {
        "priority": "Medium",
        "action": "Practice Git branching, merging, pull requests and version control.",
        "project": "Manage a complete software project using Git."
    },

    "Linux": {
        "priority": "Medium",
        "action": "Practice Linux commands, shell scripting, permissions and process management.",
        "project": "Deploy and manage an application on a Linux server."
    },

    "Cybersecurity": {
        "priority": "High",
        "action": "Study network security, authentication, vulnerabilities and security monitoring.",
        "project": "Build a cybersecurity monitoring or vulnerability-analysis project."
    },

    "Networking": {
        "priority": "High",
        "action": "Study TCP/IP, DNS, HTTP, routing, firewalls and network security.",
        "project": "Design and document a secure computer network."
    },

    "Ethical Hacking": {
        "priority": "High",
        "action": "Study ethical penetration testing methodologies and security assessment concepts.",
        "project": "Build a controlled security testing lab."
    },

    "Figma": {
        "priority": "High",
        "action": "Practice wireframing, prototyping, components and design systems.",
        "project": "Design a complete mobile or web application prototype."
    },

    "UI/UX": {
        "priority": "High",
        "action": "Learn user research, information architecture, wireframing and usability principles.",
        "project": "Design and test a complete user experience."
    },

    "Graphic Design": {
        "priority": "Medium",
        "action": "Practice typography, composition, branding and visual design.",
        "project": "Create a professional branding portfolio."
    },

    "SEO": {
        "priority": "Medium",
        "action": "Learn keyword research, technical SEO, on-page optimization and analytics.",
        "project": "Optimize a website and measure search performance."
    },

    "Digital Marketing": {
        "priority": "High",
        "action": "Learn content marketing, social media, campaigns and digital analytics.",
        "project": "Create and analyze a digital marketing campaign."
    },

    "Project Management": {
        "priority": "High",
        "action": "Learn project planning, Agile, Scrum, risk management and stakeholder management.",
        "project": "Manage a complete project using Agile methodology."
    },

    "Communication": {
        "priority": "Medium",
        "action": "Improve technical communication, presentations and professional writing.",
        "project": "Present a technical project to a professional audience."
    },

    "Leadership": {
        "priority": "Medium",
        "action": "Develop team coordination, decision making and leadership skills.",
        "project": "Lead a small team project from planning to delivery."
    },

    "Teamwork": {
        "priority": "Medium",
        "action": "Practice collaboration, peer review and conflict resolution.",
        "project": "Contribute to a collaborative software project."
    }
}


# ============================================================
# NORMALIZE SKILL
# ============================================================

def normalize_skill(skill: str) -> str:
    """
    Normalize skill names for comparison.
    """

    return " ".join(
        str(skill).strip().lower().split()
    )


# ============================================================
# GET CAREER REQUIREMENTS
# ============================================================

def get_required_skills(career: str) -> List[str]:
    """
    Return required skills for a career.
    """

    if not career:
        return []

    return CAREER_SKILLS.get(
        career,
        []
    )


# ============================================================
# CALCULATE SKILL GAP
# ============================================================

def calculate_skill_gap(
    identified_skills: List[str],
    career: str
) -> Dict[str, Any]:
    """
    Compare candidate skills against career requirements.

    Returns:

    - required skills
    - matched skills
    - missing skills
    - skill alignment
    - gap percentage
    - actionable recommendations
    """

    required_skills = get_required_skills(
        career
    )

    if not required_skills:

        return {
            "career": career,
            "required_skills": [],
            "identified_skills": identified_skills,
            "matched_skills": [],
            "missing_skills": [],
            "skill_alignment": 0.0,
            "skill_gap_percentage": 0.0,
            "recommendations": []
        }

    identified_normalized = {
        normalize_skill(skill)
        for skill in identified_skills
    }

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if normalize_skill(skill) in identified_normalized:

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)

    total_required = len(
        required_skills
    )

    matched_count = len(
        matched_skills
    )

    alignment = (
        matched_count
        /
        total_required
    ) * 100

    gap_percentage = (
        len(missing_skills)
        /
        total_required
    ) * 100

    recommendations = []

    for skill in missing_skills:

        suggestion = SKILL_SUGGESTIONS.get(
            skill,
            {
                "priority": "Medium",
                "action": f"Develop practical skills in {skill}.",
                "project": f"Complete a project demonstrating {skill}."
            }
        )

        recommendations.append({
            "skill": skill,
            "priority": suggestion["priority"],
            "action": suggestion["action"],
            "project": suggestion["project"]
        })

    return {
        "career": career,

        "required_skills": required_skills,

        "identified_skills": identified_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "skill_alignment": round(
            alignment,
            2
        ),

        "skill_gap_percentage": round(
            gap_percentage,
            2
        ),

        "recommendations": recommendations
    }


# ============================================================
# GENERATE GAP REPORT
# ============================================================

def generate_gap_report(
    identified_skills: List[str],
    career: str
) -> Dict[str, Any]:
    """
    Generate a complete career skill-gap report.
    """

    report = calculate_skill_gap(
        identified_skills,
        career
    )

    if report["skill_alignment"] >= 80:

        readiness = "Excellent"

    elif report["skill_alignment"] >= 60:

        readiness = "Good"

    elif report["skill_alignment"] >= 40:

        readiness = "Moderate"

    else:

        readiness = "Needs Improvement"

    report["career_readiness"] = readiness

    report["summary"] = (
        f"You currently match "
        f"{len(report['matched_skills'])} out of "
        f"{len(report['required_skills'])} required skills "
        f"for {career}."
    )

    return report


# ============================================================
# TEST MODULE
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("CAREERCAST - MILESTONE 3 - STEP 3")
    print("SKILL GAP ANALYSIS ENGINE")
    print("=" * 70)

    sample_skills = [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch"
    ]

    sample_career = "Deep Learning Engineer"

    report = generate_gap_report(
        sample_skills,
        sample_career
    )

    print()
    print("Career:")
    print(report["career"])

    print()
    print("Required Skills:")
    print(report["required_skills"])

    print()
    print("Identified Skills:")
    print(report["identified_skills"])

    print()
    print("Matched Skills:")
    print(report["matched_skills"])

    print()
    print("Missing Skills:")
    print(report["missing_skills"])

    print()
    print(
        "Skill Alignment:",
        f"{report['skill_alignment']}%"
    )

    print(
        "Skill Gap:",
        f"{report['skill_gap_percentage']}%"
    )

    print(
        "Career Readiness:",
        report["career_readiness"]
    )

    print()
    print("ACTIONABLE RECOMMENDATIONS")
    print("-" * 70)

    for recommendation in report["recommendations"]:

        print()
        print(
            f"Skill: {recommendation['skill']}"
        )

        print(
            f"Priority: {recommendation['priority']}"
        )

        print(
            f"Action: {recommendation['action']}"
        )

        print(
            f"Project: {recommendation['project']}"
        )

    print()
    print("=" * 70)
    print("✓ SKILL GAP ANALYSIS ENGINE VERIFIED")
    print("=" * 70)