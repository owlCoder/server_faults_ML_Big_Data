import pandas as pd
from Domain.Constants.XmlPaths import COMMENTS_XML_PATH

def load_comments_data():
    """
    Loads the data from multiple Comments XML files and returns them as a single pandas DataFrame.

    This method reads multiple Comments XML files (e.g., Comments-1.xml, Comments-2.xml, ...)
    and concatenates them into one DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing all the comments data combined.
    """
    # Initialize an empty list to store DataFrames
    all_comments_data = []

    # Read multiple Comments XML files
    for i in range(1, 2):
        comments_df = pd.read_xml(COMMENTS_XML_PATH.format(i))
        all_comments_data.append(comments_df)

    # Concatenate all the data into a single DataFrame
    combined_comments_df = pd.concat(all_comments_data, ignore_index=True)

    # Return the combined DataFrame
    return combined_comments_df
