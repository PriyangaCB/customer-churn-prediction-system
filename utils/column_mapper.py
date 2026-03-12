import pandas as pd
from difflib import get_close_matches

def auto_match_columns(df, expected_columns, threshold=0.6):
    """
    Automatically match incoming dataset columns
    to model expected columns using similarity matching
    """

    df_columns = df.columns.tolist()

    column_mapping = {}

    for exp_col in expected_columns:

        match = get_close_matches(exp_col, df_columns, n=1, cutoff=threshold)

        if match:
            column_mapping[match[0]] = exp_col

    # rename columns
    df = df.rename(columns=column_mapping)

    return df


def align_missing_columns(df, expected_columns):
    """
    Add missing columns with default value
    """

    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0

    # keep only required columns in correct order
    df = df[expected_columns]

    return df