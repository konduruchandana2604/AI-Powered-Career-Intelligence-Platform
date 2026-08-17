import os
import re
import json
import hashlib
import warnings

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split


warnings.filterwarnings("ignore")


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "career_dataset.csv"

OUTPUT_DIR = "data"

CLEANED_FILE = os.path.join(
    OUTPUT_DIR,
    "career_dataset_cleaned.csv"
)

BALANCED_FILE = os.path.join(
    OUTPUT_DIR,
    "career_dataset_balanced.csv"
)

MODEL_READY_FILE = os.path.join(
    OUTPUT_DIR,
    "career_dataset_model_ready.csv"
)

TRAIN_FILE = os.path.join(
    OUTPUT_DIR,
    "train.csv"
)

VALIDATION_FILE = os.path.join(
    OUTPUT_DIR,
    "validation.csv"
)

TEST_FILE = os.path.join(
    OUTPUT_DIR,
    "test.csv"
)

REPORT_FILE = os.path.join(
    OUTPUT_DIR,
    "dataset_report.json"
)


TARGET_COLUMN = "Suggested_Career_Path"


RANDOM_STATE = 42


# ============================================================
# EXPECTED COLUMNS
# ============================================================

EXPECTED_COLUMNS = [
    "Age",
    "Gender",
    "Location",
    "Highest_qualification",
    "Stream",
    "Current_Academic_Level",
    "Grade_CGPA_Percentage",
    "Technical_Skills",
    "Soft_Skills",
    "Languages_Known",
    "Certifications",
    "Fields_of_Interest",
    "Preferred_Work_Style",
    "Work_Type_Interest",
    "Past_Jobs_Internships",
    "Achievements",
    "Skills_Gained",
    "Willing_to_Relocate",
    "Suggested_Career_Path"
]


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(value):
    """
    Normalize textual values without destroying useful
    information.
    """

    if pd.isna(value):
        return ""

    value = str(value)

    value = value.strip()

    value = value.lower()

    # Replace common separators with spaces
    value = value.replace(";", ",")
    value = value.replace("|", ",")
    value = value.replace("/", ",")
    value = value.replace("\\", ",")

    # Normalize whitespace
    value = re.sub(
        r"\s+",
        " ",
        value
    )

    # Normalize repeated commas
    value = re.sub(
        r",\s*,+",
        ",",
        value
    )

    # Remove leading/trailing commas
    value = value.strip(" ,")

    return value


# ============================================================
# CAREER NORMALIZATION
# ============================================================

def normalize_career(value):
    """
    Normalize career labels while preserving meaningful
    career distinctions.
    """

    if pd.isna(value):
        return None

    value = str(value).strip()

    if not value:
        return None

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    value = value.lower()

    # Standardized aliases
    aliases = {

        "data scientist":
            "Data Scientist",

        "data science":
            "Data Scientist",

        "data analyst":
            "Data Analyst",

        "data analytics":
            "Data Analyst",

        "machine learning engineer":
            "Machine Learning Engineer",

        "ml engineer":
            "Machine Learning Engineer",

        "artificial intelligence engineer":
            "AI Engineer",

        "ai engineer":
            "AI Engineer",

        "deep learning engineer":
            "Deep Learning Engineer",

        "software developer":
            "Software Developer",

        "software engineer":
            "Software Engineer",

        "web developer":
            "Web Developer",

        "frontend developer":
            "Frontend Developer",

        "front end developer":
            "Frontend Developer",

        "backend developer":
            "Backend Developer",

        "back end developer":
            "Backend Developer",

        "devops engineer":
            "DevOps Engineer",

        "cybersecurity analyst":
            "Cybersecurity Analyst",

        "cyber security analyst":
            "Cybersecurity Analyst",

        "ethical hacker":
            "Ethical Hacker",

        "cloud engineer":
            "Cloud Engineer",

        "cloud architect":
            "Cloud Architect",

        "business analyst":
            "Business Analyst",

        "project manager":
            "Project Manager",

        "marketing executive":
            "Marketing Executive",

        "hr manager":
            "HR Manager",

        "human resources manager":
            "HR Manager",

        "financial analyst":
            "Financial Analyst",

        "accountant":
            "Accountant",

        "ui ux designer":
            "UI/UX Designer",

        "ui/ux designer":
            "UI/UX Designer",

        "product manager":
            "Product Manager",

        "database administrator":
            "Database Administrator",

        "network engineer":
            "Network Engineer"
    }

    if value in aliases:
        return aliases[value]

    # Generic title formatting
    return value.title()


