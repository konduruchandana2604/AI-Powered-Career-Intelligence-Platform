import os
import pickle
import json
import time
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ==============================================================
# MILESTONE 2 - STEP 3
# SENTENCE-BERT SKILL EMBEDDINGS
# ==============================================================

print("=" * 70)
print("MILESTONE 2 - STEP 3")
print("SENTENCE-BERT SKILL EMBEDDINGS")
print("=" * 70)


# ==============================================================
# CONFIGURATION
# ==============================================================

TRAIN_FILE = "data/train.csv"
VALIDATION_FILE = "data/validation.csv"
TEST_FILE = "data/test.csv"

MODEL_NAME = "all-MiniLM-L6-v2"

OUTPUT_DIR = "models"

CAREER_EMBEDDINGS_FILE = os.path.join(
    OUTPUT_DIR,
    "sentence_bert_career_embeddings.pkl"
)

CAREER_NAMES_FILE = os.path.join(
    OUTPUT_DIR,
    "sentence_bert_career_names.pkl"
)

MODEL_INFO_FILE = os.path.join(
    OUTPUT_DIR,
    "sentence_bert_model_info.json"
)

TRAIN_EMBEDDINGS_FILE = os.path.join(
    OUTPUT_DIR,
    "sentence_bert_train_embeddings.pkl"
)

VALIDATION_EMBEDDINGS_FILE = os.path.join(
    OUTPUT_DIR,
    "sentence_bert_validation_embeddings.pkl"
)

TEST_EMBEDDINGS_FILE = os.path.join(
    OUTPUT_DIR,
    "sentence_bert_test_embeddings.pkl"
)


os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==============================================================
# START TIMER
# ==============================================================

start_time = time.time()


# ==============================================================
# STEP 1 - CHECK DATASET FILES
# ==============================================================

print()
print("=" * 70)
print("CHECKING DATASET FILES")
print("=" * 70)

for file_path in [
    TRAIN_FILE,
    VALIDATION_FILE,
    TEST_FILE
]:
    if os.path.exists(file_path):
        print(f"✓ {file_path}")
    else:
        raise FileNotFoundError(
            f"Required dataset file not found: {file_path}"
        )


# ==============================================================
# STEP 2 - LOAD DATASETS
# ==============================================================

print()
print("=" * 70)
print("LOADING DATASETS")
print("=" * 70)

train_df = pd.read_csv(TRAIN_FILE)
validation_df = pd.read_csv(VALIDATION_FILE)
test_df = pd.read_csv(TEST_FILE)

print(f"Training shape   : {train_df.shape}")
print(f"Validation shape : {validation_df.shape}")
print(f"Test shape       : {test_df.shape}")


# ==============================================================
# STEP 3 - CHECK REQUIRED COLUMNS
# ==============================================================

print()
print("=" * 70)
print("CHECKING REQUIRED COLUMNS")
print("=" * 70)

required_columns = [
    "ML_Text",
    "Suggested_Career_Path"
]

for column in required_columns:

    for name, df in [
        ("Training", train_df),
        ("Validation", validation_df),
        ("Test", test_df)
    ]:

        if column not in df.columns:
            raise ValueError(
                f"Missing column '{column}' in {name} dataset"
            )

    print(f"✓ {column}")


# ==============================================================
# STEP 4 - CLEAN TEXT
# ==============================================================

print()
print("=" * 70)
print("PREPARING TEXT DATA")
print("=" * 70)


def clean_text(value):
    """
    Convert values to clean strings.
    """

    if pd.isna(value):
        return ""

    return str(value).strip()


train_texts = train_df["ML_Text"].apply(clean_text).tolist()
validation_texts = validation_df["ML_Text"].apply(clean_text).tolist()
test_texts = test_df["ML_Text"].apply(clean_text).tolist()


print(f"Training records   : {len(train_texts)}")
print(f"Validation records : {len(validation_texts)}")
print(f"Test records       : {len(test_texts)}")


# ==============================================================
# STEP 5 - LOAD SENTENCE-BERT
# ==============================================================

print()
print("=" * 70)
print("LOADING SENTENCE-BERT MODEL")
print("=" * 70)

print(f"Model: {MODEL_NAME}")
print()
print("First execution may download the model.")
print("Please wait if downloading occurs.")


