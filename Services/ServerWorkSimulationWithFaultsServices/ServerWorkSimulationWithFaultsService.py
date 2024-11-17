import random
from typing import List, Optional
import numpy as np
import pandas as pd
from sklearn.linear_model import SGDClassifier
from scipy.sparse import csr_matrix, hstack
import weakref
from threading import Event
from Services.FaultSimulationServices.FaultPickerService import pick_a_server_fault
import gc


class FaultSimulator:
    def __init__(self):
        self._stop_event = Event()
        self._models = {}
        self._last_faulty_server = None
        self._fault_counts = {}

    def cleanup(self):
        self._stop_event.set()
        for model_key in list(self._models.keys()):
            del self._models[model_key]
        self._models.clear()
        gc.collect()

    def group_similar_comments(self, comments: pd.DataFrame) -> np.ndarray:
        """
        Groups similar comments using SGDClassifier with proper sparse matrix handling.
        """
        if not isinstance(comments, pd.DataFrame):
            raise ValueError("Comments must be a pandas DataFrame")

        try:
            # Create sparse features properly
            scores = csr_matrix(comments['Score'].values.reshape(-1, 1))
            user_ids = csr_matrix(comments['UserId'].values.reshape(-1, 1))
            features = hstack([scores, user_ids], format='csr')

            labels = comments['PostId'].values

            # Initialize classifier
            sgd_classifier = SGDClassifier(
                loss='log_loss',
                max_iter=100,
                tol=1e-3,
                random_state=42,
                learning_rate='optimal'
            )

            self._models['sgd_classifier'] = weakref.ref(sgd_classifier)

            # Train in mini-batches
            batch_size = 1000
            n_samples = features.shape[0]  # Use shape property for sparse matrix

            for i in range(0, n_samples, batch_size):
                end_idx = min(i + batch_size, n_samples)
                batch_features = features[i:end_idx]
                batch_labels = labels[i:end_idx]

                if i == 0:  # First batch
                    sgd_classifier.partial_fit(
                        batch_features,
                        batch_labels,
                        classes=np.unique(labels)
                    )
                else:  # Subsequent batches
                    sgd_classifier.partial_fit(batch_features, batch_labels)

            # Predict in batches
            grouped_comments = np.zeros(n_samples, dtype=np.int32)
            for i in range(0, n_samples, batch_size):
                end_idx = min(i + batch_size, n_samples)
                batch_features = features[i:end_idx]
                grouped_comments[i:end_idx] = sgd_classifier.predict(batch_features)

            return grouped_comments

        finally:
            gc.collect()

    def predict_best_comment(self,
                             posts: pd.DataFrame,
                             comments: pd.DataFrame) -> Optional[int]:
        """
        Predicts the best comment using SGDClassifier with proper sparse matrix handling.
        """
        try:
            # Create sparse feature matrix
            features = csr_matrix(comments['Score'].values.reshape(-1, 1))
            n_samples = features.shape[0]  # Use shape property for sparse matrix

            # Create binary target
            median_id = posts['Id'].median()
            target = (posts['Id'].values > median_id).astype(np.int32)

            sgd_classifier = SGDClassifier(
                loss='log_loss',
                max_iter=100,
                tol=1e-3,
                random_state=42,
                learning_rate='optimal'
            )

            self._models['comment_predictor'] = weakref.ref(sgd_classifier)

            # Train in mini-batches
            batch_size = 1000
            unique_classes = np.unique(target)

            for i in range(0, n_samples, batch_size):
                end_idx = min(i + batch_size, n_samples)
                batch_features = features[i:end_idx]
                batch_target = target[i:end_idx]

                if i == 0:  # First batch
                    sgd_classifier.partial_fit(
                        batch_features,
                        batch_target,
                        classes=unique_classes
                    )
                else:  # Subsequent batches
                    sgd_classifier.partial_fit(batch_features, batch_target)

            # Predict probabilities in batches
            all_probs = np.zeros(n_samples)
            for i in range(0, n_samples, batch_size):
                end_idx = min(i + batch_size, n_samples)
                batch_features = features[i:end_idx]
                probs = sgd_classifier.predict_proba(batch_features)
                all_probs[i:end_idx] = probs[:, 1]

            best_comment_idx = np.argmax(all_probs)
            return comments.iloc[best_comment_idx].Id

        finally:
            gc.collect()

    def handle_fault(self,
                     users: pd.DataFrame,
                     comments: pd.DataFrame,
                     posts: pd.DataFrame,
                     servers: List,
                     grouped_comments: np.ndarray) -> None:
        """
        Handles a server fault with improved fault distribution and memory management.
        """
        try:
            fault = pick_a_server_fault(posts)
            if fault.empty:
                return

            # Initialize fault counts if not exists
            for server in servers:
                if server not in self._fault_counts:
                    self._fault_counts[server] = 0

            # Select server ensuring fair distribution
            available_servers = [s for s in servers if self._fault_counts[s] == min(self._fault_counts.values())]
            selected_server = random.choice(available_servers)

            # Update fault count and add fault
            selected_server.dodaj_otkaz(int(fault["Id"].iloc[0]))

            predicted_comment = self.predict_best_comment(posts, comments)

            if predicted_comment is not None:
                comment_mask = comments['Id'] == predicted_comment
                user_id = comments.loc[comment_mask, 'UserId'].iloc[0]
                user_mask = users['AccountId'] == user_id
                user_name = users.loc[user_mask, 'DisplayName'].iloc[0]
                print(f"Fault resolved! Best comment by user: {user_name}")
            else:
                print("Fault couldn't be resolved right now.")

        except Exception as e:
            print(f"Error handling fault: {str(e)}")
        finally:
            gc.collect()