
"""
CareerCast Skill Database

Skill requirements for the exact 22 career classes
used by the CareerCast Milestone 2 models.
"""

# ============================================================
# CAREER -> REQUIRED SKILLS
# ============================================================

CAREER_SKILLS = {

    "AI Researcher": [
        "python",
        "machine learning",
        "deep learning",
        "statistics",
        "linear algebra",
        "neural networks",
        "pytorch",
        "tensorflow",
        "natural language processing",
        "computer vision",
        "research"
    ],

    "Backend Developer": [
        "python",
        "java",
        "sql",
        "rest api",
        "fastapi",
        "flask",
        "django",
        "git",
        "docker",
        "testing"
    ],

    "Business Analyst": [
        "business analysis",
        "sql",
        "excel",
        "statistics",
        "data visualization",
        "power bi",
        "tableau",
        "requirements analysis",
        "communication"
    ],

    "Business Manager": [
        "business management",
        "leadership",
        "strategic planning",
        "communication",
        "financial management",
        "project management",
        "market research",
        "analytics"
    ],

    "Cybersecurity Analyst": [
        "cybersecurity",
        "network security",
        "linux",
        "firewalls",
        "cryptography",
        "siem",
        "incident response",
        "risk assessment",
        "vulnerability assessment"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "statistics",
        "excel",
        "pandas",
        "numpy",
        "data visualization",
        "power bi",
        "tableau"
    ],

    "Data Scientist": [
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
    ],

    "Deep Learning Engineer": [
        "python",
        "deep learning",
        "machine learning",
        "neural networks",
        "pytorch",
        "tensorflow",
        "numpy",
        "pandas",
        "computer vision",
        "natural language processing"
    ],

    "Digital Marketing Specialist": [
        "digital marketing",
        "seo",
        "social media marketing",
        "content marketing",
        "google analytics",
        "email marketing",
        "search engine marketing",
        "marketing analytics"
    ],

    "Ethical Hacker": [
        "ethical hacking",
        "penetration testing",
        "cybersecurity",
        "network security",
        "linux",
        "python",
        "cryptography",
        "vulnerability assessment",
        "web security"
    ],

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "typescript",
        "git",
        "responsive design",
        "web accessibility"
    ],

    "Full Stack Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "python",
        "sql",
        "rest api",
        "git",
        "docker"
    ],

    "Graphic Designer": [
        "graphic design",
        "adobe photoshop",
        "adobe illustrator",
        "figma",
        "typography",
        "color theory",
        "branding",
        "visual design",
        "creativity"
    ],

    "Machine Learning Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "numpy",
        "pandas",
        "sql",
        "docker",
        "git"
    ],

    "Marketing Executive": [
        "marketing",
        "digital marketing",
        "market research",
        "communication",
        "sales",
        "social media marketing",
        "content marketing",
        "marketing analytics"
    ],

    "Operations Manager": [
        "operations management",
        "project management",
        "supply chain",
        "process improvement",
        "leadership",
        "communication",
        "planning",
        "risk management",
        "analytics"
    ],

    "Product Designer": [
        "product design",
        "ui design",
        "ux design",
        "figma",
        "wireframing",
        "prototyping",
        "user research",
        "usability testing",
        "interaction design"
    ],

    "Project Manager": [
        "project management",
        "agile",
        "scrum",
        "risk management",
        "leadership",
        "communication",
        "planning",
        "jira",
        "stakeholder management"
    ],

    "Security Engineer": [
        "cybersecurity",
        "network security",
        "linux",
        "firewalls",
        "cryptography",
        "penetration testing",
        "security architecture",
        "incident response",
        "python"
    ],

    "Seo Analyst": [
        "seo",
        "keyword research",
        "google analytics",
        "google search console",
        "on page seo",
        "technical seo",
        "link building",
        "content optimization",
        "seo analytics"
    ],

    "Software Engineer": [
        "python",
        "java",
        "javascript",
        "data structures",
        "algorithms",
        "object oriented programming",
        "sql",
        "git",
        "testing",
        "rest api"
    ],

    "UI/UX Designer": [
        "ui design",
        "ux design",
        "figma",
        "wireframing",
        "prototyping",
        "user research",
        "usability testing",
        "interaction design",
        "visual design"
    ]
}


# ============================================================
# ACTIONABLE RECOMMENDATIONS
# ============================================================