# ============================================================
# COLUMN NORMALIZATION
# ============================================================

def normalize_column_name(column):
    """
    Convert column names into a consistent format.
    """

    column = str(column).strip()

    column = re.sub(
        r"\s+",
        "_",
        column
    )

    column = re.sub(
        r"[^A-Za-z0-9_]",
        "",
        column
    )

    return column


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    print("\n" + "=" * 80)
    print("STEP 1 - DATASET CLEANING")
    print("=" * 80)

    if not os.path.exists(INPUT_FILE):

        raise FileNotFoundError(
            f"\nDataset not found: {INPUT_FILE}\n"
            f"Place the CSV file in the project directory."
        )

    print(
        f"\nLoading dataset: {INPUT_FILE}"
    )

    df = pd.read_csv(
        INPUT_FILE,
        encoding="utf-8",
        low_memory=False
    )

    print(
        f"Original dataset shape: {df.shape}"
    )

    return df


# ============================================================
# COLUMN CLEANING
# ============================================================

def clean_columns(df):

    print("\n[1/10] Normalizing column names...")

    df = df.copy()

    df.columns = [
        normalize_column_name(column)
        for column in df.columns
    ]

    print("\nColumns found:")

    for column in df.columns:
        print(
            f"  - {column}"
        )

    if TARGET_COLUMN not in df.columns:

        raise ValueError(
            f"\nTarget column '{TARGET_COLUMN}' "
            f"was not found."
        )

    return df


# ============================================================
# REMOVE COMPLETELY EMPTY COLUMNS
# ============================================================

def remove_empty_columns(df):

    print("\n[2/10] Removing completely empty columns...")

    empty_columns = []

    for column in df.columns:

        if df[column].isna().all():

            empty_columns.append(
                column
            )

    if empty_columns:

        print(
            "Removing:",
            empty_columns
        )

        df = df.drop(
            columns=empty_columns
        )

    else:

        print(
            "No completely empty columns found."
        )

    return df


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text_columns(df):

    print("\n[3/10] Cleaning text fields...")

    df = df.copy()

    for column in df.columns:

        if column == TARGET_COLUMN:

            continue

        if df[column].dtype == "object":

            df[column] = (
                df[column]
                .apply(normalize_text)
            )

    return df


# ============================================================
# NUMERIC CLEANING
# ============================================================

def clean_numeric_columns(df):

    print("\n[4/10] Cleaning numeric fields...")

    df = df.copy()

    if "Age" in df.columns:

        df["Age"] = pd.to_numeric(
            df["Age"],
            errors="coerce"
        )

        # Keep realistic age range
        df.loc[
            (df["Age"] < 15) |
            (df["Age"] > 80),
            "Age"
        ] = np.nan

    if "Grade_CGPA_Percentage" in df.columns:

        grade = (
            df["Grade_CGPA_Percentage"]
            .astype(str)
        )

        # Extract first numeric value
        extracted = grade.str.extract(
            r"(\d+(?:\.\d+)?)"
        )[0]

        df["Grade_CGPA_Percentage"] = pd.to_numeric(
            extracted,
            errors="coerce"
        )

    return df


# ============================================================
# TARGET CLEANING
# ============================================================

def clean_target(df):

    print("\n[5/10] Cleaning target labels...")

    df = df.copy()

    df[TARGET_COLUMN] = (
        df[TARGET_COLUMN]
        .apply(normalize_career)
    )

    before = len(df)

    df = df.dropna(
        subset=[TARGET_COLUMN]
    )

    removed = before - len(df)

    print(
        f"Removed rows with invalid target: {removed}"
    )

    print(
        f"Number of career classes: "
        f"{df[TARGET_COLUMN].nunique()}"
    )

    print("\nCareer distribution:")

    print(
        df[TARGET_COLUMN]
        .value_counts()
        .to_string()
    )

    return df


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicates(df):

    print("\n[6/10] Removing duplicates...")

    before = len(df)

    df = df.drop_duplicates()

    removed = before - len(df)

    print(
        f"Exact duplicate rows removed: {removed}"
    )

    return df


