import os
import random
import json

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

RANDOM_STATE = 42
SAMPLES_PER_CAREER = 750

random.seed(RANDOM_STATE)
np.random.seed(RANDOM_STATE)

OUTPUT_DIR = "data"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# CAREER PROFILES
#
# primary   = strong career-related skills
# secondary = related-career/common skills
# ============================================================

CAREER_PROFILES = {

    "Data Scientist": {
        "primary": [
            "python",
            "pandas",
            "numpy",
            "statistics",
            "predictive modeling"
        ],
        "secondary": [
            "sql",
            "data analysis",
            "machine learning",
            "scikit learn",
            "data visualization",
            "power bi",
            "tableau"
        ],
        "interests": [
            "data science",
            "analytics",
            "machine learning",
            "artificial intelligence",
            "business intelligence"
        ],
        "projects": [
            "data analysis project",
            "prediction project",
            "analytics dashboard",
            "machine learning project"
        ],
        "education": [
            "btech cse",
            "btech it",
            "bsc computer science",
            "msc data science",
            "mba"
        ],
        "certifications": [
            "python",
            "data analytics",
            "machine learning",
            "data science"
        ]
    },

    "Data Analyst": {
        "primary": [
            "sql",
            "excel",
            "data analysis",
            "power bi",
            "tableau"
        ],
        "secondary": [
            "python",
            "pandas",
            "statistics",
            "data visualization",
            "business intelligence",
            "machine learning"
        ],
        "interests": [
            "data analytics",
            "business intelligence",
            "analytics",
            "reporting",
            "data visualization"
        ],
        "projects": [
            "sales analysis",
            "business dashboard",
            "data analysis project",
            "analytics dashboard"
        ],
        "education": [
            "bcom",
            "bba",
            "bsc statistics",
            "bsc computer science",
            "btech cse"
        ],
        "certifications": [
            "sql",
            "power bi",
            "tableau",
            "data analytics"
        ]
    },

    "Machine Learning Engineer": {
        "primary": [
            "python",
            "machine learning",
            "scikit learn",
            "model deployment",
            "mlops"
        ],
        "secondary": [
            "tensorflow",
            "pytorch",
            "numpy",
            "pandas",
            "deep learning",
            "sql",
            "data analysis"
        ],
        "interests": [
            "machine learning",
            "artificial intelligence",
            "deep learning",
            "mlops",
            "analytics"
        ],
        "projects": [
            "machine learning project",
            "prediction system",
            "recommendation system",
            "model deployment"
        ],
        "education": [
            "btech cse",
            "btech it",
            "msc computer science",
            "msc artificial intelligence",
            "bsc computer science"
        ],
        "certifications": [
            "machine learning",
            "python",
            "tensorflow",
            "cloud computing"
        ]
    },

    "Deep Learning Engineer": {
        "primary": [
            "deep learning",
            "neural networks",
            "tensorflow",
            "pytorch",
            "computer vision"
        ],
        "secondary": [
            "python",
            "machine learning",
            "numpy",
            "scikit learn",
            "natural language processing",
            "data analysis"
        ],
        "interests": [
            "deep learning",
            "machine learning",
            "artificial intelligence",
            "computer vision",
            "neural networks"
        ],
        "projects": [
            "deep learning project",
            "image classification",
            "computer vision project",
            "prediction system"
        ],
        "education": [
            "btech cse",
            "msc artificial intelligence",
            "msc computer science",
            "btech it"
        ],
        "certifications": [
            "deep learning",
            "tensorflow",
            "pytorch",
            "machine learning"
        ]
    },

    "AI Researcher": {
        "primary": [
            "artificial intelligence",
            "research methodology",
            "machine learning research",
            "neural networks",
            "natural language processing"
        ],
        "secondary": [
            "python",
            "machine learning",
            "deep learning",
            "pytorch",
            "tensorflow",
            "computer vision"
        ],
        "interests": [
            "artificial intelligence",
            "ai research",
            "machine learning",
            "deep learning",
            "research"
        ],
        "projects": [
            "ai research project",
            "machine learning research",
            "nlp research",
            "research project"
        ],
        "education": [
            "msc artificial intelligence",
            "msc computer science",
            "mtech computer science",
            "btech cse"
        ],
        "certifications": [
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "python"
        ]
    },

    "Backend Developer": {
        "primary": [
            "python",
            "java",
            "backend development",
            "rest api",
            "database"
        ],
        "secondary": [
            "django",
            "flask",
            "spring boot",
            "node js",
            "mysql",
            "postgresql",
            "mongodb",
            "javascript"
        ],
        "interests": [
            "backend development",
            "software development",
            "web development",
            "api development"
        ],
        "projects": [
            "backend application",
            "rest api",
            "web application",
            "database application"
        ],
        "education": [
            "btech cse",
            "btech it",
            "bca",
            "bsc computer science"
        ],
        "certifications": [
            "python",
            "java",
            "backend development",
            "cloud computing"
        ]
    },

    "Frontend Developer": {
        "primary": [
            "html",
            "css",
            "javascript",
            "react",
            "frontend development"
        ],
        "secondary": [
            "typescript",
            "angular",
            "bootstrap",
            "responsive design",
            "web development",
            "ui design",
            "figma"
        ],
        "interests": [
            "frontend development",
            "web development",
            "web design",
            "user interfaces"
        ],
        "projects": [
            "responsive website",
            "web interface",
            "react application",
            "portfolio website"
        ],
        "education": [
            "btech cse",
            "btech it",
            "bca",
            "bsc computer science"
        ],
        "certifications": [
            "javascript",
            "react",
            "web development",
            "frontend development"
        ]
    },

    "Full Stack Developer": {
        "primary": [
            "javascript",
            "react",
            "node js",
            "full stack development",
            "rest api"
        ],
        "secondary": [
            "html",
            "css",
            "mongodb",
            "mysql",
            "express",
            "python",
            "web development",
            "frontend development"
        ],
        "interests": [
            "full stack development",
            "web development",
            "software development",
            "application development"
        ],
        "projects": [
            "full stack web application",
            "ecommerce application",
            "web platform",
            "web application"
        ],
        "education": [
            "btech cse",
            "btech it",
            "bca",
            "msc computer science"
        ],
        "certifications": [
            "full stack development",
            "javascript",
            "web development",
            "cloud computing"
        ]
    },

    "Software Engineer": {
        "primary": [
            "java",
            "python",
            "software engineering",
            "data structures",
            "algorithms"
        ],
        "secondary": [
            "c++",
            "object oriented programming",
            "git",
            "unit testing",
            "javascript",
            "database",
            "rest api"
        ],
        "interests": [
            "software development",
            "programming",
            "application development",
            "technology"
        ],
        "projects": [
            "software application",
            "enterprise application",
            "software project",
            "web application"
        ],
        "education": [
            "btech cse",
            "btech it",
            "bca",
            "bsc computer science"
        ],
        "certifications": [
            "java",
            "python",
            "software engineering",
            "cloud computing"
        ]
    },

    "Cybersecurity Analyst": {
        "primary": [
            "cybersecurity",
            "threat detection",
            "incident response",
            "siem",
            "network security"
        ],
        "secondary": [
            "splunk",
            "firewall",
            "linux",
            "vulnerability assessment",
            "penetration testing",
            "cloud security"
        ],
        "interests": [
            "cybersecurity",
            "network security",
            "threat analysis",
            "information security"
        ],
        "projects": [
            "security monitoring",
            "threat detection system",
            "security audit",
            "network security project"
        ],
        "education": [
            "btech cse",
            "btech it",
            "bsc cybersecurity",
            "msc cybersecurity"
        ],
        "certifications": [
            "cybersecurity",
            "security plus",
            "network security",
            "ethical hacking"
        ]
    },

    "Ethical Hacker": {
        "primary": [
            "ethical hacking",
            "penetration testing",
            "kali linux",
            "burp suite",
            "metasploit"
        ],
        "secondary": [
            "network security",
            "cybersecurity",
            "vulnerability assessment",
            "web security",
            "linux",
            "firewall"
        ],
        "interests": [
            "ethical hacking",
            "penetration testing",
            "cybersecurity",
            "web security"
        ],
        "projects": [
            "penetration testing",
            "security testing",
            "web security audit",
            "vulnerability assessment"
        ],
        "education": [
            "btech cse",
            "btech it",
            "bsc cybersecurity",
            "msc cybersecurity"
        ],
        "certifications": [
            "ceh",
            "ethical hacking",
            "penetration testing",
            "security plus"
        ]
    },

    "Security Engineer": {
        "primary": [
            "network security",
            "firewall",
            "cloud security",
            "iam",
            "security architecture"
        ],
        "secondary": [
            "cybersecurity",
            "linux",
            "siem",
            "encryption",
            "identity management",
            "vulnerability assessment"
        ],
        "interests": [
            "cloud security",
            "network security",
            "information security",
            "security engineering"
        ],
        "projects": [
            "cloud security project",
            "security infrastructure",
            "identity management",
            "network security project"
        ],
        "education": [
            "btech cse",
            "btech it",
            "msc cybersecurity",
            "bsc cybersecurity"
        ],
        "certifications": [
            "security plus",
            "aws security",
            "azure security",
            "cybersecurity"
        ]
    },

    "Business Analyst": {
        "primary": [
            "business analysis",
            "requirements analysis",
            "sql",
            "business intelligence",
            "process improvement"
        ],
        "secondary": [
            "excel",
            "power bi",
            "tableau",
            "data analysis",
            "jira",
            "project management"
        ],
        "interests": [
            "business analysis",
            "business intelligence",
            "process improvement",
            "analytics"
        ],
        "projects": [
            "business analysis project",
            "requirements gathering",
            "business dashboard",
            "process improvement"
        ],
        "education": [
            "bba",
            "bcom",
            "mba",
            "btech"
        ],
        "certifications": [
            "business analysis",
            "power bi",
            "project management",
            "data analytics"
        ]
    },

    "Business Manager": {
        "primary": [
            "business management",
            "business strategy",
            "sales management",
            "financial analysis",
            "crm"
        ],
        "secondary": [
            "excel",
            "business analytics",
            "marketing",
            "project management",
            "leadership"
        ],
        "interests": [
            "business management",
            "leadership",
            "business strategy",
            "sales"
        ],
        "projects": [
            "business strategy",
            "business development",
            "sales project",
            "market expansion"
        ],
        "education": [
            "mba",
            "bba",
            "bcom",
            "business administration"
        ],
        "certifications": [
            "business management",
            "leadership",
            "project management",
            "sales"
        ]
    },

    "Project Manager": {
        "primary": [
            "project management",
            "agile",
            "scrum",
            "project planning",
            "risk management"
        ],
        "secondary": [
            "jira",
            "ms project",
            "leadership",
            "team management",
            "business analysis",
            "operations management"
        ],
        "interests": [
            "project management",
            "leadership",
            "team management",
            "agile management"
        ],
        "projects": [
            "project planning",
            "agile project",
            "project delivery",
            "team management"
        ],
        "education": [
            "mba",
            "bba",
            "btech",
            "business administration"
        ],
        "certifications": [
            "pmp",
            "scrum master",
            "agile",
            "project management"
        ]
    },

    "Operations Manager": {
        "primary": [
            "operations management",
            "supply chain",
            "inventory management",
            "process optimization",
            "logistics"
        ],
        "secondary": [
            "excel",
            "quality management",
            "project management",
            "business analytics",
            "process improvement"
        ],
        "interests": [
            "operations",
            "supply chain",
            "process improvement",
            "logistics"
        ],
        "projects": [
            "process optimization",
            "supply chain project",
            "inventory management",
            "operations improvement"
        ],
        "education": [
            "mba",
            "bba",
            "bcom",
            "industrial engineering"
        ],
        "certifications": [
            "operations management",
            "supply chain",
            "six sigma",
            "project management"
        ]
    },

    "Marketing Executive": {
        "primary": [
            "marketing",
            "sales",
            "market research",
            "crm",
            "brand management"
        ],
        "secondary": [
            "social media marketing",
            "content marketing",
            "google analytics",
            "digital marketing",
            "business development"
        ],
        "interests": [
            "marketing",
            "sales",
            "advertising",
            "brand management"
        ],
        "projects": [
            "marketing campaign",
            "market research",
            "brand campaign",
            "sales campaign"
        ],
        "education": [
            "mba marketing",
            "bba",
            "bcom",
            "mass communication"
        ],
        "certifications": [
            "marketing",
            "digital marketing",
            "google analytics",
            "sales"
        ]
    },

    "Digital Marketing Specialist": {
        "primary": [
            "digital marketing",
            "google ads",
            "facebook ads",
            "social media marketing",
            "email marketing"
        ],
        "secondary": [
            "seo",
            "google analytics",
            "content marketing",
            "marketing",
            "market research"
        ],
        "interests": [
            "digital marketing",
            "social media",
            "online advertising",
            "content marketing"
        ],
        "projects": [
            "digital marketing campaign",
            "social media campaign",
            "google ads campaign",
            "content strategy"
        ],
        "education": [
            "mba marketing",
            "bba",
            "mass communication",
            "bcom"
        ],
        "certifications": [
            "google ads",
            "google analytics",
            "digital marketing",
            "hubspot"
        ]
    },

    "Seo Analyst": {
        "primary": [
            "seo",
            "keyword research",
            "google search console",
            "on page seo",
            "technical seo"
        ],
        "secondary": [
            "google analytics",
            "content optimization",
            "digital marketing",
            "content marketing",
            "social media marketing"
        ],
        "interests": [
            "seo",
            "search marketing",
            "content optimization",
            "digital marketing"
        ],
        "projects": [
            "seo audit",
            "keyword research",
            "website optimization",
            "search engine optimization"
        ],
        "education": [
            "bba",
            "mba marketing",
            "mass communication",
            "bcom"
        ],
        "certifications": [
            "seo",
            "google analytics",
            "digital marketing",
            "content marketing"
        ]
    },

    "Graphic Designer": {
        "primary": [
            "photoshop",
            "illustrator",
            "graphic design",
            "typography",
            "branding"
        ],
        "secondary": [
            "figma",
            "adobe xd",
            "visual design",
            "illustration",
            "ui design",
            "ux design"
        ],
        "interests": [
            "graphic design",
            "visual design",
            "branding",
            "illustration"
        ],
        "projects": [
            "brand identity",
            "poster design",
            "logo design",
            "visual campaign"
        ],
        "education": [
            "bdes",
            "bfa",
            "graphic design",
            "visual communication"
        ],
        "certifications": [
            "graphic design",
            "adobe photoshop",
            "adobe illustrator",
            "ui ux design"
        ]
    },

    "UI/UX Designer": {
        "primary": [
            "figma",
            "wireframing",
            "prototyping",
            "user research",
            "usability testing"
        ],
        "secondary": [
            "adobe xd",
            "sketch",
            "ui design",
            "ux design",
            "graphic design",
            "design systems"
        ],
        "interests": [
            "ui design",
            "ux design",
            "user experience",
            "product design"
        ],
        "projects": [
            "mobile app prototype",
            "website redesign",
            "user research",
            "ux case study"
        ],
        "education": [
            "bdes",
            "bfa",
            "design",
            "visual communication"
        ],
        "certifications": [
            "ui ux design",
            "figma",
            "ux design",
            "product design"
        ]
    },

    "Product Designer": {
        "primary": [
            "product design",
            "design systems",
            "user research",
            "ux design",
            "prototyping"
        ],
        "secondary": [
            "figma",
            "wireframing",
            "usability testing",
            "ui design",
            "graphic design",
            "product development"
        ],
        "interests": [
            "product design",
            "ux design",
            "user experience",
            "design thinking"
        ],
        "projects": [
            "product redesign",
            "mobile product",
            "design system",
            "product prototype"
        ],
        "education": [
            "bdes",
            "design",
            "bfa",
            "visual communication"
        ],
        "certifications": [
            "product design",
            "ux design",
            "figma",
            "design thinking"
        ]
    }
}