SKILL_RECOMMENDATIONS = {

    "python": {
        "level": "Beginner → Advanced",
        "priority": "High",
        "action": (
            "Practice Python syntax, functions, OOP, "
            "data structures and real-world projects."
        )
    },

    "sql": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Practice joins, subqueries, CTEs, window "
            "functions, indexing and query optimization."
        )
    },

    "statistics": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Study probability, distributions, hypothesis "
            "testing, correlation and regression."
        )
    },

    "linear algebra": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Study vectors, matrices, matrix multiplication, "
            "eigenvalues and transformations."
        )
    },

    "machine learning": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Build classification, regression and clustering "
            "projects using real datasets."
        )
    },

    "deep learning": {
        "level": "Advanced",
        "priority": "High",
        "action": (
            "Learn neural networks, CNNs, optimization "
            "and modern deep learning architectures."
        )
    },

    "pandas": {
        "level": "Beginner → Intermediate",
        "priority": "High",
        "action": (
            "Practice data cleaning, transformation, "
            "grouping, merging and exploratory analysis."
        )
    },

    "numpy": {
        "level": "Beginner → Intermediate",
        "priority": "Medium",
        "action": (
            "Practice arrays, vectorization, broadcasting "
            "and numerical computing."
        )
    },

    "scikit-learn": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Build complete ML pipelines using preprocessing, "
            "training, evaluation and hyperparameter tuning."
        )
    },

    "tensorflow": {
        "level": "Intermediate → Advanced",
        "priority": "Medium",
        "action": (
            "Build neural networks and practice training, "
            "validation and model deployment."
        )
    },

    "pytorch": {
        "level": "Intermediate → Advanced",
        "priority": "High",
        "action": (
            "Practice tensors, datasets, neural networks, "
            "training loops and model deployment."
        )
    },

    "data visualization": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Create effective visualizations using Matplotlib, "
            "Plotly, Power BI or Tableau."
        )
    },

    "excel": {
        "level": "Beginner → Intermediate",
        "priority": "Medium",
        "action": (
            "Practice formulas, pivot tables, charts, "
            "lookup functions and data analysis."
        )
    },

    "power bi": {
        "level": "Intermediate",
        "priority": "Medium",
        "action": (
            "Build dashboards and practice DAX and data modeling."
        )
    },

    "tableau": {
        "level": "Intermediate",
        "priority": "Medium",
        "action": (
            "Build interactive dashboards and practice "
            "calculated fields and filters."
        )
    },

    "docker": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Learn Dockerfiles, images, containers, "
            "volumes, networks and Compose."
        )
    },

    "git": {
        "level": "Beginner → Intermediate",
        "priority": "High",
        "action": (
            "Practice branches, commits, merges, pull "
            "requests and conflict resolution."
        )
    },

    "fastapi": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Build REST APIs using FastAPI, Pydantic, "
            "validation and dependency injection."
        )
    },

    "rest api": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Learn HTTP methods, status codes, JSON, "
            "authentication and REST API design."
        )
    },

    "html": {
        "level": "Beginner",
        "priority": "Medium",
        "action": (
            "Practice semantic HTML, forms and accessibility."
        )
    },

    "css": {
        "level": "Beginner → Intermediate",
        "priority": "Medium",
        "action": (
            "Practice Flexbox, Grid, responsive design "
            "and modern CSS."
        )
    },

    "javascript": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Practice ES6+, asynchronous programming, "
            "DOM manipulation and API integration."
        )
    },

    "react": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Build applications using components, hooks, "
            "routing and state management."
        )
    },

    "linux": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Practice Linux commands, permissions, "
            "processes, networking and shell scripting."
        )
    },

    "network security": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Study firewalls, VPNs, IDS/IPS, secure protocols "
            "and network monitoring."
        )
    },

    "cybersecurity": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Study authentication, vulnerability management, "
            "security monitoring and incident response."
        )
    },

    "penetration testing": {
        "level": "Advanced",
        "priority": "High",
        "action": (
            "Practice authorized security testing, "
            "vulnerability discovery and reporting."
        )
    },

    "natural language processing": {
        "level": "Advanced",
        "priority": "High",
        "action": (
            "Learn text preprocessing, embeddings, "
            "transformers and modern NLP pipelines."
        )
    },

    "computer vision": {
        "level": "Advanced",
        "priority": "High",
        "action": (
            "Practice image processing, OpenCV, CNNs "
            "and image classification."
        )
    },

    "figma": {
        "level": "Beginner → Intermediate",
        "priority": "High",
        "action": (
            "Create wireframes, prototypes, design systems "
            "and responsive UI designs in Figma."
        )
    },

    "wireframing": {
        "level": "Beginner",
        "priority": "Medium",
        "action": (
            "Practice converting user requirements into "
            "structured low-fidelity interface layouts."
        )
    },

    "prototyping": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Create interactive prototypes and test "
            "user flows before implementation."
        )
    },

    "agile": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Learn Agile principles, iterative delivery "
            "and sprint-based development."
        )
    },

    "scrum": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Practice Scrum roles, ceremonies, sprint "
            "planning, reviews and retrospectives."
        )
    },

    "communication": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Develop technical communication, presentations, "
            "documentation and stakeholder communication."
        )
    },

    "leadership": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Develop team leadership, delegation, decision-making "
            "and conflict-resolution skills."
        )
    },

    "seo": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Learn keyword research, on-page optimization, "
            "technical SEO and search performance analysis."
        )
    },

    "keyword research": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Practice search-intent analysis, keyword discovery "
            "and competitive keyword research."
        )
    },

    "graphic design": {
        "level": "Intermediate",
        "priority": "High",
        "action": (
            "Create portfolio projects covering typography, "
            "composition, branding and visual communication."
        )
    },

    "adobe photoshop": {
        "level": "Intermediate",
        "priority": "Medium",
        "action": (
            "Practice image editing, retouching, compositing "
            "and professional design workflows."
        )
    },

    "adobe illustrator": {
        "level": "Intermediate",
        "priority": "Medium",
        "action": (
            "Practice vector graphics, logos, illustrations "
            "and branding assets."
        )
    }
}


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {

    "py": "python",
    "python3": "python",

    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",

    "ml": "machine learning",
    "dl": "deep learning",

    "nlp": "natural language processing",
    "cv": "computer vision",

    "js": "javascript",

    "powerbi": "power bi",
    "power-bi": "power bi",

    "nodejs": "node.js",
    "node js": "node.js",

    "k8s": "kubernetes",

    "github actions": "ci/cd",

    "ui ux": "ui/ux design",
    "ui/ux": "ui/ux design",

    "seo analyst": "seo"
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_skill(skill: str) -> str:
    """Normalize a skill name."""

    if not isinstance(skill, str):
        return ""

    skill = skill.lower().strip()

    skill = " ".join(skill.split())

    return SKILL_ALIASES.get(
        skill,
        skill
    )