# ============================================================
# PROFILE QUALITY
# ============================================================

PROFILE_COLUMNS = [
    "Technical_Skills",
    "Soft_Skills",
    "Languages_Known",
    "Certifications",
    "Fields_of_Interest",
    "Past_Jobs_Internships",
    "Achievements",
    "Skills_Gained"
]


def calculate_information_score(row):

    score = 0

    for column in PROFILE_COLUMNS:

        if column not in row.index:
            continue

        value = str(
            row[column]
        ).strip()

        if value and value != "nan":

            if len(value) >= 2:
                score += 1

    return score


def remove_low_information_rows(df):

    print(
        "\n[7/10] Removing extremely "
        "low-information profiles..."
    )

    df = df.copy()

    df["information_score"] = (
        df.apply(
            calculate_information_score,
            axis=1
        )
    )

    before = len(df)

    # Require at least 2 meaningful profile fields
    df = df[
        df["information_score"] >= 2
    ]

    removed = before - len(df)

    print(
        f"Low-information rows removed: {removed}"
    )

    df = df.drop(
        columns=["information_score"]
    )

    return df


# ============================================================
# PROFILE SIGNATURE
# ============================================================

SIGNATURE_COLUMNS = [
    "Technical_Skills",
    "Soft_Skills",
    "Languages_Known",
    "Certifications",
    "Fields_of_Interest",
    "Past_Jobs_Internships",
    "Skills_Gained"
]


def create_profile_signature(row):

    values = []

    for column in SIGNATURE_COLUMNS:

        if column in row.index:

            value = str(
                row[column]
            ).strip()

            value = normalize_text(
                value
            )

            values.append(value)

    combined = " | ".join(
        values
    )

    return hashlib.md5(
        combined.encode("utf-8")
    ).hexdigest()


def remove_profile_duplicates(df):

    print(
        "\nRemoving duplicate profiles..."
    )

    df = df.copy()

    df["_profile_signature"] = (
        df.apply(
            create_profile_signature,
            axis=1
        )
    )

    before = len(df)

    df = df.drop_duplicates(
        subset=["_profile_signature"],
        keep="first"
    )

    removed = before - len(df)

    print(
        f"Duplicate profiles removed: {removed}"
    )

    df = df.drop(
        columns=["_profile_signature"]
    )

    return df


# ============================================================
# NORMALIZE MISSING VALUES
# ============================================================

def fill_missing_values(df):

    print(
        "\n[8/10] Handling missing values..."
    )

    df = df.copy()

    text_columns = [
        column
        for column in df.columns
        if df[column].dtype == "object"
    ]

    for column in text_columns:

        if column == TARGET_COLUMN:
            continue

        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    if "Age" in df.columns:

        median_age = df["Age"].median()

        if pd.isna(median_age):
            median_age = 21

        df["Age"] = (
            df["Age"]
            .fillna(median_age)
        )

    if "Grade_CGPA_Percentage" in df.columns:

        median_grade = (
            df[
                "Grade_CGPA_Percentage"
            ].median()
        )

        if pd.isna(median_grade):
            median_grade = 70

        df[
            "Grade_CGPA_Percentage"
        ] = (
            df[
                "Grade_CGPA_Percentage"
            ]
            .fillna(median_grade)
        )

    return df


# ============================================================
# CREATE ML TEXT FEATURE
# ============================================================

def create_ml_text(df):

    print(
        "\n[9/10] Creating ML text feature..."
    )

    df = df.copy()

    columns = [

        "Highest_qualification",

        "Stream",

        "Current_Academic_Level",

        "Technical_Skills",

        "Soft_Skills",

        "Languages_Known",

        "Certifications",

        "Fields_of_Interest",

        "Preferred_Work_Style",

        "Work_Type_Interest",

        "Past_Jobs_Internships",

        "Achievements",

        "Skills_Gained",

        "Willing_to_Relocate"
    ]

    available_columns = [
        column
        for column in columns
        if column in df.columns
    ]

    df["ML_Text"] = (
        df[
            available_columns
        ]
        .fillna("")
        .astype(str)
        .agg(
            " ".join,
            axis=1
        )
    )

    # Normalize final text
    df["ML_Text"] = (
        df["ML_Text"]
        .apply(normalize_text)
    )

    # Remove profiles with almost no text
    df = df[
        df["ML_Text"].str.len() >= 10
    ]

    return df