model = SentenceTransformer(MODEL_NAME)

print()
print("✓ Sentence-BERT model loaded successfully")


# ==============================================================
# STEP 6 - MODEL INFORMATION
# ==============================================================

print()
print("=" * 70)
print("MODEL INFORMATION")
print("=" * 70)

embedding_dimension = model.get_sentence_embedding_dimension()

print(f"Model name          : {MODEL_NAME}")
print(f"Embedding dimension : {embedding_dimension}")


if embedding_dimension != 384:
    print(
        f"WARNING: Expected 384 dimensions, "
        f"but received {embedding_dimension}"
    )
else:
    print("✓ 384-dimensional embeddings confirmed")


# ==============================================================
# STEP 7 - GENERATE TEXT EMBEDDINGS
# ==============================================================

print()
print("=" * 70)
print("GENERATING TRAINING EMBEDDINGS")
print("=" * 70)

print("Encoding training text...")

train_embeddings = model.encode(
    train_texts,
    batch_size=32,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

print()
print(f"Training embeddings shape: {train_embeddings.shape}")


# ==============================================================
# VALIDATION EMBEDDINGS
# ==============================================================

print()
print("=" * 70)
print("GENERATING VALIDATION EMBEDDINGS")
print("=" * 70)

print("Encoding validation text...")

validation_embeddings = model.encode(
    validation_texts,
    batch_size=32,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

print()
print(
    f"Validation embeddings shape: "
    f"{validation_embeddings.shape}"
)


# ==============================================================
# TEST EMBEDDINGS
# ==============================================================

print()
print("=" * 70)
print("GENERATING TEST EMBEDDINGS")
print("=" * 70)

print("Encoding test text...")

test_embeddings = model.encode(
    test_texts,
    batch_size=32,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

print()
print(
    f"Test embeddings shape: "
    f"{test_embeddings.shape}"
)


# ==============================================================
# STEP 8 - EXTRACT CAREER NAMES
# ==============================================================

print()
print("=" * 70)
print("EXTRACTING CAREER CLASSES")
print("=" * 70)

career_names = sorted(
    train_df["Suggested_Career_Path"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
    .tolist()
)

print(f"Number of career classes: {len(career_names)}")

for index, career in enumerate(career_names):
    print(f"{index:02d} -> {career}")


# ==============================================================
# STEP 9 - CREATE CAREER PROFILES
# ==============================================================

print()
print("=" * 70)
print("CREATING CAREER PROFILES")
print("=" * 70)


career_profiles = {

    "AI Researcher":
        "AI research artificial intelligence machine learning "
        "deep learning neural networks research algorithms",

    "Backend Developer":
        "backend development server side programming APIs databases "
        "Python Java Node.js REST services SQL",

    "Business Analyst":
        "business analysis requirements gathering data analysis "
        "business intelligence reporting stakeholder management",

    "Business Manager":
        "business management leadership strategy operations "
        "business planning team management",

    "Cybersecurity Analyst":
        "cybersecurity security analysis threat detection "
        "network security vulnerability assessment incident response",

    "Data Analyst":
        "data analysis statistics SQL Python Excel visualization "
        "Power BI Tableau reporting",

    "Data Scientist":
        "data science machine learning statistics Python SQL "
        "data analysis predictive modeling visualization",

    "Deep Learning Engineer":
        "deep learning neural networks artificial intelligence "
        "PyTorch TensorFlow computer vision NLP",

    "Digital Marketing Specialist":
        "digital marketing social media advertising SEO "
        "content marketing analytics campaigns",

    "Ethical Hacker":
        "ethical hacking penetration testing cybersecurity "
        "network security vulnerability assessment Kali Linux",

    "Frontend Developer":
        "frontend web development HTML CSS JavaScript React "
        "user interfaces responsive design",

    "Full Stack Developer":
        "full stack web development frontend backend JavaScript "
        "React Node.js databases APIs",

    "Graphic Designer":
        "graphic design visual design Photoshop Illustrator "
        "branding typography creative design",

    "Machine Learning Engineer":
        "machine learning artificial intelligence Python "
        "scikit-learn TensorFlow model development deployment",

    "Marketing Executive":
        "marketing campaigns sales promotion customer engagement "
        "market research advertising",

    "Operations Manager":
        "operations management process optimization logistics "
        "planning team management business operations",

    "Product Designer":
        "product design user research prototyping interaction design "
        "product development",

    "Project Manager":
        "project management planning scheduling Agile Scrum "
        "leadership risk management",

    "Security Engineer":
        "security engineering cybersecurity network security "
        "cloud security systems security",

    "Seo Analyst":
        "SEO search engine optimization keyword research "
        "Google Analytics content optimization",

    "Software Engineer":
        "software engineering programming software development "
        "algorithms databases testing",

    "UI/UX Designer":
        "UI UX design user experience user interface "
        "wireframes prototyping usability Figma"
}


# Check profiles

missing_profiles = [
    career
    for career in career_names
    if career not in career_profiles
]

if missing_profiles:

    raise ValueError(
        "Missing career profiles for: "
        + ", ".join(missing_profiles)
    )


print()
print("✓ Career profiles created")
print(f"✓ Profiles available: {len(career_profiles)}")


# ==============================================================
# STEP 10 - GENERATE CAREER EMBEDDINGS
# ==============================================================

print()
print("=" * 70)
print("GENERATING CAREER EMBEDDINGS")
print("=" * 70)

career_profile_texts = [
    career_profiles[career]
    for career in career_names
]

career_embeddings = model.encode(
    career_profile_texts,
    convert_to_numpy=True,
    normalize_embeddings=True,
    show_progress_bar=True
)

print()
print(
    f"Career embeddings shape: "
    f"{career_embeddings.shape}"
)


# ==============================================================
# STEP 11 - VERIFY EMBEDDINGS
# ==============================================================

print()
print("=" * 70)
print("VERIFYING EMBEDDINGS")
print("=" * 70)


def verify_embeddings(name, embeddings):

    if not isinstance(embeddings, np.ndarray):
        raise TypeError(
            f"{name} embeddings are not NumPy arrays"
        )

    if embeddings.ndim != 2:
        raise ValueError(
            f"{name} embeddings must be 2-dimensional"
        )

    if embeddings.shape[1] != embedding_dimension:
        raise ValueError(
            f"{name} embedding dimension mismatch: "
            f"{embeddings.shape[1]}"
        )

    if not np.isfinite(embeddings).all():
        raise ValueError(
            f"{name} embeddings contain NaN or infinity"
        )

    print(
        f"✓ {name}: "
        f"{embeddings.shape} | "
        f"valid"
    )


verify_embeddings(
    "Training",
    train_embeddings
)

verify_embeddings(
    "Validation",
    validation_embeddings
)

verify_embeddings(
    "Test",
    test_embeddings
)

verify_embeddings(
    "Career",
    career_embeddings
)


# ==============================================================
# STEP 12 - TEST COSINE SIMILARITY
# ==============================================================

print()
print("=" * 70)
print("TESTING SKILL-TO-CAREER SIMILARITY")
print("=" * 70)


sample_embedding = validation_embeddings[0].reshape(1, -1)

similarities = cosine_similarity(
    sample_embedding,
    career_embeddings
)[0]

top_indices = np.argsort(
    similarities
)[::-1][:5]

print()
print("Sample Top-5 Career Matches:")

for rank, index in enumerate(top_indices, start=1):

    print(
        f"{rank}. "
        f"{career_names[index]} "
        f"-> {similarities[index] * 100:.2f}%"
    )


# ==============================================================
# STEP 13 - SAVE CAREER EMBEDDINGS
# ==============================================================

print()
print("=" * 70)
print("SAVING MODEL FILES")
print("=" * 70)


with open(
    CAREER_EMBEDDINGS_FILE,
    "wb"
) as f:

    pickle.dump(
        career_embeddings,
        f
    )

print(
    f"✓ Saved: "
    f"{CAREER_EMBEDDINGS_FILE}"
)


with open(
    CAREER_NAMES_FILE,
    "wb"
) as f:

    pickle.dump(
        career_names,
        f
    )

print(
    f"✓ Saved: "
    f"{CAREER_NAMES_FILE}"
)


# ==============================================================
# SAVE DATASET EMBEDDINGS
# ==============================================================

with open(
    TRAIN_EMBEDDINGS_FILE,
    "wb"
) as f:

    pickle.dump(
        train_embeddings,
        f
    )

print(
    f"✓ Saved: "
    f"{TRAIN_EMBEDDINGS_FILE}"
)


with open(
    VALIDATION_EMBEDDINGS_FILE,
    "wb"
) as f:

    pickle.dump(
        validation_embeddings,
        f
    )

print(
    f"✓ Saved: "
    f"{VALIDATION_EMBEDDINGS_FILE}"
)


with open(
    TEST_EMBEDDINGS_FILE,
    "wb"
) as f:

    pickle.dump(
        test_embeddings,
        f
    )

print(
    f"✓ Saved: "
    f"{TEST_EMBEDDINGS_FILE}"
)


# ==============================================================
# STEP 14 - SAVE MODEL INFORMATION
# ==============================================================

model_info = {

    "milestone": "Milestone 2",

    "step": "Step 3",

    "component": "Sentence-BERT Skill Embeddings",

    "model_name": MODEL_NAME,

    "embedding_dimension": int(
        embedding_dimension
    ),

    "number_of_careers": len(
        career_names
    ),

    "career_names": career_names,

    "train_samples": len(
        train_texts
    ),

    "validation_samples": len(
        validation_texts
    ),

    "test_samples": len(
        test_texts
    ),

    "normalized_embeddings": True,

    "career_profiles_created": True
}


with open(
    MODEL_INFO_FILE,
    "w"
) as f:

    json.dump(
        model_info,
        f,
        indent=4
    )

print(
    f"✓ Saved: "
    f"{MODEL_INFO_FILE}"
)


# ==============================================================
# STEP 15 - RELOAD VERIFICATION
# ==============================================================

print()
print("=" * 70)
print("RELOADING SAVED FILES")
print("=" * 70)


with open(
    CAREER_EMBEDDINGS_FILE,
    "rb"
) as f:

    reloaded_career_embeddings = pickle.load(f)


with open(
    CAREER_NAMES_FILE,
    "rb"
) as f:

    reloaded_career_names = pickle.load(f)


if np.array_equal(
    career_embeddings,
    reloaded_career_embeddings
):

    print(
        "✓ Career embeddings reload verified"
    )

else:

    raise ValueError(
        "Career embedding reload verification failed"
    )


if career_names == reloaded_career_names:

    print(
        "✓ Career names reload verified"
    )

else:

    raise ValueError(
        "Career names reload verification failed"
    )


# ==============================================================
# STEP 16 - FINAL FILE VERIFICATION
# ==============================================================

print()
print("=" * 70)
print("FINAL FILE VERIFICATION")
print("=" * 70)


files_to_verify = [

    CAREER_EMBEDDINGS_FILE,

    CAREER_NAMES_FILE,

    MODEL_INFO_FILE,

    TRAIN_EMBEDDINGS_FILE,

    VALIDATION_EMBEDDINGS_FILE,

    TEST_EMBEDDINGS_FILE
]


for file_path in files_to_verify:

    if os.path.exists(file_path):

        file_size = os.path.getsize(
            file_path
        )

        print(
            f"✓ {file_path} "
            f"({file_size:,} bytes)"
        )

    else:

        raise FileNotFoundError(
            f"File was not created: {file_path}"
        )


# ==============================================================
# FINAL SUMMARY
# ==============================================================

total_time = time.time() - start_time

print()
print("=" * 70)
print("MILESTONE 2 - STEP 3 COMPLETE")
print("=" * 70)

print(
    f"Sentence-BERT Model : {MODEL_NAME}"
)

print(
    f"Embedding Dimension  : {embedding_dimension}"
)

print(
    f"Career Classes       : {len(career_names)}"
)

print(
    f"Training Embeddings  : {train_embeddings.shape}"
)

print(
    f"Validation Embeddings: {validation_embeddings.shape}"
)

print(
    f"Test Embeddings      : {test_embeddings.shape}"
)

print(
    f"Career Embeddings     : {career_embeddings.shape}"
)

print()
print("Verified files:")

for file_path in files_to_verify:

    print(
        f"  ✓ {file_path}"
    )

print()
print(
    f"Total execution time: "
    f"{total_time:.2f} seconds"
)

print()
print("✓ SENTENCE-BERT EMBEDDINGS VERIFIED")
print("✓ MILESTONE 2 - STEP 3 COMPLETED")

print("=" * 70)