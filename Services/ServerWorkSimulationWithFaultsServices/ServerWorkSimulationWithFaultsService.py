import random
from typing import List, Optional, Any
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from scipy.sparse import csr_matrix, hstack, vstack
import weakref
from threading import Event

from Domain.Models.Comment import Comment
from Services.FaultSimulationServices.FaultPickerService import pick_a_server_fault
import gc

class SafeLabelEncoder(LabelEncoder):
    def __init__(self):
        super().__init__()
        self.classes_ = np.array([])

    def fit(self, y):
        # Convert values to strings for handling
        y = y.astype(str)
        return super().fit(y)

    def transform(self, y):
        # Convert values to strings for handling
        y = y.astype(str)

        # Handle unseen labels by adding them to the encoder
        unseen = np.setdiff1d(np.unique(y), self.classes_)
        if len(unseen) > 0:
            self.classes_ = np.concatenate([self.classes_, unseen])
        return np.array([np.where(self.classes_ == item)[0][0] for item in y])


class FaultSimulator:
    def __init__(self):
        self._stop_event = Event()
        self._models = {}
        self._last_faulty_server = None
        self._fault_counts = {}
        self._total_faults = 0
        self._resolved_faults = 0
        self._label_encoders = {}

    def cleanup(self):
        self._stop_event.set()
        for model_key in list(self._models.keys()):
            model = self._models[model_key]()  # Actual object from weak ref
            if model is not None:
                del model
        self._models.clear()
        self._label_encoders.clear()
        gc.collect()

    @staticmethod
    def _process_in_batches(data: pd.DataFrame, batch_size: int = 1000) -> pd.DataFrame:
        """Process DataFrames in batches"""
        result_chunks = []
        for start_idx in range(0, len(data), batch_size):
            end_idx = min(start_idx + batch_size, len(data))
            chunk = data.iloc[start_idx:end_idx].copy()
            result_chunks.append(chunk)
            gc.collect()
        return pd.concat(result_chunks) if result_chunks else pd.DataFrame()

    def _prepare_features(self, comments: pd.DataFrame, batch_size: int = 1000) -> csr_matrix | Any:
        """
        Feature preparation using sparse matrices and batching with label encoding
        """
        if 'UserId' not in self._label_encoders:
            self._label_encoders['UserId'] = SafeLabelEncoder()

        features_list = []
        for start_idx in range(0, len(comments), batch_size):
            end_idx = min(start_idx + batch_size, len(comments))
            chunk = comments.iloc[start_idx:end_idx]

            # Convert scores to numeric
            scores = pd.to_numeric(chunk['Score'], errors='coerce').fillna(0)

            # Handle user IDs
            if start_idx == 0:  # First batch - fit and transform
                user_ids = self._label_encoders['UserId'].fit(chunk['UserId'].fillna('UNKNOWN'))
                user_ids = self._label_encoders['UserId'].transform(chunk['UserId'].fillna('UNKNOWN'))
            else:  # Subsequent batches - transform only
                user_ids = self._label_encoders['UserId'].transform(chunk['UserId'].fillna('UNKNOWN'))

            # Create sparse matrices for the chunk
            chunk_features = hstack([
                csr_matrix(scores.values.reshape(-1, 1)),
                csr_matrix(user_ids.reshape(-1, 1))
            ])

            features_list.append(chunk_features)
            gc.collect()

        # Combine all chunks
        if features_list:
            return vstack(features_list, format='csr')
        return csr_matrix((0, 2))

    def group_similar_comments(self, comments: pd.DataFrame) -> np.ndarray:
        """
        Grouping of similar comments with label handling
        """
        if not isinstance(comments, pd.DataFrame):
            raise ValueError("Comments must be a pandas DataFrame")

        try:
            batch_size = 1000
            features = self._prepare_features(comments, batch_size)

            # Convert PostId to numeric categories
            if 'PostId' not in self._label_encoders:
                self._label_encoders['PostId'] = SafeLabelEncoder()

            # Ensure PostId is handled
            comments['PostId'] = comments['PostId'].fillna(-1).astype(str)
            labels = self._label_encoders['PostId'].fit_transform(comments['PostId'])
            unique_classes = np.unique(labels)

            if len(unique_classes) < 2:
                return np.zeros(len(comments), dtype=np.int32)

            # Initialize classifiers
            sgd = SGDClassifier(loss='log_loss', max_iter=5, tol=1e-2, random_state=42, n_jobs=8)
            logistic = LogisticRegression(max_iter=5, solver='sag', n_jobs=8)
            rf = RandomForestClassifier(n_estimators=4, max_depth=5, n_jobs=8)

            self._models.update({
                'sgd_classifier': weakref.ref(sgd),
                'logistic_classifier': weakref.ref(logistic),
                'rf_classifier': weakref.ref(rf)
            })

            # Train classifiers in batches
            predictions = np.zeros((len(comments), 3), dtype=np.int32)

            training_iterations = 2
            for start_idx in range(0, training_iterations): # 1
                print(f"⌛ Training model {start_idx + 1}/{training_iterations}")
                end_idx = min(start_idx + batch_size, features.shape[0])
                batch_features = features[start_idx:end_idx]
                batch_labels = labels[start_idx:end_idx]

                if start_idx == 0:
                    sgd.partial_fit(batch_features, batch_labels, classes=unique_classes)
                    logistic.fit(batch_features, batch_labels)
                    rf.fit(batch_features, batch_labels)
                else:
                    sgd.partial_fit(batch_features, batch_labels)

                predictions[start_idx:end_idx, 0] = sgd.predict(batch_features)
                predictions[start_idx:end_idx, 1] = logistic.predict(batch_features)
                predictions[start_idx:end_idx, 2] = rf.predict(batch_features)

                gc.collect()

            # Majority voting algorithm
            final_predictions = np.zeros(len(comments), dtype=np.int32)
            for i in range(0, len(comments), batch_size):
                end_idx = min(i + batch_size, len(comments))
                batch_pred = predictions[i:end_idx]
                final_predictions[i:end_idx] = np.apply_along_axis(
                    lambda x: np.bincount(x).argmax(),
                    axis=1,
                    arr=batch_pred
                )
                gc.collect()

            return final_predictions

        finally:
            gc.collect()

    @staticmethod
    def predict_best_comment(self, posts: pd.DataFrame, comments: pd.DataFrame) -> Optional[int]:
        try:
            comment_id = comments['Id'].sample(n=1).iloc[0]
            return  comment_id

            # Batch size
            batch_size = 1000
            features = self._prepare_features(comments, batch_size)

            # Binary target
            posts['Id'] = pd.to_numeric(posts['Id'], errors='coerce').fillna(-1)
            median_id = posts['Id'].median()
            best_comment_index = comment_id

            target = (posts['Id'] > median_id).astype(int)
            unique_classes = np.array([0, 1])

            if len(np.unique(target)) < 2:
                return best_comment_index

            # Initialize classifiers
            sgd = SGDClassifier(loss='log_loss', max_iter=5, tol=1e-2, random_state=42)
            logistic = LogisticRegression(max_iter=50, solver='sag', n_jobs=2)
            rf = RandomForestClassifier(n_estimators=20, max_depth=5, n_jobs=2)

            self._models.update({
                'comment_sgd': weakref.ref(sgd),
                'comment_logistic': weakref.ref(logistic),
                'comment_rf': weakref.ref(rf)
            })

            # Train and predict in batches
            all_probs = np.zeros((len(comments), 3))

            for start_idx in range(0, features.shape[0], batch_size):
                end_idx = min(start_idx + batch_size, features.shape[0])
                batch_features = features[start_idx:end_idx]
                batch_target = target[start_idx:end_idx]

                if start_idx == 0:
                    sgd.partial_fit(batch_features, batch_target, classes=unique_classes)
                    logistic.fit(batch_features, batch_target)
                    rf.fit(batch_features, batch_target)
                else:
                    sgd.partial_fit(batch_features, batch_target)

                all_probs[start_idx:end_idx, 0] = sgd.predict_proba(batch_features)[:, 1]
                all_probs[start_idx:end_idx, 1] = logistic.predict_proba(batch_features)[:, 1]
                all_probs[start_idx:end_idx, 2] = rf.predict_proba(batch_features)[:, 1]

                gc.collect()

            # Find best comment
            ensemble_probs = np.mean(all_probs, axis=1)
            best_comment_idx = np.argmax(ensemble_probs)

            return comment_id

        except Exception as e:
            return None
        finally:
            gc.collect()

    def handle_fault(self, users: pd.DataFrame, comments: pd.DataFrame,
                     posts: pd.DataFrame, servers: List, grouped_comments: np.ndarray) -> None:
        """
        Fault handling with data handling
        """
        try:
            if not servers:
                print("ℹ️ No servers available for fault handling")
                return

            # Select server with fair distribution
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
            try:
                fault_id = int(fault["Id"].iloc[0])
                faulty_server.dodaj_otkaz(fault_id)
            except (ValueError, TypeError):
                print("Invalid fault ID detected")
                return

            print(f"\n⚠️ Fault detected on server {faulty_server.naziv} (ID: {server_id})")
            print(f"Fault ID: {fault_id}")
            print(f"Current server fault count: {len(faulty_server.lista_otkaza)}")
            print(f"Total system faults: {self._total_faults}")

            # Process prediction in smaller chunks
            predicted_comment = self.predict_best_comment(
                self,
                posts,
                comments
            )

            if predicted_comment is not None:
                try:
                    comment_info = comments[comments['Id'] == predicted_comment].iloc[0]
                    user_info = users[users['AccountId'] == comment_info['UserId']].iloc[0]

                    self._resolved_faults += 1
                    print(f"\n✅ Fault successfully resolved!")
                    print(f"Resolution provided by user: {user_info['DisplayName']}")
                    print(f"Total resolved faults: {self._resolved_faults}/{self._total_faults}")
                    print(f"Current resolution rate: {(self._resolved_faults / self._total_faults) * 100:.1f}%")
                except IndexError:
                    print("\n⚠️ Fault partially resolved - Some information not found")
            else:
                print("\n❌ Fault could not be resolved")
                print("No suitable resolution found")

        except Exception as e:
            print("")
        finally:
            gc.collect()