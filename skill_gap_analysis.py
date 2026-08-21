"""
CareerCast - Milestone 3
Step 2: Skill Gap Analysis Engine

This module:
1. Extracts skills from resume text.
2. Determines required skills for a career.
3. Calculates matched and missing skills.
4. Calculates skill alignment.
5. Assigns learning priority.
6. Generates actionable improvement suggestions.
7. Produces a complete gap report.
"""

import re
from typing import Dict, List, Any


# ============================================================
# SKILL DATABASE
# ============================================================

SKILL_DATABASE = {

    "Python": [
        "python"
    ],

    "Java": [
        "java"
    ],

    "JavaScript": [
        "javascript",
        "js"
    ],

    "C++": [
        "c++"
    ],

    "SQL": [
        "sql",
        "mysql",
        "postgresql",
        "postgres"
    ],

    "HTML": [
        "html"
    ],

    "CSS": [
        "css"
    ],

    "React": [
        "react",
        "reactjs"
    ],

    "Node.js": [
        "node.js",
        "nodejs",
        "node"
    ],

    "Django": [
        "django"
    ],

    "Flask": [
        "flask"
    ],

    "Machine Learning": [
        "machine learning",
        "machine-learning"
    ],

    "Deep Learning": [
        "deep learning",
        "deep-learning"
    ],

    "Artificial Intelligence": [
        "artificial intelligence",
        "artificial-intelligence",
        "ai"
    ],

    "TensorFlow": [
        "tensorflow"
    ],

    "PyTorch": [
        "pytorch"
    ],

    "Scikit-learn": [
        "scikit-learn",
        "sklearn"
    ],

    "Pandas": [
        "pandas"
    ],

    "NumPy": [
        "numpy"
    ],

    "Data Analysis": [
        "data analysis",
        "data analytics"
    ],

    "Data Visualization": [
        "data visualization",
        "data visualisation"
    ],

    "Power BI": [
        "power bi"
    ],

    "Tableau": [
        "tableau"
    ],

    "AWS": [
        "aws",
        "amazon web services"
    ],

    "Azure": [
        "azure",
        "microsoft azure"
    ],

    "Google Cloud": [
        "google cloud",
        "gcp"
    ],

    "Docker": [
        "docker"
    ],

    "Kubernetes": [
        "kubernetes"
    ],

    "Git": [
        "git"
    ],

    "GitHub": [
        "github"
    ],

    "Cybersecurity": [
        "cybersecurity",
        "cyber security"
    ],

    "Ethical Hacking": [
        "ethical hacking",
        "ethical hacker"
    ],

    "Networking": [
        "networking",
        "computer networks"
    ],

    "Linux": [
        "linux"
    ],

    "Figma": [
        "figma"
    ],

    "UI/UX": [
        "ui/ux",
        "ui ux",
        "user experience",
        "user interface"
    ],

    "Graphic Design": [
        "graphic design",
        "graphic designing"
    ],

    "SEO": [
        "seo",
        "search engine optimization"
    ],

    "Digital Marketing": [
        "digital marketing"
    ],

    "Project Management": [
        "project management"
    ],

    "Communication": [
        "communication"
    ],

    "Leadership": [
        "leadership"
    ],

    "Teamwork": [
        "teamwork",
        "team work"
    ]
}


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
# ACTIONABLE LEARNING SUGGESTIONS
# ============================================================