# ============================================================
# COMMON VOCABULARY
# ============================================================

COMMON_SKILLS = [
    "communication",
    "teamwork",
    "problem solving",
    "leadership",
    "time management",
    "critical thinking",
    "creativity",
    "adaptability",
    "microsoft office",
    "presentation",
    "research",
    "project work",
    "documentation",
    "team collaboration"
]

LOCATIONS = [
    "Hyderabad",
    "Bangalore",
    "Chennai",
    "Pune",
    "Mumbai",
    "Delhi",
    "Kolkata",
    "Coimbatore",
    "Visakhapatnam",
    "Vijayawada"
]

GENDERS = [
    "male",
    "female"
]

LANGUAGES = [
    "english",
    "hindi",
    "telugu",
    "tamil",
    "kannada",
    "marathi"
]

WORK_STYLES = [
    "remote",
    "hybrid",
    "office"
]

WORK_TYPES = [
    "full time",
    "part time",
    "internship"
]

RELOCATION = [
    "yes",
    "no"
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def choose_items(items, minimum, maximum):

    maximum = min(
        maximum,
        len(items)
    )

    minimum = min(
        minimum,
        maximum
    )

    count = random.randint(
        minimum,
        maximum
    )

    return random.sample(
        items,
        count
    )


def comma_join(items):

    return ", ".join(items)


# ============================================================
# GENERATE PROFILE
# ============================================================

def generate_profile(career, profile):

    # --------------------------------------------------------
    # Primary skills
    #
    # We keep some strong career information.
    # --------------------------------------------------------

    primary = choose_items(
        profile["primary"],
        2,
        min(4, len(profile["primary"]))
    )

    # --------------------------------------------------------
    # Secondary skills
    #
    # These create overlap with related careers.
    # --------------------------------------------------------

    secondary = choose_items(
        profile["secondary"],
        2,
        min(4, len(profile["secondary"]))
    )

    # --------------------------------------------------------
    # Common skills
    # --------------------------------------------------------

    common = choose_items(
        COMMON_SKILLS,
        2,
        4
    )

    # --------------------------------------------------------
    # Randomly introduce additional skills
    #
    # This prevents the model from learning a rigid template.
    # --------------------------------------------------------

    technical_skills = (
        primary +
        secondary
    )

    # 20% chance of adding one unrelated/general technical skill
    if random.random() < 0.20:

        technical_skills.append(
            random.choice([
                "git",
                "database",
                "cloud computing",
                "python",
                "excel",
                "javascript",
                "sql"
            ])
        )

    technical_skills = list(
        dict.fromkeys(
            technical_skills
        )
    )

    # --------------------------------------------------------
    # Interests
    # --------------------------------------------------------

    interests = choose_items(
        profile["interests"],
        1,
        min(3, len(profile["interests"]))
    )

    # Add overlap to interests
    if random.random() < 0.30:

        interests.append(
            random.choice([
                "technology",
                "analytics",
                "business",
                "innovation",
                "design",
                "problem solving"
            ])
        )

    interests = list(
        dict.fromkeys(
            interests
        )
    )

    # --------------------------------------------------------
    # Certifications
    # --------------------------------------------------------

    certifications = choose_items(
        profile["certifications"],
        1,
        min(2, len(profile["certifications"]))
    )

    # --------------------------------------------------------
    # Project
    # --------------------------------------------------------

    projects = choose_items(
        profile["projects"],
        1,
        min(2, len(profile["projects"]))
    )

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    education = random.choice(
        profile["education"]
    )

    # --------------------------------------------------------
    # Soft skills
    # --------------------------------------------------------

    soft_skills = choose_items(
        COMMON_SKILLS,
        2,
        4
    )

    # --------------------------------------------------------
    # Other profile attributes
    # --------------------------------------------------------

    age = random.randint(
        20,
        35
    )

    location = random.choice(
        LOCATIONS
    )

    gender = random.choice(
        GENDERS
    )

    languages = choose_items(
        LANGUAGES,
        1,
        3
    )

    work_style = random.choice(
        WORK_STYLES
    )

    work_type = random.choice(
        WORK_TYPES
    )

    relocation = random.choice(
        RELOCATION
    )

    experience = random.choice([
        "fresher",
        "internship experience",
        "academic project",
        "one year experience",
        "two years experience",
        "project experience"
    ])

    achievements = random.choice([
        "completed academic project",
        "completed internship",
        "won college competition",
        "received academic award",
        "completed professional project",
        "participated in technical competition"
    ])

    # --------------------------------------------------------
    # Structured row
    # --------------------------------------------------------

    row = {

        "Age":
            age,

        "Gender":
            gender,

        "Location":
            location,

        "Highest_qualification":
            education,

        "Technical_Skills":
            comma_join(
                technical_skills
            ),

        "Soft_Skills":
            comma_join(
                soft_skills
            ),

        "Languages_Known":
            comma_join(
                languages
            ),

        "Certifications":
            comma_join(
                certifications
            ),

        "Fields_of_Interest":
            comma_join(
                interests
            ),

        "Preferred_Work_Style":
            work_style,

        "Work_Type_Interest":
            work_type,

        "Past_Jobs_Internships":
            experience,

        "Achievements":
            achievements,

        "Skills_Gained":
            comma_join(
                technical_skills
            ),

        "Willing_to_Relocate":
            relocation,

        "Suggested_Career_Path":
            career
    }

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # Career name is NOT included in ML_Text.
    # --------------------------------------------------------

    text_parts = [

        f"qualification {education}",

        f"technical skills "
        f"{comma_join(technical_skills)}",

        f"soft skills "
        f"{comma_join(soft_skills)}",

        f"languages "
        f"{comma_join(languages)}",

        f"certifications "
        f"{comma_join(certifications)}",

        f"interests "
        f"{comma_join(interests)}",

        f"work style "
        f"{work_style}",

        f"work type "
        f"{work_type}",

        f"experience "
        f"{experience}",

        f"achievements "
        f"{achievements}",

        f"skills gained "
        f"{comma_join(technical_skills)}"
    ]

    row["ML_Text"] = " ".join(
        text_parts
    )

    return row


# ============================================================
# GENERATE COMPLETE DATASET
# ============================================================

def generate_dataset():

    rows = []

    print("=" * 70)
    print("CAREERCAST DATASET V2")
    print("=" * 70)

    print(
        f"\nNumber of careers: "
        f"{len(CAREER_PROFILES)}"
    )

    print(
        f"Samples per career: "
        f"{SAMPLES_PER_CAREER}"
    )

    print(
        f"Expected total samples: "
        f"{len(CAREER_PROFILES) * SAMPLES_PER_CAREER}"
    )

    print("\nGenerating profiles...\n")

    for career, profile in CAREER_PROFILES.items():

        print(
            f"Generating: {career}"
        )

        for _ in range(
            SAMPLES_PER_CAREER
        ):

            rows.append(
                generate_profile(
                    career,
                    profile
                )
            )

    # Shuffle
    random.shuffle(
        rows
    )

    df = pd.DataFrame(
        rows
    )

    return df


# ============================================================
# CLEAN DATASET
# ============================================================

def clean_dataset(df):

    print("\n" + "=" * 70)
    print("DATASET CLEANING")
    print("=" * 70)

    original_count = len(df)

    # Remove exact duplicate ML text + label combinations
    df = df.drop_duplicates(
        subset=[
            "ML_Text",
            "Suggested_Career_Path"
        ]
    ).reset_index(
        drop=True
    )

    print(
        f"\nDuplicates removed: "
        f"{original_count - len(df)}"
    )

    # Remove missing text
    df["ML_Text"] = (
        df["ML_Text"]
        .fillna("")
        .astype(str)
        .str.replace(
            r"\s+",
            " ",
            regex=True
        )
        .str.strip()
    )

    df = df[
        df["ML_Text"].str.len() > 0
    ]

    # Remove missing labels
    df["Suggested_Career_Path"] = (
        df["Suggested_Career_Path"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df = df[
        df["Suggested_Career_Path"].str.len() > 0
    ]

    return df.reset_index(
        drop=True
    )


# ============================================================
# STRATIFIED SPLIT
# ============================================================

def split_dataset(df):

    print("\n" + "=" * 70)
    print("CREATING TRAIN / VALIDATION / TEST SPLITS")
    print("=" * 70)

    train_parts = []
    validation_parts = []
    test_parts = []

    for career, group in df.groupby(
        "Suggested_Career_Path"
    ):

        group = group.sample(
            frac=1,
            random_state=RANDOM_STATE
        ).reset_index(
            drop=True
        )

        n = len(group)

        train_end = int(
            n * 0.70
        )

        validation_end = int(
            n * 0.85
        )

        train_parts.append(
            group.iloc[:train_end]
        )

        validation_parts.append(
            group.iloc[
                train_end:validation_end
            ]
        )

        test_parts.append(
            group.iloc[
                validation_end:
            ]
        )

    train_df = pd.concat(
        train_parts,
        ignore_index=True
    )

    validation_df = pd.concat(
        validation_parts,
        ignore_index=True
    )

    test_df = pd.concat(
        test_parts,
        ignore_index=True
    )

    # Shuffle independently
    train_df = train_df.sample(
        frac=1,
        random_state=RANDOM_STATE
    ).reset_index(
        drop=True
    )

    validation_df = validation_df.sample(
        frac=1,
        random_state=RANDOM_STATE
    ).reset_index(
        drop=True
    )

    test_df = test_df.sample(
        frac=1,
        random_state=RANDOM_STATE
    ).reset_index(
        drop=True
    )

    return (
        train_df,
        validation_df,
        test_df
    )


# ============================================================
# DATASET REPORT
# ============================================================

def create_report(
    df,
    train_df,
    validation_df,
    test_df
):

    report = {

        "dataset_version":
            "V2",

        "random_state":
            RANDOM_STATE,

        "total_records":
            len(df),

        "number_of_careers":
            int(
                df[
                    "Suggested_Career_Path"
                ].nunique()
            ),

        "train_records":
            len(train_df),

        "validation_records":
            len(validation_df),

        "test_records":
            len(test_df),

        "career_distribution":
            df[
                "Suggested_Career_Path"
            ]
            .value_counts()
            .sort_index()
            .to_dict()
    }

    report_file = os.path.join(
        OUTPUT_DIR,
        "dataset_report_v2.json"
    )

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )

    print(
        f"\nReport saved: "
        f"{report_file}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    # Generate
    df = generate_dataset()

    # Clean
    df = clean_dataset(
        df
    )

    # Split
    (
        train_df,
        validation_df,
        test_df
    ) = split_dataset(
        df
    )

    # Save complete dataset
    df.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "career_dataset_cleaned.csv"
        ),
        index=False
    )

    # Save train
    train_df.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "train.csv"
        ),
        index=False
    )

    # Save validation
    validation_df.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "validation.csv"
        ),
        index=False
    )

    # Save test
    test_df.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "test.csv"
        ),
        index=False
    )

    # Report
    create_report(
        df,
        train_df,
        validation_df,
        test_df
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("DATASET V2 GENERATION COMPLETE")
    print("=" * 70)

    print(
        f"\nComplete dataset : "
        f"{df.shape}"
    )

    print(
        f"Training dataset : "
        f"{train_df.shape}"
    )

    print(
        f"Validation dataset : "
        f"{validation_df.shape}"
    )

    print(
        f"Test dataset : "
        f"{test_df.shape}"
    )

    print("\nCareer distribution:")

    print(
        df[
            "Suggested_Career_Path"
        ]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print("\nCreated/updated files:")

    print(
        "✓ data/career_dataset_cleaned.csv"
    )

    print(
        "✓ data/train.csv"
    )

    print(
        "✓ data/validation.csv"
    )

    print(
        "✓ data/test.csv"
    )

    print(
        "✓ data/dataset_report_v2.json"
    )

    print("\nDataset V2 ready.")


if __name__ == "__main__":
    main()