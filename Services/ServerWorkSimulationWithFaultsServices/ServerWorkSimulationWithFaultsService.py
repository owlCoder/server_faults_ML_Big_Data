import random
from typing import List, Optional
from datetime import datetime
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
        self._total_faults = 0
        self._resolved_faults = 0

    def cleanup(self):
        self._stop_event.set()
        for model_key in list(self._models.keys()):
            del self._models[model_key]
        self._models.clear()
        gc.collect()

    def group_similar_comments(self, comments: pd.DataFrame) -> np.ndarray:
        """
        Groups similar comments using SGDClassifier with sparse matrix handling.
        """
        if not isinstance(comments, pd.DataFrame):
            raise ValueError("Comments must be a pandas DataFrame")

        try:
            # Create sparse features
            scores = csr_matrix(comments['Score'].values.reshape(-1, 1))
            user_ids = csr_matrix(comments['UserId'].values.reshape(-1, 1))

            # TODO NE RADI, NE ZNAM
            return comments


            features = hstack([scores, user_ids], format='csr')

            labels = comments['PostId'].values

            # Initialize classifier
            sgd_classifier = SGDClassifier(
                loss='log_loss',
                max_iter=10,
                tol=1e-1,
                random_state=42,
                learning_rate='optimal'
            )

            self._models['sgd_classifier'] = weakref.ref(sgd_classifier)

            # Train in mini-batches
            batch_size = 1000
            n_samples = features.shape[0]

            for i in range(0, n_samples, batch_size):
                end_idx = min(i + batch_size, n_samples)
                batch_features = features[i:end_idx]
                batch_labels = labels[i:end_idx]

                if i == 0:
                    sgd_classifier.partial_fit(
                        batch_features,
                        batch_labels,
                        classes=np.unique(labels)
                    )
                else:
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
        Predicts the best comment using SGDClassifier with sparse matrix handling.
        """
        try:
            if comments.empty or posts.empty:
                return None

            # Create sparse feature matrix
            features = csr_matrix(comments['Score'].values.reshape(-1, 1))
            n_samples = features.shape[0]

            # Create binary target
            median_id = posts['Id'].median()
            target = (posts['Id'].values > median_id)

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

                if i == 0:
                    sgd_classifier.partial_fit(
                        batch_features,
                        batch_target,
                        classes=unique_classes
                    )
                else:
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
            if not servers:
                print("No servers available for fault handling")
                return

            # Select server = fair distribution
            fault = pick_a_server_fault(posts)
            if fault is None or fault.empty:
                print("No fault detected")
                return

            random.seed(datetime.now().timestamp())
            faulty_server_index = random.randint(0, len(servers) - 1)
            faulty_server = servers[faulty_server_index]

            # Update fault tracking
            self._total_faults += 1
            server_id = faulty_server.id_servera
            self._fault_counts[server_id] = self._fault_counts.get(server_id, 0) + 1

            # Add fault to server
            fault_id = int(fault["Id"].iloc[0])
            faulty_server.dodaj_otkaz(fault_id)

            print(f"\n⚠️ Fault detected on server {faulty_server.naziv} (ID: {server_id})")
            print(f"Fault ID: {fault_id}")
            print(f"Current server fault count: {len(faulty_server.lista_otkaza)}")
            print(f"Total system faults: {self._total_faults}")

            predicted_comment = self.predict_best_comment(posts, comments)

            if predicted_comment is not None:
                comment_mask = comments['Id'] == predicted_comment
                if any(comment_mask):
                    user_id = comments.loc[comment_mask, 'UserId'].iloc[0]
                    user_mask = users['AccountId'] == user_id
                    if any(user_mask):
                        user_name = users.loc[user_mask, 'DisplayName'].iloc[0]
                        self._resolved_faults += 1
                        print(f"\n✅ Fault successfully resolved!")
                        print(f"Resolution provided by user: {user_name}")
                        print(f"Total resolved faults: {self._resolved_faults}/{self._total_faults}")
                        print(f"Current resolution rate: {(self._resolved_faults / self._total_faults) * 100:.1f}%")
                    else:
                        print("\n⚠️ Fault partially resolved - User not found")
                else:
                    print("\n⚠️ Fault partially resolved - Comment not found")
            else:
                print("\n❌ Fault could not be resolved")
                print("No suitable resolution found in available comments")

        except Exception as e:
            print(e)
        finally:
            gc.collect()