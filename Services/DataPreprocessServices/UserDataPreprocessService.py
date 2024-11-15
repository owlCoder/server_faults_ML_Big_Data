import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from Services.DataDimsReductionServices.UserDimsReductionService import apply_pca_on_user_df

def preprocess_users_data(users_df):
    """
    Preprocesses the user data to select relevant columns, apply scaling for PCA,
    and retain the original AccountId (not scaled) while excluding rows with AccountId < 1.

    Args:
        users_df (pd.DataFrame): The DataFrame containing users data.

    Returns:
        pd.DataFrame: The preprocessed DataFrame containing only relevant columns for PCA,
                      with the original 'AccountId' kept intact, and rows with AccountId < 1 removed.
    """
    # Filter out rows where AccountId is less than 1
    users_df = users_df[users_df['AccountId'] >= 1]

    # Select only the relevant columns: 'AccountId', 'DisplayName', 'Reputation'
    users_df_selected = users_df[['AccountId', 'DisplayName', 'Reputation', 'UpVotes']]

    # Drop 'DisplayName' since it's categorical and cannot be used in PCA
    users_df_selected = users_df_selected.drop(columns=['DisplayName'])

    # Initialize the SimpleImputer to fill missing values with the mean
    imputer = SimpleImputer(strategy='mean')

    # Apply the imputer to fill missing values in numerical columns
    users_df_selected_imputed = imputer.fit_transform(users_df_selected)

    # Separate the 'AccountId' from the features to be scaled
    account_ids = users_df_selected['AccountId']
    features_to_scale = users_df_selected_imputed[:, 1:]  # Only scale 'Reputation', drop 'AccountId'

    # Standardize the data (only for numeric columns)
    scalar = StandardScaler()
    scaled_data = scalar.fit_transform(features_to_scale)

    # Apply PCA and include 'AccountId'
    users_reduced_df = apply_pca_on_user_df(scaled_data, account_ids, n_components=1)

    return users_reduced_df