# ============================================================
# BALANCE DATASET
# ============================================================

def balance_dataset(df):

    print(
        "\n[10/10] Creating balanced dataset..."
    )

    counts = (
        df[TARGET_COLUMN]
        .value_counts()
    )

    print("\nOriginal class counts:")

    print(
        counts.to_string()
    )

    # Use a robust target size.
    #
    # We use the minimum class count so that
    # every class has equal representation.
    target_per_class = int(
        counts.min()
    )

    print(
        f"\nTarget records per career: "
        f"{target_per_class}"
    )

    balanced_parts = []

    for career in sorted(
        df[TARGET_COLUMN].unique()
    ):

        career_df = df[
            df[TARGET_COLUMN] == career
        ]

        # Deterministic sampling
        career_df = career_df.sample(
            n=target_per_class,
            random_state=RANDOM_STATE
        )

        balanced_parts.append(
            career_df
        )

    balanced = pd.concat(
        balanced_parts,
        ignore_index=True
    )

    balanced = balanced.sample(
        frac=1,
        random_state=RANDOM_STATE
    ).reset_index(
        drop=True
    )

    print(
        "\nBalanced distribution:"
    )

    print(
        balanced[
            TARGET_COLUMN
        ].value_counts().to_string()
    )

    return balanced


# ============================================================
# DATASET SPLIT
# ============================================================

