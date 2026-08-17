import os
import json
import pickle
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


# ============================================================
# MILESTONE 2
# TOP-K CAREER RANKING & RECOMMENDATION ENGINE
# ============================================================

print("=" * 70)
print("MILESTONE 2 - TOP-K CAREER RECOMMENDATION ENGINE")
print("=" * 70)


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)


# ============================================================
# FILE PATHS
# ============================================================

RF_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "random_forest.pkl"
)

RF_TFIDF_PATH = os.path.join(
    MODEL_DIR,
    "random_forest_tfidf.pkl"
)

RF_ENCODER_PATH = os.path.join(
    MODEL_DIR,
    "random_forest_label_encoder.pkl"
)

XGB_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "xgboost.pkl"
)

XGB_TFIDF_PATH = os.path.join(
    MODEL_DIR,
    "xgboost_tfidf.pkl"
)

XGB_ENCODER_PATH = os.path.join(
    MODEL_DIR,
    "xgboost_label_encoder.pkl"
)

SBERT_EMBEDDINGS_PATH = os.path.join(
    MODEL_DIR,
    "sentence_bert_career_embeddings.pkl"
)

SBERT_NAMES_PATH = os.path.join(
    MODEL_DIR,
    "sentence_bert_career_names.pkl"
)


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def load_pickle(path):
    """
    Load a pickle/joblib-compatible file.
    """

    if not os.path.exists(path):

        raise FileNotFoundError(
            f"Required model file not found: {path}"
        )

    with open(path, "rb") as file:

        return pickle.load(file)


def verify_file(path):

    if not os.path.exists(path):

        raise FileNotFoundError(
            f"Required file not found: {path}"
        )

    print(f"✓ {path}")


def normalize_scores(scores):
    """
    Convert arbitrary similarity scores into
    a 0-100 range.
    """

    scores = np.asarray(
        scores,
        dtype=float
    )

    minimum = scores.min()
    maximum = scores.max()

    if maximum == minimum:

        return np.ones_like(
            scores
        ) * 100.0

    normalized = (
        (scores - minimum)
        /
        (maximum - minimum)
    ) * 100.0

    return normalized


def top_k_indices(scores, k=5):

    k = min(
        k,
        len(scores)
    )

    return np.argsort(
        scores
    )[::-1][:k]


# ============================================================
# VERIFY REQUIRED FILES
# ============================================================

print()
print("=" * 70)
print("CHECKING REQUIRED MODEL FILES")
print("=" * 70)

required_files = [

    RF_MODEL_PATH,
    RF_TFIDF_PATH,
    RF_ENCODER_PATH,

    XGB_MODEL_PATH,
    XGB_TFIDF_PATH,
    XGB_ENCODER_PATH,

    SBERT_EMBEDDINGS_PATH,
    SBERT_NAMES_PATH

]

for file_path in required_files:

    verify_file(file_path)


# ============================================================
# LOAD RANDOM FOREST
# ============================================================

print()
print("=" * 70)
print("LOADING RANDOM FOREST")
print("=" * 70)

rf_model = load_pickle(
    RF_MODEL_PATH
)

rf_tfidf = load_pickle(
    RF_TFIDF_PATH
)

rf_label_encoder = load_pickle(
    RF_ENCODER_PATH
)

print("✓ Random Forest model loaded")
print("✓ Random Forest TF-IDF loaded")
print("✓ Random Forest Label Encoder loaded")


# ============================================================
# LOAD XGBOOST
# ============================================================

print()
print("=" * 70)
print("LOADING XGBOOST")
print("=" * 70)

xgb_model = load_pickle(
    XGB_MODEL_PATH
)

xgb_tfidf = load_pickle(
    XGB_TFIDF_PATH
)

xgb_label_encoder = load_pickle(
    XGB_ENCODER_PATH
)

print("✓ XGBoost model loaded")
print("✓ XGBoost TF-IDF loaded")
print("✓ XGBoost Label Encoder loaded")


# ============================================================
# LOAD SENTENCE-BERT CAREER EMBEDDINGS
# ============================================================

