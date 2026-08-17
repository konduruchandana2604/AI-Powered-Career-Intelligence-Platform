import pandas as pd
import numpy as np


TARGET = "Suggested_Career_Path"


def load_dataset(path="career_dataset.csv"):
    df = pd.read_csv(path)

    print("=" * 70)
    print("DATASET INFORMATION")
    print("=" * 70)

    print("Shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    if TARGET not in df.columns:
        raise ValueError(
            f"Target column '{TARGET}' not found in dataset."
        )

    df = df.drop_duplicates()

    df[TARGET] = df[TARGET].astype(str).str.strip()

    df = df[df[TARGET] != ""]

    df = df.fillna("Unknown")

    print("\nCleaned shape:", df.shape)
    print("\nCareer distribution:")
    print(df[TARGET].value_counts())

    return df


def create_text_features(df):
    """
    Creates a unified text representation of the user's profile.
    """

    feature_columns = [
        "Gender",
        "Location",
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

    existing_columns = [
        c for c in feature_columns
        if c in df.columns
    ]

    text = df[existing_columns].astype(str).agg(
        " ".join,
        axis=1
    )

    return text


if __name__ == "__main__":
    df = load_dataset()

    text = create_text_features(df)

    print("\nExample feature:")
    print(text.iloc[0])