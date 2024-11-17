import random
from datetime import datetime
from Services.FaultSimulationServices.FaultPickerService import pick_a_server_fault
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression


def group_similar_comments(comments):
    """
    Groups similar comments using a Random Forest approach.
    """
    # Prepare the data for classification
    features = comments[['Score', 'UserId']].values
    labels = comments['PostId']

    # Train Random Forest
    rf_model = RandomForestClassifier(random_state=42)
    rf_model.fit(features, labels)

    # Predict groups of similar comments
    grouped_comments = rf_model.predict(features)

    return grouped_comments


def predict_best_comment(posts, comments, grouped_comments):
    """
    Predicts the best comment for a given post using linear regression.
    """
    # Prepare features and target for regression
    features = comments[['Score']].values
    target = posts['Id']

    # Train Linear Regression model
    lr_model = LinearRegression()
    lr_model.fit(features, target)

    # Predict best comment for each post
    predicted_post = lr_model.predict(features)

    return predicted_post

def handle_fault(users, comments, posts, servers, grouped_comments):
    """
    Handles a server fault and tries to resolve it using comment predictions.
    """
    fault = pick_a_server_fault(posts)
    random.seed(datetime.now().timestamp())
    faulty_server_index = random.randint(0, len(servers) - 1)

    # Add fault to a server's fault list
    servers[faulty_server_index].dodaj_otkaz(int(fault["Id"].iloc[0]))

    # Try to resolve the fault
    predicted_comment = predict_best_comment(posts, comments, grouped_comments)

    # Check if a solution exists
    if predicted_comment:
        # Find the comment and the user who wrote it
        solved_comment = comments.loc[comments['Id'] == predicted_comment]
        user = users.loc[users['AccountId'] == solved_comment['UserId'].iloc[0]]
        print(f"Fault resolved! Best comment by user: {user['DisplayName'].iloc[0]}")
    else:
        print("Fault couldn't be resolved right now.")


def run_simulation_with_faults(users, posts, comments, servers):
    """
    Orchestrates the fault simulation and resolution process.
    """
    # Group similar comments
    grouped_comments = group_similar_comments(comments)

    # Handle a server fault
    handle_fault(users, comments, posts, servers, grouped_comments)