print()
print("=" * 70)
print("LOADING SENTENCE-BERT CAREER EMBEDDINGS")
print("=" * 70)

career_embeddings = load_pickle(
    SBERT_EMBEDDINGS_PATH
)

career_names = load_pickle(
    SBERT_NAMES_PATH
)

career_embeddings = np.asarray(
    career_embeddings,
    dtype=np.float32
)

print(
    "✓ Career embeddings loaded:",
    career_embeddings.shape
)

print(
    "✓ Career names loaded:",
    len(career_names)
)


# ============================================================
# LOAD SENTENCE-BERT MODEL ONCE
# ============================================================

print()
print("=" * 70)
print("LOADING SENTENCE-BERT MODEL")
print("=" * 70)

SBERT_MODEL_NAME = "all-MiniLM-L6-v2"

print(
    "Model:",
    SBERT_MODEL_NAME
)

sbert_model = SentenceTransformer(
    SBERT_MODEL_NAME
)

print(
    "✓ Sentence-BERT model loaded"
)

print(
    "✓ Embedding dimension:",
    sbert_model.get_sentence_embedding_dimension()
)


# ============================================================
# VERIFY CAREER CLASSES
# ============================================================

print()
print("=" * 70)
print("VERIFYING CAREER CLASSES")
print("=" * 70)

rf_classes = list(
    rf_label_encoder.classes_
)

xgb_classes = list(
    xgb_label_encoder.classes_
)

print(
    "Number of career classes:",
    len(career_names)
)

for index, career in enumerate(
    career_names
):

    print(
        f"{index:02d} -> {career}"
    )


# ============================================================
# VERIFY MODEL CONSISTENCY
# ============================================================

print()
print("=" * 70)
print("VERIFYING MODEL CLASS CONSISTENCY")
print("=" * 70)

print(
    "Random Forest classes :",
    len(rf_classes)
)

print(
    "XGBoost classes       :",
    len(xgb_classes)
)

print(
    "Sentence-BERT careers :",
    len(career_names)
)


if set(rf_classes) != set(xgb_classes):

    raise ValueError(
        "Random Forest and XGBoost career classes do not match."
    )


if set(rf_classes) != set(career_names):

    raise ValueError(
        "Sentence-BERT career names do not match classifier classes."
    )


print(
    "✓ Random Forest and XGBoost classes match"
)

print(
    "✓ Sentence-BERT career names match classifier classes"
)


# ============================================================
# CAREER NAME -> INDEX
# ============================================================

career_to_index = {

    career: index

    for index, career
    in enumerate(career_names)

}


# ============================================================
# MAIN RECOMMENDATION FUNCTION
# ============================================================

