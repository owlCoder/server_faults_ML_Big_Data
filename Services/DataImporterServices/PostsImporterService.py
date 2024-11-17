import pandas as pd
from xml.etree.ElementTree import iterparse
from Domain.Constants.XmlPaths import POSTS_XML_PATH

def load_posts_data():
    """
    Loads and processes large Posts XML files using iterative parsing.

    This method reads Posts XML files iteratively to handle large datasets efficiently
    and returns the combined DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing the combined posts data.
    """
    # Initialize an empty list to store parsed records
    all_posts_data = []

    # Iterate through multiple XML files
    for i in range(0, 1):
        xml_file_path = POSTS_XML_PATH.format(i)

        # Parse XML iteratively
        for event, element in iterparse(xml_file_path, events=("end",)):
            # Process only 'row' elements
            if element.tag == "row":
                # Extract attributes as a dictionary
                row_data = element.attrib

                # Append the dictionary to the list
                all_posts_data.append(row_data)

                # Clear the element to free memory
                element.clear()

    # Convert the list of dictionaries into a DataFrame
    posts_df = pd.DataFrame(all_posts_data)

    return posts_df
