import pandas as pd
from Domain.Constants.XmlPaths import COMMENTS_XML_PATH, POSTS_XML_PATH, USERS_XML_PATH

def load_comments_data():
    """
    Loads the comments data from the XML file and returns it as a pandas DataFrame.

    This method reads the XML file located at the path specified by 
    `COMMENTS_XML_PATH` in the Constants module, and returns it as a DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing the comments data.
    """
    # Load the XML data into a pandas DataFrame
    comments_df = pd.read_xml(COMMENTS_XML_PATH)
    
    # Return the DataFrame
    return comments_df


def load_posts_data():
    """
    Loads the posts data from the XML file and returns it as a pandas DataFrame.

    This method reads the XML file located at the path specified by 
    `POSTS_XML_PATH` in the Constants module, and returns it as a DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing the posts data.
    """
    # Load the XML data into a pandas DataFrame
    posts_df = pd.read_xml(POSTS_XML_PATH)
    
    # Return the DataFrame
    return posts_df



