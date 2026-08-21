from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime
import os
import re
import traceback

from pypdf import PdfReader
from docx import Document

# ============================================================
# CAREERCAST MILESTONE 3
# FASTAPI REST SERVICE
# ============================================================

app = FastAPI(
    title="CareerCast AI Career Intelligence API",
    description="""
    CareerCast Milestone 3 REST API.

    Provides:
    - Career prediction
    - Top-K career recommendation
    - Skill gap analysis
    - Actionable competency improvement suggestions
    - Complete career gap report
    """,
    version="3.0.0"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR / "models"
UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# IMPORT MILESTONE 2 RECOMMENDATION ENGINE
# ============================================================

try:

    from career_recommendation_engine import (
        recommend_careers
    )

    RECOMMENDATION_ENGINE_AVAILABLE = True

    print("=" * 70)
    print("CAREERCAST MILESTONE 3")
    print("Recommendation engine imported successfully")
    print("=" * 70)

except Exception as e:

    RECOMMENDATION_ENGINE_AVAILABLE = False

    print("=" * 70)
    print("WARNING: Recommendation engine import failed")
    print(str(e))
    print("=" * 70)


# ============================================================
# CAREER SKILL DATABASE
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
# GENERAL SKILL DATABASE
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

    "FastAPI": [
        "fastapi"
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
        "artificial-intelligence"
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
# ACTIONABLE SKILL DEVELOPMENT DATABASE
# ============================================================

SKILL_SUGGESTIONS = {

    "Python": {
        "priority": "High",
        "action": "Practice Python programming, data structures and object-oriented programming.",
        "project": "Build a Python-based automation or data-processing project."
    },

    "Machine Learning": {
        "priority": "High",
        "action": "Study supervised and unsupervised learning algorithms and model evaluation.",
        "project": "Build an end-to-end machine learning prediction project."
    },

    "Deep Learning": {
        "priority": "High",
        "action": "Learn neural networks, CNNs, RNNs and transformer architectures.",
        "project": "Build an image or text classification system."
    },

    "Artificial Intelligence": {
        "priority": "High",
        "action": "Study AI fundamentals, search, reasoning and intelligent-agent concepts.",
        "project": "Build an AI-powered application."
    },

    "TensorFlow": {
        "priority": "Medium",
        "action": "Practice neural-network development and model training using TensorFlow.",
        "project": "Create and train a TensorFlow classification model."
    },

    "PyTorch": {
        "priority": "Medium",
        "action": "Practice deep-learning model development using PyTorch.",
        "project": "Build and train a PyTorch neural network."
    },

    "Scikit-learn": {
        "priority": "Medium",
        "action": "Practice preprocessing, feature engineering, classification and regression.",
        "project": "Create a complete Scikit-learn ML pipeline."
    },

    "SQL": {
        "priority": "High",
        "action": "Practice joins, subqueries, aggregation, window functions and database design.",
        "project": "Build a relational database analytics project."
    },

    "Data Analysis": {
        "priority": "High",
        "action": "Practice exploratory data analysis, statistics and data interpretation.",
        "project": "Analyze a real-world dataset and create an insight report."
    },

    "Pandas": {
        "priority": "Medium",
        "action": "Practice dataframe manipulation, filtering, grouping and data cleaning.",
        "project": "Build a reusable data-cleaning pipeline."
    },

    "NumPy": {
        "priority": "Medium",
        "action": "Practice arrays, vectorized operations and numerical computation.",
        "project": "Implement numerical-analysis utilities using NumPy."
    },

    "HTML": {
        "priority": "Medium",
        "action": "Learn semantic HTML and accessible web-page structure.",
        "project": "Build a responsive portfolio page."
    },

    "CSS": {
        "priority": "Medium",
        "action": "Practice layouts, Flexbox, Grid, responsive design and animations.",
        "project": "Build a responsive dashboard."
    },

    "JavaScript": {
        "priority": "High",
        "action": "Practice modern JavaScript, DOM manipulation, asynchronous programming and APIs.",
        "project": "Build an interactive web application."
    },

    "React": {
        "priority": "High",
        "action": "Learn components, hooks, state management and API integration.",
        "project": "Build a React frontend connected to a REST API."
    },

    "Node.js": {
        "priority": "Medium",
        "action": "Learn server-side JavaScript and REST API development.",
        "project": "Build a Node.js REST API."
    },

    "Git": {
        "priority": "Medium",
        "action": "Practice branching, merging, commits and collaborative workflows.",
        "project": "Maintain a project using Git feature branches."
    },

    "Linux": {
        "priority": "Medium",
        "action": "Practice Linux commands, permissions, processes and shell scripting.",
        "project": "Create shell scripts for system automation."
    },

    "Docker": {
        "priority": "Medium",
        "action": "Learn containers, images, Dockerfiles and networking.",
        "project": "Containerize a machine-learning or web application."
    },

    "AWS": {
        "priority": "Medium",
        "action": "Learn core AWS compute, storage, networking and deployment services.",
        "project": "Deploy a web application on AWS."
    },

    "Cybersecurity": {
        "priority": "High",
        "action": "Study network security, authentication, vulnerabilities and security monitoring.",
        "project": "Build a security monitoring or vulnerability-analysis project."
    },

    "Networking": {
        "priority": "High",
        "action": "Study TCP/IP, DNS, HTTP, routing and network security.",
        "project": "Create a network-monitoring project."
    },

    "Ethical Hacking": {
        "priority": "High",
        "action": "Learn penetration-testing methodology and defensive security practices.",
        "project": "Build a controlled security-testing lab."
    },

    "Figma": {
        "priority": "High",
        "action": "Practice wireframing, prototyping, components and design systems.",
        "project": "Design a complete application prototype."
    },

    "UI/UX": {
        "priority": "High",
        "action": "Study user research, information architecture and usability principles.",
        "project": "Design and evaluate a complete user experience."
    },

    "Graphic Design": {
        "priority": "Medium",
        "action": "Practice typography, composition, branding and visual hierarchy.",
        "project": "Create a professional branding portfolio."
    },

    "SEO": {
        "priority": "Medium",
        "action": "Learn keyword research, on-page SEO, technical SEO and analytics.",
        "project": "Optimize a website and measure search performance."
    },

    "Digital Marketing": {
        "priority": "Medium",
        "action": "Learn content marketing, campaigns, analytics and digital strategy.",
        "project": "Create and evaluate a digital marketing campaign."
    },

    "Communication": {
        "priority": "Medium",
        "action": "Improve technical communication, presentation and professional writing.",
        "project": "Prepare and present a technical project."
    },

    "Leadership": {
        "priority": "Medium",
        "action": "Develop decision-making, delegation and team leadership skills.",
        "project": "Lead a small project from planning to delivery."
    },

    "Teamwork": {
        "priority": "Medium",
        "action": "Practice collaborative planning, communication and conflict resolution.",
        "project": "Contribute to a collaborative software project."
    },

    "Project Management": {
        "priority": "High",
        "action": "Learn Agile, Scrum, planning, estimation and risk management.",
        "project": "Manage a project using a Scrum-style workflow."
    },

    "Power BI": {
        "priority": "Medium",
        "action": "Learn dashboards, data modeling, DAX and business reporting.",
        "project": "Build an interactive business intelligence dashboard."
    },

    "Tableau": {
        "priority": "Medium",
        "action": "Practice visualization, dashboards and analytical storytelling.",
        "project": "Create an interactive Tableau analytics dashboard."
    },

    "Java": {
        "priority": "Medium",
        "action": "Practice Java OOP, collections, exception handling and backend development.",
        "project": "Build a Java-based backend application."
    },

    "Django": {
        "priority": "Medium",
        "action": "Learn Django models, views, templates, authentication and REST APIs.",
        "project": "Build a Django web application."
    },

    "Flask": {
        "priority": "Medium",
        "action": "Practice Flask routing, APIs, templates and deployment.",
        "project": "Build a Flask REST application."
    }
}


# ============================================================
# PYDANTIC REQUEST MODELS
# ============================================================

class ResumeRequest(BaseModel):

    resume_text: str = Field(
        ...,
        min_length=20,
        description="Resume or candidate profile text."
    )


class RecommendationRequest(BaseModel):

    resume_text: str = Field(
        ...,
        min_length=20
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=22
    )


class GapRequest(BaseModel):

    resume_text: str = Field(
        ...,
        min_length=20
    )

    career: Optional[str] = None


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text: str) -> str:

    text = str(text)

    text = text.replace(
        "\n",
        " "
    )

    text = text.replace(
        "\r",
        " "
    )

    text = text.replace(
        "\t",
        " "
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# EXTRACT TEXT FROM PDF
# ============================================================

def extract_pdf_text(file_path: Path) -> str:

    reader = PdfReader(
        str(file_path)
    )

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:

            pages.append(text)

    return "\n".join(pages)


# ============================================================
# EXTRACT TEXT FROM DOCX
# ============================================================

def extract_docx_text(file_path: Path) -> str:

    document = Document(
        str(file_path)
    )

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            paragraphs.append(
                paragraph.text.strip()
            )

    return "\n".join(paragraphs)


# ============================================================
# EXTRACT TEXT FROM TXT
# ============================================================

def extract_txt_text(file_path: Path) -> str:

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        return file.read()


# ============================================================
# RESUME FILE EXTRACTION
# ============================================================

def extract_resume_file(
    file_path: Path
) -> str:

    extension = file_path.suffix.lower()

    if extension == ".pdf":

        return extract_pdf_text(
            file_path
        )

    if extension == ".docx":

        return extract_docx_text(
            file_path
        )

    if extension == ".txt":

        return extract_txt_text(
            file_path
        )

    raise ValueError(
        "Unsupported file type. "
        "Use PDF, DOCX or TXT."
    )


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(
    text: str
) -> List[str]:

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

                detected.append(
                    skill
                )

                break

    return sorted(
        list(
            set(detected)
        )
    )


# ============================================================
# NORMALIZE CAREER NAME
# ============================================================

def normalize_career_name(
    career: str
) -> Optional[str]:

    if not career:

        return None

    career_lower = career.strip().lower()

    for known_career in CAREER_SKILLS:

        if known_career.lower() == career_lower:

            return known_career

    return None


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

def calculate_gap(
    identified_skills: List[str],
    career: str
) -> Dict[str, Any]:

    career = normalize_career_name(
        career
    )

    if career is None:

        raise ValueError(
            "Unknown career. "
            "Please provide a career supported by CareerCast."
        )

    required_skills = CAREER_SKILLS[
        career
    ]

    identified_set = {
        skill.lower()
        for skill in identified_skills
    }

    matched = []
    missing = []

    for skill in required_skills:

        if skill.lower() in identified_set:

            matched.append(skill)

        else:

            missing.append(skill)

    total = len(
        required_skills
    )

    alignment = (
        len(matched) / total * 100
        if total > 0
        else 0
    )

    return {

        "career": career,

        "required_skills":
            required_skills,

        "matched_skills":
            matched,

        "missing_skills":
            missing,

        "alignment":
            round(
                alignment,
                2
            ),

        "required_skill_count":
            total,

        "matched_skill_count":
            len(matched),

        "missing_skill_count":
            len(missing)
    }


# ============================================================
# ACTIONABLE IMPROVEMENT SUGGESTIONS
# ============================================================

def generate_suggestions(
    missing_skills: List[str]
) -> List[Dict[str, Any]]:

    suggestions = []

    for skill in missing_skills:

        information = SKILL_SUGGESTIONS.get(
            skill,
            {
                "priority": "Medium",
                "action":
                    f"Develop practical competency in {skill}.",
                "project":
                    f"Build a practical project demonstrating {skill}."
            }
        )

        suggestions.append({

            "skill": skill,

            "priority":
                information["priority"],

            "action":
                information["action"],

            "project":
                information["project"]
        })

    return suggestions


# ============================================================
# BUILD GAP REPORT
# ============================================================

def build_gap_report(
    resume_text: str,
    career: Optional[str] = None
) -> Dict[str, Any]:

    resume_text = clean_text(
        resume_text
    )

    identified_skills = extract_skills(
        resume_text
    )

    # --------------------------------------------------------
    # If career was not provided, use recommendation engine
    # --------------------------------------------------------

    recommendations = []

    if career is None:

        if not RECOMMENDATION_ENGINE_AVAILABLE:

            raise RuntimeError(
                "Recommendation engine is unavailable."
            )

        recommendations = recommend_careers(
            resume_text,
            top_k=5
        )

        if not recommendations:

            raise RuntimeError(
                "No career recommendations were generated."
            )

        career = recommendations[0]["career"]

    else:

        career = normalize_career_name(
            career
        )

        if career is None:

            raise ValueError(
                "Unknown career."
            )

    # --------------------------------------------------------
    # Calculate skill gap
    # --------------------------------------------------------

    gap = calculate_gap(
        identified_skills,
        career
    )

    suggestions = generate_suggestions(
        gap["missing_skills"]
    )

    return {

        "generated_at":
            datetime.utcnow().isoformat() + "Z",

        "recommended_career":
            career,

        "identified_skills":
            identified_skills,

        "skill_gap":
            gap,

        "actionable_improvement_plan":
            suggestions,

        "recommendations":
            recommendations,

        "resume_text_length":
            len(resume_text)
    }


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {

        "application":
            "CareerCast",

        "milestone":
            "Milestone 3",

        "version":
            "3.0.0",

        "status":
            "running",

        "services": [

            "Career Prediction",

            "Top-K Recommendation",

            "Skill Gap Analysis",

            "Actionable Improvement Suggestions",

            "Career Gap Report"
        ],

        "documentation":
            "/docs"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    model_files = {

        "random_forest":
            MODEL_DIR / "random_forest.pkl",

        "xgboost":
            MODEL_DIR / "xgboost.pkl",

        "sentence_bert_embeddings":
            MODEL_DIR /
            "sentence_bert_career_embeddings.pkl"
    }

    model_status = {

        name:
            path.exists()

        for name, path
        in model_files.items()
    }

    return {

        "status":
            "healthy",

        "recommendation_engine":
            RECOMMENDATION_ENGINE_AVAILABLE,

        "models":
            model_status,

        "timestamp":
            datetime.utcnow().isoformat() + "Z"
    }


# ============================================================
# PREDICTION ENDPOINT
# ============================================================

@app.post("/predict")
def predict(
    request: ResumeRequest
):

    try:

        if not RECOMMENDATION_ENGINE_AVAILABLE:

            raise HTTPException(
                status_code=503,
                detail=
                    "Recommendation engine is unavailable."
            )

        resume_text = clean_text(
            request.resume_text
        )

        recommendations = recommend_careers(
            resume_text,
            top_k=5
        )

        if not recommendations:

            raise HTTPException(
                status_code=500,
                detail=
                    "No prediction was generated."
            )

        top_prediction = (
            recommendations[0]
        )

        return {

            "success":
                True,

            "prediction":
                top_prediction["career"],

            "confidence":
                top_prediction["hybrid_score"],

            "model_scores": {

                "random_forest":
                    top_prediction[
                        "random_forest_confidence"
                    ],

                "xgboost":
                    top_prediction[
                        "xgboost_confidence"
                    ],

                "sentence_bert":
                    top_prediction[
                        "skill_alignment"
                    ]
            },

            "timestamp":
                datetime.utcnow().isoformat() + "Z"
        }

    except HTTPException:

        raise

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# TOP-K RECOMMENDATION ENDPOINT
# ============================================================

@app.post("/recommend")
def recommend(
    request: RecommendationRequest
):

    try:

        if not RECOMMENDATION_ENGINE_AVAILABLE:

            raise HTTPException(
                status_code=503,
                detail=
                    "Recommendation engine is unavailable."
            )

        resume_text = clean_text(
            request.resume_text
        )

        recommendations = recommend_careers(
            resume_text,
            top_k=request.top_k
        )

        return {

            "success":
                True,

            "top_k":
                len(recommendations),

            "recommendations":
                recommendations,

            "timestamp":
                datetime.utcnow().isoformat() + "Z"
        }

    except HTTPException:

        raise

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# GAP ANALYSIS ENDPOINT
# ============================================================

@app.post("/gap-analysis")
def gap_analysis(
    request: GapRequest
):

    try:

        report = build_gap_report(
            request.resume_text,
            request.career
        )

        return {

            "success":
                True,

            "career":
                report[
                    "recommended_career"
                ],

            "identified_skills":
                report[
                    "identified_skills"
                ],

            "required_skills":
                report[
                    "skill_gap"
                ]["required_skills"],

            "matched_skills":
                report[
                    "skill_gap"
                ]["matched_skills"],

            "missing_skills":
                report[
                    "skill_gap"
                ]["missing_skills"],

            "skill_alignment":
                report[
                    "skill_gap"
                ]["alignment"],

            "improvement_suggestions":
                report[
                    "actionable_improvement_plan"
                ]
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# COMPLETE GAP REPORT ENDPOINT
# ============================================================

@app.post("/gap-report")
def gap_report(
    request: GapRequest
):

    try:

        report = build_gap_report(
            request.resume_text,
            request.career
        )

        return {

            "success":
                True,

            "report":
                report
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# FILE-BASED COMPLETE ANALYSIS
# ============================================================

@app.post("/analyze-file")
async def analyze_file(
    file: UploadFile = File(...)
):

    allowed_extensions = {
        ".pdf",
        ".docx",
        ".txt"
    }

    filename = file.filename or ""

    extension = Path(
        filename
    ).suffix.lower()

    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail=
                "Unsupported file format. "
                "Upload PDF, DOCX or TXT."
        )

    safe_name = (
        f"career_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        f"{extension}"
    )

    file_path = (
        UPLOAD_DIR /
        safe_name
    )

    try:

        contents = await file.read()

        with open(
            file_path,
            "wb"
        ) as output:

            output.write(
                contents
            )

        resume_text = extract_resume_file(
            file_path
        )

        resume_text = clean_text(
            resume_text
        )

        if len(resume_text) < 20:

            raise HTTPException(
                status_code=400,
                detail=
                    "Could not extract enough text "
                    "from the resume."
            )

        report = build_gap_report(
            resume_text
        )

        return {

            "success":
                True,

            "filename":
                filename,

            "report":
                report
        }

    except HTTPException:

        raise

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if file_path.exists():

            try:

                file_path.unlink()

            except Exception:

                pass


# ============================================================
# AVAILABLE CAREERS
# ============================================================

@app.get("/careers")
def available_careers():

    return {

        "count":
            len(CAREER_SKILLS),

        "careers":
            sorted(
                CAREER_SKILLS.keys()
            )
    }


# ============================================================
# CAREER SKILLS
# ============================================================

@app.get("/careers/{career}/skills")
def career_skills(
    career: str
):

    normalized = normalize_career_name(
        career
    )

    if normalized is None:

        raise HTTPException(
            status_code=404,
            detail=
                "Career not found."
        )

    return {

        "career":
            normalized,

        "required_skills":
            CAREER_SKILLS[
                normalized
            ]
    }


# ============================================================
# STARTUP MESSAGE
# ============================================================

@app.on_event("startup")
async def startup_event():

    print()
    print("=" * 70)
    print("CAREERCAST - MILESTONE 3 FASTAPI SERVICE")
    print("=" * 70)
    print("✓ FastAPI application started")
    print(
        "✓ Recommendation engine:",
        RECOMMENDATION_ENGINE_AVAILABLE
    )
    print()
    print("Available endpoints:")
    print("  GET  /")
    print("  GET  /health")
    print("  GET  /docs")
    print("  GET  /careers")
    print("  POST /predict")
    print("  POST /recommend")
    print("  POST /gap-analysis")
    print("  POST /gap-report")
    print("  POST /analyze-file")
    print("=" * 70)