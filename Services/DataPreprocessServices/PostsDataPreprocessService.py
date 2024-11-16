import pandas as pd

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
    # Define the columns to keep
    columns_to_keep = ['PostTypeId', 'Score', 'Title', 'OwnerUserId', 'AnswerCount', 'Body']

    # Filter the DataFrame to include only reputable users and PostTypeId 1 or 2
    filtered_posts_df = posts_df[
        (posts_df['OwnerUserId'].isin(reputable_user_ids)) &
        (posts_df['PostTypeId'].isin([1, 2]))
    ]

    # Retain only the specified columns
    filtered_posts_df = filtered_posts_df[columns_to_keep]

    return filtered_posts_df