def create_splits(df):

    print(
        "\nCreating stratified "
        "train/validation/test splits..."
    )

    train_df, temp_df = train_test_split(
        df,
        test_size=0.30,
        random_state=RANDOM_STATE,
        stratify=df[TARGET_COLUMN]
    )

    validation_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        random_state=RANDOM_STATE,
        stratify=temp_df[TARGET_COLUMN]
    )

    print(
        "\nSplit sizes:"
    )

    print(
        f"Train      : {len(train_df)}"
    )

    print(
        f"Validation : {len(validation_df)}"
    )

    print(
        f"Test       : {len(test_df)}"
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
    original_df,
    cleaned_df,
    balanced_df,
    train_df,
    validation_df,
    test_df
):

    report = {

        "random_state":
            RANDOM_STATE,

        "original_rows":
            int(len(original_df)),

        "original_columns":
            int(len(original_df.columns)),

        "cleaned_rows":
            int(len(cleaned_df)),

        "cleaned_columns":
            int(len(cleaned_df.columns)),

        "balanced_rows":
            int(len(balanced_df)),

        "number_of_careers":
            int(
                balanced_df[
                    TARGET_COLUMN
                ].nunique()
            ),

        "train_rows":
            int(len(train_df)),

        "validation_rows":
            int(len(validation_df)),

        "test_rows":
            int(len(test_df)),

        "career_distribution_original":
            {
                str(k): int(v)
                for k, v in
                original_df[
                    TARGET_COLUMN
                ]
                .value_counts(dropna=False)
                .items()
            },

        "career_distribution_cleaned":
            {
                str(k): int(v)
                for k, v in
                cleaned_df[
                    TARGET_COLUMN
                ]
                .value_counts()
                .items()
            },

        "career_distribution_balanced":
            {
                str(k): int(v)
                for k, v in
                balanced_df[
                    TARGET_COLUMN
                ]
                .value_counts()
                .items()
            },

        "missing_values_after_cleaning":
            {
                str(k): int(v)
                for k, v in
                cleaned_df.isna()
                .sum()
                .items()
            },

        "train_classes":
            int(
                train_df[
                    TARGET_COLUMN
                ].nunique()
            ),

        "validation_classes":
            int(
                validation_df[
                    TARGET_COLUMN
                ].nunique()
            ),

        "test_classes":
            int(
                test_df[
                    TARGET_COLUMN
                ].nunique()
            )
    }

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )

    return report


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    original_df = load_dataset()

    # --------------------------------------------------------
    # Clean columns
    # --------------------------------------------------------

    df = clean_columns(
        original_df
    )

    # --------------------------------------------------------
    # Remove empty columns
    # --------------------------------------------------------

    df = remove_empty_columns(
        df
    )

    # --------------------------------------------------------
    # Clean text
    # --------------------------------------------------------

    df = clean_text_columns(
        df
    )

    # --------------------------------------------------------
    # Numeric cleaning
    # --------------------------------------------------------

    df = clean_numeric_columns(
        df
    )

    # --------------------------------------------------------
    # Target cleaning
    # --------------------------------------------------------

    df = clean_target(
        df
    )

    # --------------------------------------------------------
    # Remove exact duplicates
    # --------------------------------------------------------

    df = remove_duplicates(
        df
    )

    # --------------------------------------------------------
    # Remove low-information rows
    # --------------------------------------------------------

    df = remove_low_information_rows(
        df
    )

    # --------------------------------------------------------
    # Remove duplicate profiles
    # --------------------------------------------------------

    df = remove_profile_duplicates(
        df
    )

    # --------------------------------------------------------
    # Fill missing values
    # --------------------------------------------------------

    df = fill_missing_values(
        df
    )

    # --------------------------------------------------------
    # Save cleaned dataset
    # --------------------------------------------------------

    df.to_csv(
        CLEANED_FILE,
        index=False
    )

    print(
        f"\nCleaned dataset saved:"
        f"\n{CLEANED_FILE}"
    )

    # --------------------------------------------------------
    # Create ML text
    # --------------------------------------------------------

    df = create_ml_text(
        df
    )

    # --------------------------------------------------------
    # Balance
    # --------------------------------------------------------

    balanced_df = balance_dataset(
        df
    )

    # --------------------------------------------------------
    # Save balanced dataset
    # --------------------------------------------------------

    balanced_df.to_csv(
        BALANCED_FILE,
        index=False
    )

    print(
        f"\nBalanced dataset saved:"
        f"\n{BALANCED_FILE}"
    )

    # --------------------------------------------------------
    # Model-ready dataset
    # --------------------------------------------------------

    model_ready = balanced_df[
        [
            "ML_Text",
            TARGET_COLUMN
        ]
    ].copy()

    model_ready.to_csv(
        MODEL_READY_FILE,
        index=False
    )

    print(
        f"\nModel-ready dataset saved:"
        f"\n{MODEL_READY_FILE}"
    )

    # --------------------------------------------------------
    # Train/validation/test
    # --------------------------------------------------------

    train_df, validation_df, test_df = (
        create_splits(
            model_ready
        )
    )

    # --------------------------------------------------------
    # Save splits
    # --------------------------------------------------------

    train_df.to_csv(
        TRAIN_FILE,
        index=False
    )

    validation_df.to_csv(
        VALIDATION_FILE,
        index=False
    )

    test_df.to_csv(
        TEST_FILE,
        index=False
    )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    report = create_report(
        original_df,
        df,
        balanced_df,
        train_df,
        validation_df,
        test_df
    )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print(
        "\n" + "=" * 80
    )

    print(
        "DATASET PREPARATION COMPLETE"
    )

    print(
        "=" * 80
    )

    print(
        f"\nOriginal dataset:"
        f" {len(original_df)} rows"
    )

    print(
        f"Cleaned dataset:"
        f" {len(df)} rows"
    )

    print(
        f"Balanced dataset:"
        f" {len(balanced_df)} rows"
    )

    print(
        f"Number of careers:"
        f" {balanced_df[TARGET_COLUMN].nunique()}"
    )

    print(
        f"\nTrain:"
        f" {len(train_df)}"
    )

    print(
        f"Validation:"
        f" {len(validation_df)}"
    )

    print(
        f"Test:"
        f" {len(test_df)}"
    )

    print(
        "\nFiles generated:"
    )

    print(
        f"  {CLEANED_FILE}"
    )

    print(
        f"  {BALANCED_FILE}"
    )

    print(
        f"  {MODEL_READY_FILE}"
    )

    print(
        f"  {TRAIN_FILE}"
    )

    print(
        f"  {VALIDATION_FILE}"
    )

    print(
        f"  {TEST_FILE}"
    )

    print(
        f"  {REPORT_FILE}"
    )

    print(
        "\nNext step:"
    )

    print(
        "Train Logistic Regression using "
        "data/train.csv."
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()