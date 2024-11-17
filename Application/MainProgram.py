import threading
import time

from Domain.Models.Server import Server
from Presentation.ServerStatusShow.ServerStatusUI import show_servers_status
from Services.DataImporterServices.CommentsImporterService import load_comments_data
from Services.DataImporterServices.PostsImporterService import load_posts_data
from Services.DataImporterServices.UsersImporterService import load_users_data
from Services.DataPreprocessServices.CommentsDataPreprocessService import preprocess_comments_data
from Services.DataPreprocessServices.PostsDataPreprocessService import preprocess_posts_data
from Services.DataPreprocessServices.UserDataPreprocessService import preprocess_users_data

# Load and data from XML
""" 
users_df = load_users_data()
posts_df = load_posts_data()
comments_df = load_comments_data()

# Preprocess Data
users_data = preprocess_users_data(users_df)
reputable_user_ids = users_data['AccountId'].tolist() # Extract reputable user IDs
posts_data = preprocess_posts_data(posts_df, reputable_user_ids)
comments_data = preprocess_comments_data(comments_df)
"""

# Make cluster of 10 Servers
servers_cluster = [
    Server("Lenovo ThinkCentre MQ 7i"), Server("Dell OptiFlex 70D"), Server("HP OmniRun 2V"),
    Server("Lenovo ThinkStation P350"), Server("Dell PowerEdge T40"),
    Server("HP ProLant DL360"), Server("Lenovo ThinkEdge SE50"), Server("Dell Latitude 7520"),
    Server("HP ZBook Firefly G9"), Server("Lenovo Legion T5 28IMB05")
]

# Show server statuses on every 5 seconds
threading.Thread(target=lambda: [show_servers_status(servers_cluster) or time.sleep(15) for _ in iter(int, 1)]).start()

# Run simulation
while 1:
    print("simulation in progress")
    time.sleep(10)
    # todo dodaj simulaciju i neka prosledi sva 3 DF