import pandas as pd
from Domain.Constants.XmlPaths import POSTS_XML_PATH

def load_posts_data():
    """
    Loads the data from multiple Posts XML files and returns them as a single pandas DataFrame.

    This method reads multiple Posts XML files (e.g., Posts-1.xml, Posts-2.xml, ...)
    and concatenates them into one DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing all the posts data combined.
    """
    # Initialize an empty list to store DataFrames
    all_posts_data = []

    # Read multiple Posts XML files
    for i in range(1, 2):
        posts_df = pd.read_xml(POSTS_XML_PATH.format(i))
        all_posts_data.append(posts_df)

    # Concatenate all the data into a single DataFrame
    combined_posts_df = pd.concat(all_posts_data, ignore_index=True)

    # Return the combined DataFrame
    return combined_posts_df