def recommend_careers(
    user_text,
    top_k=5,
    rf_weight=0.35,
    xgb_weight=0.35,
    sbert_weight=0.30
):
    """
    Generate Top-K career recommendations.

    Hybrid model:

    Random Forest      = 35%
    XGBoost            = 35%
    Sentence-BERT      = 30%

    Returns:

    rank
    career
    hybrid_score
    random_forest_confidence
    xgboost_confidence
    skill_alignment
    """

    # --------------------------------------------------------
    # VALIDATE INPUT
    # --------------------------------------------------------

    if not user_text:

        raise ValueError(
            "User text cannot be empty."
        )

    user_text = str(
        user_text
    ).strip()

    if len(user_text) < 20:

        raise ValueError(
            "Resume text is too short. "
            "Please provide more information."
        )


    # --------------------------------------------------------
    # RANDOM FOREST
    # --------------------------------------------------------

    rf_vector = rf_tfidf.transform(
        [user_text]
    )

    rf_probabilities = (
        rf_model.predict_proba(
            rf_vector
        )[0]
    )


    # --------------------------------------------------------
    # XGBOOST
    # --------------------------------------------------------

    xgb_vector = xgb_tfidf.transform(
        [user_text]
    )

    xgb_probabilities = (
        xgb_model.predict_proba(
            xgb_vector
        )[0]
    )


    # --------------------------------------------------------
    # SENTENCE-BERT
    # --------------------------------------------------------

    user_embedding = (
        sbert_model.encode(
            [user_text],
            convert_to_numpy=True,
            normalize_embeddings=True
        )
    )

    user_embedding = np.asarray(
        user_embedding,
        dtype=np.float32
    )


    # --------------------------------------------------------
    # COSINE SIMILARITY
    # --------------------------------------------------------

    similarities = cosine_similarity(
        user_embedding,
        career_embeddings
    )[0]


    # --------------------------------------------------------
    # NORMALIZE SBERT SCORES
    # --------------------------------------------------------

    sbert_scores = normalize_scores(
        similarities
    )


    # --------------------------------------------------------
    # ALIGN RANDOM FOREST SCORES
    # --------------------------------------------------------

    rf_scores = np.zeros(
        len(career_names),
        dtype=float
    )

    for classifier_index, career in enumerate(
        rf_classes
    ):

        career_index = career_to_index[
            career
        ]

        rf_scores[career_index] = (
            rf_probabilities[
                classifier_index
            ] * 100.0
        )


    # --------------------------------------------------------
    # ALIGN XGBOOST SCORES
    # --------------------------------------------------------

    xgb_scores = np.zeros(
        len(career_names),
        dtype=float
    )

    for classifier_index, career in enumerate(
        xgb_classes
    ):

        career_index = career_to_index[
            career
        ]

        xgb_scores[career_index] = (
            xgb_probabilities[
                classifier_index
            ] * 100.0
        )


    # --------------------------------------------------------
    # HYBRID SCORE
    # --------------------------------------------------------

    hybrid_scores = (

        rf_weight * rf_scores

        +

        xgb_weight * xgb_scores

        +

        sbert_weight * sbert_scores

    )


    # --------------------------------------------------------
    # TOP-K
    # --------------------------------------------------------

    ranked_indices = top_k_indices(
        hybrid_scores,
        top_k
    )


    recommendations = []


    for rank, index in enumerate(
        ranked_indices,
        start=1
    ):

        recommendation = {

            "rank":
                rank,

            "career":
                career_names[index],

            "hybrid_score":
                round(
                    float(
                        hybrid_scores[index]
                    ),
                    2
                ),

            "random_forest_confidence":
                round(
                    float(
                        rf_scores[index]
                    ),
                    2
                ),

            "xgboost_confidence":
                round(
                    float(
                        xgb_scores[index]
                    ),
                    2
                ),

            "skill_alignment":
                round(
                    float(
                        sbert_scores[index]
                    ),
                    2
                )

        }

        recommendations.append(
            recommendation
        )


    return recommendations


# ============================================================
# DISPLAY RECOMMENDATIONS
# ============================================================

def display_recommendations(
    recommendations
):

    print()
    print("=" * 70)
    print("TOP CAREER RECOMMENDATIONS")
    print("=" * 70)

    for recommendation in recommendations:

        print(
            f"\n{recommendation['rank']}. "
            f"{recommendation['career']}"
        )

        print(
            "   Hybrid Score       : "
            f"{recommendation['hybrid_score']}%"
        )

        print(
            "   Random Forest      : "
            f"{recommendation['random_forest_confidence']}%"
        )

        print(
            "   XGBoost            : "
            f"{recommendation['xgboost_confidence']}%"
        )

        print(
            "   Skill Alignment    : "
            f"{recommendation['skill_alignment']}%"
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    sample_text = """
    Python programming, machine learning, deep learning,
    artificial intelligence, TensorFlow, PyTorch, NumPy,
    Pandas, scikit-learn, data analysis, neural networks,
    natural language processing and model development.
    """

    print()
    print("=" * 70)
    print("TESTING RECOMMENDATION ENGINE")
    print("=" * 70)

    recommendations = recommend_careers(
        sample_text,
        top_k=5
    )

    display_recommendations(
        recommendations
    )

    output_path = os.path.join(
        MODEL_DIR,
        "sample_career_recommendations.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            recommendations,
            file,
            indent=4
        )

    print()
    print(
        "✓ Saved:",
        output_path
    )

    print()
    print(
        "✓ MILESTONE 2 RECOMMENDATION ENGINE VERIFIED"
    )