SKILL_SUGGESTIONS = {

    "Python": {
        "priority": "High",
        "category": "Programming",
        "suggestion": (
            "Strengthen Python by building practical applications "
            "and solving programming problems."
        ),
        "project": (
            "Build a Python application using APIs, data processing, "
            "error handling and testing."
        )
    },

    "Java": {
        "priority": "Medium",
        "category": "Programming",
        "suggestion": (
            "Learn object-oriented programming, collections, "
            "exception handling and Java application development."
        ),
        "project": (
            "Build a Java-based REST API or backend application."
        )
    },

    "JavaScript": {
        "priority": "High",
        "category": "Web Development",
        "suggestion": (
            "Strengthen modern JavaScript including ES6+, "
            "async programming, DOM manipulation and APIs."
        ),
        "project": (
            "Build an interactive web application using JavaScript."
        )
    },

    "SQL": {
        "priority": "High",
        "category": "Database",
        "suggestion": (
            "Practice joins, subqueries, aggregation, indexing "
            "and database design."
        ),
        "project": (
            "Build a database-driven application with complex SQL queries."
        )
    },

    "HTML": {
        "priority": "Medium",
        "category": "Web Development",
        "suggestion": (
            "Learn semantic HTML, forms, accessibility and "
            "modern page structure."
        ),
        "project": (
            "Build a responsive multi-page website."
        )
    },

    "CSS": {
        "priority": "Medium",
        "category": "Web Development",
        "suggestion": (
            "Practice responsive layouts, Flexbox, Grid, "
            "animations and modern CSS."
        ),
        "project": (
            "Create a responsive portfolio or dashboard."
        )
    },

    "React": {
        "priority": "High",
        "category": "Frontend Development",
        "suggestion": (
            "Learn React components, hooks, state management, "
            "routing and API integration."
        ),
        "project": (
            "Build a React dashboard connected to a REST API."
        )
    },

    "Node.js": {
        "priority": "High",
        "category": "Backend Development",
        "suggestion": (
            "Learn Node.js, Express, REST APIs, middleware "
            "and asynchronous programming."
        ),
        "project": (
            "Build a Node.js REST API with database integration."
        )
    },

    "Django": {
        "priority": "High",
        "category": "Backend Development",
        "suggestion": (
            "Learn Django models, views, serializers, authentication "
            "and REST API development."
        ),
        "project": (
            "Build a Django REST application."
        )
    },

    "Flask": {
        "priority": "Medium",
        "category": "Backend Development",
        "suggestion": (
            "Learn Flask routing, REST APIs, validation, "
            "authentication and deployment."
        ),
        "project": (
            "Build and deploy a Flask REST API."
        )
    },

    "Machine Learning": {
        "priority": "High",
        "category": "Artificial Intelligence",
        "suggestion": (
            "Study supervised and unsupervised learning, "
            "feature engineering, model evaluation and tuning."
        ),
        "project": (
            "Build an end-to-end machine learning prediction system."
        )
    },

    "Deep Learning": {
        "priority": "High",
        "category": "Artificial Intelligence",
        "suggestion": (
            "Learn neural networks, CNNs, RNNs, transformers "
            "and model optimization."
        ),
        "project": (
            "Build a deep learning image or text classification project."
        )
    },

    "Artificial Intelligence": {
        "priority": "High",
        "category": "Artificial Intelligence",
        "suggestion": (
            "Develop knowledge of AI concepts, intelligent systems, "
            "machine learning and modern generative AI."
        ),
        "project": (
            "Build an AI-powered application solving a real-world problem."
        )
    },

    "TensorFlow": {
        "priority": "High",
        "category": "Deep Learning Framework",
        "suggestion": (
            "Learn TensorFlow model creation, training, evaluation "
            "and deployment."
        ),
        "project": (
            "Train and deploy a TensorFlow neural network."
        )
    },

    "PyTorch": {
        "priority": "High",
        "category": "Deep Learning Framework",
        "suggestion": (
            "Practice tensors, neural networks, training loops "
            "and model deployment using PyTorch."
        ),
        "project": (
            "Build and train a PyTorch deep learning model."
        )
    },

    "Scikit-learn": {
        "priority": "High",
        "category": "Machine Learning Framework",
        "suggestion": (
            "Practice preprocessing, pipelines, classification, "
            "regression, clustering and model evaluation."
        ),
        "project": (
            "Build a complete Scikit-learn ML pipeline."
        )
    },

    "Pandas": {
        "priority": "Medium",
        "category": "Data Analysis",
        "suggestion": (
            "Practice DataFrames, data cleaning, grouping, "
            "merging and feature preparation."
        ),
        "project": (
            "Clean and analyze a real-world dataset using Pandas."
        )
    },

    "NumPy": {
        "priority": "Medium",
        "category": "Data Science",
        "suggestion": (
            "Learn arrays, vectorization, broadcasting and "
            "numerical operations."
        ),
        "project": (
            "Implement numerical data-processing algorithms with NumPy."
        )
    },

    "Data Analysis": {
        "priority": "High",
        "category": "Analytics",
        "suggestion": (
            "Improve data cleaning, exploratory analysis, "
            "statistical reasoning and insight generation."
        ),
        "project": (
            "Perform an end-to-end exploratory data analysis project."
        )
    },

    "Data Visualization": {
        "priority": "Medium",
        "category": "Analytics",
        "suggestion": (
            "Learn how to select and create effective charts "
            "for communicating analytical findings."
        ),
        "project": (
            "Create an interactive analytics dashboard."
        )
    },

    "Power BI": {
        "priority": "Medium",
        "category": "Business Intelligence",
        "suggestion": (
            "Learn Power BI data modeling, DAX, dashboards "
            "and interactive reports."
        ),
        "project": (
            "Build a business intelligence dashboard in Power BI."
        )
    },

    "Tableau": {
        "priority": "Medium",
        "category": "Business Intelligence",
        "suggestion": (
            "Practice Tableau dashboards, calculated fields "
            "and interactive visualizations."
        ),
        "project": (
            "Build a Tableau dashboard using a real-world dataset."
        )
    },

    "AWS": {
        "priority": "High",
        "category": "Cloud",
        "suggestion": (
            "Learn AWS compute, storage, networking, IAM "
            "and deployment fundamentals."
        ),
        "project": (
            "Deploy an application on AWS."
        )
    },

    "Azure": {
        "priority": "High",
        "category": "Cloud",
        "suggestion": (
            "Learn Azure compute, storage, networking "
            "and application deployment."
        ),
        "project": (
            "Deploy a web application using Azure services."
        )
    },

    "Google Cloud": {
        "priority": "High",
        "category": "Cloud",
        "suggestion": (
            "Learn Google Cloud compute, storage, IAM "
            "and deployment fundamentals."
        ),
        "project": (
            "Deploy a cloud application using Google Cloud."
        )
    },

    "Docker": {
        "priority": "High",
        "category": "DevOps",
        "suggestion": (
            "Learn Docker images, containers, Dockerfiles, "
            "volumes and networking."
        ),
        "project": (
            "Containerize a complete web application."
        )
    },

    "Kubernetes": {
        "priority": "High",
        "category": "DevOps",
        "suggestion": (
            "Learn Kubernetes pods, deployments, services "
            "and configuration management."
        ),
        "project": (
            "Deploy a containerized application on Kubernetes."
        )
    },

    "Git": {
        "priority": "High",
        "category": "Development Tools",
        "suggestion": (
            "Practice branching, merging, pull requests, "
            "rebasing and collaborative Git workflows."
        ),
        "project": (
            "Manage a multi-feature project using Git branches."
        )
    },

    "GitHub": {
        "priority": "Medium",
        "category": "Development Tools",
        "suggestion": (
            "Learn GitHub repositories, pull requests, issues "
            "and collaborative development."
        ),
        "project": (
            "Publish a complete project on GitHub with documentation."
        )
    },

    "Cybersecurity": {
        "priority": "High",
        "category": "Cybersecurity",
        "suggestion": (
            "Study security principles, vulnerabilities, "
            "threats, defensive controls and security monitoring."
        ),
        "project": (
            "Build a vulnerability analysis or security monitoring project."
        )
    },

    "Ethical Hacking": {
        "priority": "High",
        "category": "Cybersecurity",
        "suggestion": (
            "Study ethical hacking methodology, reconnaissance, "
            "web security and defensive testing."
        ),
        "project": (
            "Create a controlled security-testing lab."
        )
    },

    "Networking": {
        "priority": "High",
        "category": "Networking",
        "suggestion": (
            "Learn TCP/IP, DNS, HTTP, routing, switching "
            "and network troubleshooting."
        ),
        "project": (
            "Design and document a simulated enterprise network."
        )
    },

    "Linux": {
        "priority": "Medium",
        "category": "Operating Systems",
        "suggestion": (
            "Practice Linux commands, permissions, processes, "
            "shell scripting and system administration."
        ),
        "project": (
            "Deploy and administer a Linux-based application server."
        )
    },

    "Figma": {
        "priority": "High",
        "category": "Design",
        "suggestion": (
            "Learn Figma components, auto-layout, prototyping "
            "and design systems."
        ),
        "project": (
            "Design a complete application interface in Figma."
        )
    },

    "UI/UX": {
        "priority": "High",
        "category": "Design",
        "suggestion": (
            "Study user research, information architecture, "
            "wireframing, prototyping and usability."
        ),
        "project": (
            "Design a complete user journey and interactive prototype."
        )
    },

    "Graphic Design": {
        "priority": "Medium",
        "category": "Design",
        "suggestion": (
            "Practice typography, composition, visual hierarchy "
            "and branding."
        ),
        "project": (
            "Create a complete visual identity for a fictional product."
        )
    },

    "SEO": {
        "priority": "High",
        "category": "Digital Marketing",
        "suggestion": (
            "Learn keyword research, on-page SEO, technical SEO "
            "and search performance analysis."
        ),
        "project": (
            "Perform SEO optimization and analysis for a website."
        )
    },

    "Digital Marketing": {
        "priority": "High",
        "category": "Marketing",
        "suggestion": (
            "Learn digital campaigns, content strategy, "
            "analytics and audience targeting."
        ),
        "project": (
            "Design and analyze a complete digital marketing campaign."
        )
    },

    "Project Management": {
        "priority": "High",
        "category": "Management",
        "suggestion": (
            "Learn project planning, scheduling, risk management "
            "and Agile methodologies."
        ),
        "project": (
            "Create and manage a complete software project plan."
        )
    },

    "Communication": {
        "priority": "Medium",
        "category": "Soft Skills",
        "suggestion": (
            "Improve technical communication, presentations "
            "and professional writing."
        ),
        "project": (
            "Prepare and present a technical project demonstration."
        )
    },

    "Leadership": {
        "priority": "Medium",
        "category": "Management",
        "suggestion": (
            "Develop decision-making, delegation, team coordination "
            "and leadership skills."
        ),
        "project": (
            "Lead a small team project with defined responsibilities."
        )
    },

    "Teamwork": {
        "priority": "Medium",
        "category": "Soft Skills",
        "suggestion": (
            "Practice collaboration, conflict resolution "
            "and effective team communication."
        ),
        "project": (
            "Contribute to a collaborative software project."
        )
    }
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def clean_text(text: str) -> str:
    """
    Normalize resume text before skill extraction.
    """

    if text is None:
        return ""

    text = str(text)

    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("\t", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(text: str) -> List[str]:
    """
    Extract recognized skills from resume text.
    """

    text = clean_text(text)

    if not text:
        return []

    text_lower = text.lower()

    detected = []

    for skill, keywords in SKILL_DATABASE.items():

        for keyword in keywords:

            pattern = (
                r"(?<![a-zA-Z0-9])"
                + re.escape(keyword.lower())
                + r"(?![a-zA-Z0-9])"
            )

            if re.search(
                pattern,
                text_lower
            ):

                detected.append(skill)

                break

    return sorted(
        set(detected)
    )


# ============================================================
# CAREER VALIDATION
# ============================================================

def get_supported_careers() -> List[str]:
    """
    Return all supported CareerCast careers.
    """

    return sorted(
        CAREER_SKILLS.keys()
    )


def validate_career(career: str) -> None:
    """
    Validate requested career.
    """

    if not career:
        raise ValueError(
            "Career cannot be empty."
        )

    if career not in CAREER_SKILLS:

        raise ValueError(
            f"Unsupported career: {career}. "
            f"Supported careers: {get_supported_careers()}"
        )


# ============================================================
# REQUIRED SKILLS
# ============================================================

def get_required_skills(
    career: str
) -> List[str]:

    validate_career(career)

    return list(
        CAREER_SKILLS[career]
    )


# ============================================================
# SKILL ALIGNMENT
# ============================================================

def calculate_alignment(
    matched_count: int,
    required_count: int
) -> float:

    if required_count <= 0:
        return 0.0

    alignment = (
        matched_count /
        required_count
    ) * 100.0

    return round(
        min(alignment, 100.0),
        2
    )


# ============================================================
# GAP SEVERITY
# ============================================================

def determine_gap_severity(
    alignment: float
) -> str:

    if alignment >= 80:
        return "Low"

    if alignment >= 50:
        return "Medium"

    return "High"


# ============================================================
# LEARNING PRIORITY
# ============================================================

def calculate_learning_priority(
    missing_skill: str,
    gap_severity: str
) -> str:

    skill_information = SKILL_SUGGESTIONS.get(
        missing_skill,
        {}
    )

    base_priority = skill_information.get(
        "priority",
        "Medium"
    )

    if gap_severity == "High":
        if base_priority == "Medium":
            return "High"

    return base_priority


# ============================================================
# ACTIONABLE SUGGESTION
# ============================================================

def generate_skill_suggestion(
    skill: str,
    gap_severity: str
) -> Dict[str, Any]:

    information = SKILL_SUGGESTIONS.get(
        skill
    )

    if information is None:

        return {
            "skill": skill,
            "priority": (
                "High"
                if gap_severity == "High"
                else "Medium"
            ),
            "category": "General",
            "suggestion": (
                f"Develop practical competency in {skill} "
                "through structured learning and hands-on practice."
            ),
            "project": (
                f"Build a practical project demonstrating {skill}."
            )
        }

    priority = calculate_learning_priority(
        skill,
        gap_severity
    )

    return {
        "skill": skill,
        "priority": priority,
        "category": information["category"],
        "suggestion": information["suggestion"],
        "project": information["project"]
    }


# ============================================================
# COMPLETE CAREER GAP ANALYSIS
# ============================================================

def analyze_skill_gap(
    resume_text: str,
    career: str
) -> Dict[str, Any]:
    """
    Generate a complete skill gap report.
    """

    if not resume_text or not str(
        resume_text
    ).strip():

        raise ValueError(
            "Resume text cannot be empty."
        )

    validate_career(
        career
    )

    # --------------------------------------------------------
    # Extract skills
    # --------------------------------------------------------

    identified_skills = extract_skills(
        resume_text
    )

    identified_set = {
        skill.lower()
        for skill in identified_skills
    }

    # --------------------------------------------------------
    # Required skills
    # --------------------------------------------------------

    required_skills = get_required_skills(
        career
    )

    # --------------------------------------------------------
    # Matched / Missing
    # --------------------------------------------------------

    matched_skills = []

    missing_skills = []

    for skill in required_skills:

        if skill.lower() in identified_set:

            matched_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )

    # --------------------------------------------------------
    # Alignment
    # --------------------------------------------------------

    alignment = calculate_alignment(
        len(matched_skills),
        len(required_skills)
    )

    # --------------------------------------------------------
    # Gap severity
    # --------------------------------------------------------

    gap_severity = determine_gap_severity(
        alignment
    )

    # --------------------------------------------------------
    # Actionable recommendations
    # --------------------------------------------------------

    recommendations = []

    for skill in missing_skills:

        recommendations.append(
            generate_skill_suggestion(
                skill,
                gap_severity
            )
        )

    # --------------------------------------------------------
    # Learning priority order
    # --------------------------------------------------------

    priority_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2
    }

    recommendations.sort(
        key=lambda item: priority_order.get(
            item["priority"],
            1
        )
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    total_required = len(
        required_skills
    )

    total_matched = len(
        matched_skills
    )

    total_missing = len(
        missing_skills
    )

    return {

        "career": career,

        "skill_alignment": alignment,

        "gap_severity": gap_severity,

        "total_required_skills": total_required,

        "matched_skill_count": total_matched,

        "missing_skill_count": total_missing,

        "identified_skills": identified_skills,

        "required_skills": required_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "recommendations": recommendations
    }


# ============================================================
# TOP-5 CAREER GAP ANALYSIS
# ============================================================

def analyze_multiple_careers(
    resume_text: str,
    careers: List[str]
) -> List[Dict[str, Any]]:
    """
    Generate skill-gap reports for multiple careers.
    """

    if not careers:
        return []

    reports = []

    for career in careers:

        report = analyze_skill_gap(
            resume_text,
            career
        )

        reports.append(
            report
        )

    reports.sort(
        key=lambda item: item["skill_alignment"],
        reverse=True
    )

    return reports


# ============================================================
# SIMPLE REPORT SUMMARY
# ============================================================

def generate_gap_summary(
    report: Dict[str, Any]
) -> str:

    career = report["career"]
    alignment = report["skill_alignment"]
    severity = report["gap_severity"]

    missing = report["missing_skills"]

    if not missing:

        return (
            f"You have strong alignment with {career} "
            f"at {alignment}%. No major required skills "
            "were identified as missing."
        )

    missing_text = ", ".join(
        missing
    )

    return (
        f"Your current skill alignment with {career} "
        f"is {alignment}%, indicating a {severity.lower()} "
        f"skill gap. Priority skills to develop: "
        f"{missing_text}."
    )


# ============================================================
# MODULE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("CAREERCAST - MILESTONE 3")
    print("STEP 2 - SKILL GAP ANALYSIS ENGINE")
    print("=" * 70)

    sample_resume = """
    Python developer with experience in machine learning,
    deep learning, TensorFlow, PyTorch, NumPy, Pandas,
    scikit-learn and artificial intelligence.
    """

    sample_career = "Machine Learning Engineer"

    print()
    print("Sample Career:")
    print(sample_career)

    print()
    print("Extracted Skills:")
    print("-" * 70)

    skills = extract_skills(
        sample_resume
    )

    for skill in skills:
        print("✓", skill)

    print()
    print("Generating Skill Gap Report...")
    print("-" * 70)

    report = analyze_skill_gap(
        sample_resume,
        sample_career
    )

    print()
    print("Career:", report["career"])
    print(
        "Skill Alignment:",
        str(report["skill_alignment"]) + "%"
    )
    print(
        "Gap Severity:",
        report["gap_severity"]
    )

    print()
    print("Required Skills:")
    for skill in report["required_skills"]:
        print("  -", skill)

    print()
    print("Matched Skills:")
    for skill in report["matched_skills"]:
        print("  ✓", skill)

    print()
    print("Missing Skills:")
    for skill in report["missing_skills"]:
        print("  ✗", skill)

    print()
    print("Actionable Recommendations:")
    print("-" * 70)

    for item in report["recommendations"]:

        print()
        print("Skill:", item["skill"])
        print("Priority:", item["priority"])
        print("Category:", item["category"])
        print("Suggestion:", item["suggestion"])
        print("Project:", item["project"])

    print()
    print("Summary:")
    print(
        generate_gap_summary(report)
    )

    print()
    print("=" * 70)
    print("STEP 2 SKILL GAP ENGINE TEST COMPLETE")
    print("=" * 70)