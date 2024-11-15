from sklearn.decomposition import PCA

def apply_pca_on_user_df(scaled_data, n_components=2):
    """
    Applies PCA on the preprocessed data and reduces its dimensions to n_components.
    
    Args:
        scaled_data (np.ndarray): The standardized data.
        n_components (int): The number of principal components to keep.
    
    Returns:
        np.ndarray: The data transformed to the new PCA space with reduced dimensions.
    """
    pca = PCA(n_components=n_components)
    users_reduced = pca.fit_transform(scaled_data)
    
    return users_reduced