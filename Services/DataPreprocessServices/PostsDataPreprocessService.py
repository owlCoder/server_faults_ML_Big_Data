import pandas as pd

from Services.TextCleanUpService.TextCleanService import clean_text


def preprocess_posts_data(posts_df, reputable_user_ids):
    """
    Preprocesses the posts data to filter relevant columns, keep posts
    created only by reputable users, and include only specific PostTypeIds (1 or 2).

    Args:
        posts_df (pd.DataFrame): The DataFrame containing posts data.
        reputable_user_ids (list): A list of AccountIds representing reputable users.

    Returns:
        pd.DataFrame: The preprocessed DataFrame containing only relevant columns
                      and posts created by reputable users with PostTypeId 1 or 2.
    """
    # Filter the DataFrame to include only reputable users and PostTypeId 1 or 2
    posts_df['OwnerUserId'] = posts_df['OwnerUserId'].astype(str)
    reputable_user_ids = [str(user_id) for user_id in reputable_user_ids]

    posts_df = posts_df[
        (posts_df['OwnerUserId'].isin(reputable_user_ids)) &
        (posts_df['PostTypeId'].isin(["1", "2"]))
    ]

    # Retain only the specified columns
    posts_df = posts_df[['PostTypeId', 'Score', 'Title', 'OwnerUserId', 'AnswerCount', 'Body']]

    # Remove html content - not relevant
    posts_df['Body'] = posts_df['Body'].apply(clean_text)

    return posts_df