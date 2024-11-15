import pandas as pd
from Domain.Constants.XmlPaths import USERS_XML_PATH

def load_users_data():
    """
    Loads the users data from the XML file and returns it as a pandas DataFrame.

    This method reads the XML file located at the path specified by 
    `USERS_XML_PATH` in the Constants module, and returns it as a DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing the users data.
    """
    # Load the XML data into a pandas DataFrame
    users_df = pd.read_xml(USERS_XML_PATH)
    
    # Return the DataFrame
    return users_df