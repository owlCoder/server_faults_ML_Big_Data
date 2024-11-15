from sklearn.decomposition import PCA
import numpy as np
import pandas as pd

def apply_pca_on_user_df(scaled_data, account_ids, n_components=2):
    """
    Applies PCA on the preprocessed data and reduces its dimensions to n_components, while retaining AccountId.

    Args:
        scaled_data (np.ndarray or pd.DataFrame): The standardized data (without 'AccountId').
        account_ids (pd.Series or np.ndarray): The original AccountId values.
        n_components (int): The number of principal components to keep.

    Returns:
        pd.DataFrame: The data transformed to the new PCA space with reduced dimensions, and includes 'AccountId'.
    """
    # Check if the scaled data contains NaN or infinite values
    if np.any(np.isnan(scaled_data)):
        raise ValueError("Input data contains NaN values. Please clean the data before applying PCA.")

    if np.any(np.isinf(scaled_data)):
        raise ValueError("Input data contains infinite values. Please clean the data before applying PCA.")

    # Check that the number of components does not exceed the number of features in the data
    if n_components > scaled_data.shape[1]:
        raise ValueError(
            f"n_components cannot be greater than the number of features ({scaled_data.shape[1]}) in the data.")

    # Apply PCA to reduce the data dimensions
    pca = PCA(n_components=n_components)
    users_reduced = pca.fit_transform(scaled_data)

    # Create a DataFrame from the PCA result, with 'AccountId' retained
    users_reduced_df = pd.DataFrame(users_reduced, columns=['Reputation'])
    users_reduced_df['AccountId'] = account_ids.values

    return users_reduced_df
