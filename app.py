from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from werkzeug.utils import secure_filename

import os
import re
import traceback

from pypdf import PdfReader
from docx import Document

from career_recommendation_engine import (
    recommend_careers
)


# ============================================================
# FLASK CONFIGURATION
# ============================================================

app = Flask(__name__)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

app.config["UPLOAD_FOLDER"] = (
    UPLOAD_FOLDER
)

app.config["MAX_CONTENT_LENGTH"] = (
    10 * 1024 * 1024
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ============================================================
# ALLOWED FILE TYPES
# ============================================================

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "txt"
}


def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


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
# TEXT CLEANING
# ============================================================

def clean_text(text):

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
# PDF EXTRACTION
# ============================================================

def extract_text_from_pdf(
    file_path
):

    text = []

    reader = PdfReader(
        file_path
    )

    for page in reader.pages:

        page_text = (
            page.extract_text()
        )

        if page_text:

            text.append(
                page_text
            )

    return "\n".join(
        text
    )


# ============================================================
# DOCX EXTRACTION
# ============================================================

def extract_text_from_docx(
    file_path
):

    document = Document(
        file_path
    )

    paragraphs = []

    for paragraph in (
        document.paragraphs
    ):

        if paragraph.text.strip():

            paragraphs.append(
                paragraph.text.strip()
            )

    return "\n".join(
        paragraphs
    )


# ============================================================
# TXT EXTRACTION
# ============================================================

def extract_text_from_txt(
    file_path
):

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        return file.read()


# ============================================================
# GENERAL RESUME EXTRACTION
# ============================================================

def extract_resume_text(
    file_path
):

    extension = (
        file_path
        .rsplit(
            ".",
            1
        )[1]
        .lower()
    )

    if extension == "pdf":

        return extract_text_from_pdf(
            file_path
        )

    if extension == "docx":

        return extract_text_from_docx(
            file_path
        )

    if extension == "txt":

        return extract_text_from_txt(
            file_path
        )

    raise ValueError(
        "Unsupported file format."
    )


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(
    text
):

    text_lower = text.lower()

    detected = []

    for skill, keywords in (
        SKILL_DATABASE.items()
    ):

        for keyword in keywords:

            pattern = (
                r"(?<![a-zA-Z0-9])"
                +
                re.escape(
                    keyword.lower()
                )
                +
                r"(?![a-zA-Z0-9])"
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
            set(
                detected
            )
        )
    )


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

def calculate_skill_analysis(
    identified_skills,
    career
):

    required_skills = (
        CAREER_SKILLS.get(
            career,
            []
        )
    )

    identified_set = {
        skill.lower()
        for skill
        in identified_skills
    }

    matched = []
    missing = []

    for skill in required_skills:

        if (
            skill.lower()
            in identified_set
        ):

            matched.append(
                skill
            )

        else:

            missing.append(
                skill
            )

    if required_skills:

        alignment = (
            len(matched)
            /
            len(required_skills)
        ) * 100

    else:

        alignment = 0

    return {

        "required":
            required_skills,

        "matched":
            matched,

        "missing":
            missing,

        "alignment":
            round(
                alignment,
                2
            )

    }


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({

        "status":
            "running",

        "milestone":
            "Milestone 2",

        "recommendation_engine":
            "Random Forest + XGBoost + Sentence-BERT",

        "status_code":
            200

    })


# ============================================================
# ANALYZE RESUME
# ============================================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    try:

        resume_text = ""


        # ----------------------------------------------------
        # PASTED TEXT
        # ----------------------------------------------------

        pasted_text = (
            request.form.get(
                "resume_text",
                ""
            )
            .strip()
        )

        if pasted_text:

            resume_text = (
                pasted_text
            )


        # ----------------------------------------------------
        # UPLOADED FILE
        # ----------------------------------------------------

        uploaded_file = (
            request.files.get(
                "resume"
            )
        )

        if (
            uploaded_file
            and
            uploaded_file.filename
        ):

            filename = secure_filename(
                uploaded_file.filename
            )

            if not allowed_file(
                filename
            ):

                return jsonify({

                    "success":
                        False,

                    "error":
                        "Unsupported file format. "
                        "Please upload PDF, DOCX or TXT."

                }), 400


            file_path = os.path.join(
                UPLOAD_FOLDER,
                filename
            )

            uploaded_file.save(
                file_path
            )


            try:

                extracted_text = (
                    extract_resume_text(
                        file_path
                    )
                )

                if extracted_text.strip():

                    resume_text = (
                        extracted_text
                    )

            finally:

                if os.path.exists(
                    file_path
                ):

                    os.remove(
                        file_path
                    )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not resume_text.strip():

            return jsonify({

                "success":
                    False,

                "error":
                    "Please upload a resume or paste resume text."

            }), 400


        resume_text = clean_text(
            resume_text
        )


        # ----------------------------------------------------
        # EXTRACT SKILLS
        # ----------------------------------------------------

        identified_skills = (
            extract_skills(
                resume_text
            )
        )


        # ----------------------------------------------------
        # MILESTONE 2 PREDICTION
        # ----------------------------------------------------

        predictions = (
            recommend_careers(
                resume_text,
                top_k=5
            )
        )


        if not predictions:

            raise RuntimeError(
                "No career recommendations were generated."
            )


        # ----------------------------------------------------
        # COMPATIBILITY CONFIDENCE
        # ----------------------------------------------------

        for prediction in predictions:

            prediction["confidence"] = (
                prediction[
                    "hybrid_score"
                ]
            )


        # ----------------------------------------------------
        # TOP CAREER
        # ----------------------------------------------------

        top_career = (
            predictions[0]["career"]
        )


        # ----------------------------------------------------
        # TOP CAREER SKILL ANALYSIS
        # ----------------------------------------------------

        top_analysis = (
            calculate_skill_analysis(
                identified_skills,
                top_career
            )
        )


        # ----------------------------------------------------
        # ADD CAREER-SPECIFIC SKILL ALIGNMENT
        # ----------------------------------------------------

        for prediction in predictions:

            career_analysis = (
                calculate_skill_analysis(
                    identified_skills,
                    prediction[
                        "career"
                    ]
                )
            )

            prediction[
                "career_skill_alignment"
            ] = career_analysis[
                "alignment"
            ]


        # ----------------------------------------------------
        # FINAL RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "success":
                True,

            "message":
                "Resume analyzed successfully using the Milestone 2 hybrid recommendation engine.",

            "top_career":
                top_career,

            "top_confidence":
                predictions[0][
                    "hybrid_score"
                ],

            "predictions":
                predictions,

            "identified_skills":
                identified_skills,

            "matched_skills":
                top_analysis[
                    "matched"
                ],

            "missing_skills":
                top_analysis[
                    "missing"
                ],

            "required_skills":
                top_analysis[
                    "required"
                ],

            "skill_alignment":
                top_analysis[
                    "alignment"
                ],

            "resume_text_length":
                len(
                    resume_text
                )

        })


    except Exception as error:

        print()
        print("=" * 70)
        print("ANALYSIS ERROR")
        print("=" * 70)

        traceback.print_exc()

        return jsonify({

            "success":
                False,

            "error":
                str(error)

        }), 500


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("CAREERCAST")
    print("AI-POWERED CAREER INTELLIGENCE PLATFORM")
    print("=" * 70)

    print()
    print(
        "Milestone 2 Engine:"
    )

    print(
        "Random Forest + XGBoost + Sentence-BERT"
    )

    print()
    print(
        "Open browser at:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print("=" * 70)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )