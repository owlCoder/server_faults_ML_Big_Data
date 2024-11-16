from Services.DataImporterServices.PostsImporterService import load_posts_data
from Services.DataImporterServices.UsersImporterService import load_users_data
from Services.DataPreprocessServices.PostsDataPreprocessService import preprocess_posts_data
from Services.DataPreprocessServices.UserDataPreprocessService import preprocess_users_data

# Load and preprocess users data
users_df = load_users_data()
prepared_users = preprocess_users_data(users_df)

# Extract reputable user IDs
reputable_user_ids = prepared_users['AccountId'].tolist()

# Load posts data
posts_df = load_posts_data()

# Preprocess posts to filter by reputable users and PostTypeId
filtered_posts = preprocess_posts_data(posts_df, reputable_user_ids)

print(posts_df)
# Display the preprocessed posts
print(filtered_posts)
