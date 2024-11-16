import pandas as pd
from Domain.Constants.XmlPaths import USERS_XML_PATH

def load_users_data():
    """
    Loads the data from multiple Users XML files and returns them as a single pandas DataFrame.

    This method reads multiple Users XML files (e.g., Users-1.xml, Users-2.xml, ...)
    and concatenates them into one DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing all the users data combined.
    """
    # Initialize an empty list to store DataFrames
    all_users_data = []

    # Read multiple Users XML files
    for i in range(1, 2):
        users_df = pd.read_xml(USERS_XML_PATH.format(i))
        all_users_data.append(users_df)

    # Concatenate all the data into a single DataFrame
    combined_users_df = pd.concat(all_users_data, ignore_index=True)

    # Return the combined DataFrame
    return combined_users_df