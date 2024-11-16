import pandas as pd
from Services.TextCleanUpService.TextCleanService import clean_text

def preprocess_comments_data(comments_df):
    """
    Preprocesses the comments data by keeping only relevant columns, cleaning the 'Text' column,
    and filtering out comments from users who are not reputable.

    Args:
        comments_df (pd.DataFrame): The DataFrame containing comments data.

    Returns:
        pd.DataFrame: The preprocessed DataFrame with selected columns and cleaned 'Text' column,
                      and only comments from reputable users.
    """
    # Select only the relevant columns
    comments_df = comments_df[['PostId', 'Score', 'Text', 'UserId']]

    # Drop rows where 'UserId' is missing (optional)
    comments_df = comments_df.dropna(subset=['UserId'])

    # Clean the 'Text' column to remove HTML tags and unwanted whitespace characters
    comments_df['Text'] = comments_df['Text'].apply(clean_text)

    return comments_df
