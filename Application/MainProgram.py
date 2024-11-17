from Domain.Models.Server import Server
from Services.DataImporterServices.CommentsImporterService import load_comments_data
from Services.DataImporterServices.PostsImporterService import load_posts_data
from Services.DataImporterServices.UsersImporterService import load_users_data
from Services.DataPreprocessServices.CommentsDataPreprocessService import preprocess_comments_data
from Services.DataPreprocessServices.PostsDataPreprocessService import preprocess_posts_data
from Services.DataPreprocessServices.UserDataPreprocessService import preprocess_users_data
from Services.ServerMonitorServices.ServerMonitorService import run_simulation

if __name__ == "__main__":
    # Load and preprocess data
    users_df = load_users_data()
    posts_df = load_posts_data()
    comments_df = load_comments_data()

    users_data = preprocess_users_data(users_df)
    reputable_user_ids = users_data['AccountId'].tolist()
    posts_data = preprocess_posts_data(posts_df, reputable_user_ids)
    comments_data = preprocess_comments_data(comments_df)

    # Initialize servers
    servers_cluster = [
        Server("Lenovo ThinkCentre MQ 7i"),
        Server("Dell OptiFlex 70D"),
        Server("HP OmniRun 2V"),
        Server("Lenovo ThinkStation P350"),
        Server("Dell PowerEdge T40"),
        Server("HP ProLant DL360"),
        Server("Lenovo ThinkEdge SE50"),
        Server("Dell Latitude 7520"),
        Server("HP ZBook Firefly G9"),
        Server("Lenovo Legion T5 28IMB05")
    ]

    # Run simulation with proper resource management
    run_simulation(users_data, posts_data, comments_data, servers_cluster)