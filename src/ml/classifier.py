from functools import lru_cache
from pathlib import Path
import pickle
from typing import Sequence

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


LABELS = ("non_transaction", "transaction")
MODEL_FILE = Path("data/ml_artifacts/transaction_classifier.pkl")


def train_classifier(
    texts: Sequence[str],
    labels: Sequence[str],
) -> tuple[TfidfVectorizer, LogisticRegression]:
    """Train the baseline: raw text -> TF-IDF -> Logistic Regression."""

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        stop_words="english",
    )
    features = vectorizer.fit_transform(texts)

    model = LogisticRegression(
        max_iter=1000,
        random_state=42,
    )
    model.fit(features, labels)

    return vectorizer, model


def predict_classifier(
    vectorizer: TfidfVectorizer,
    model: LogisticRegression,
    texts: Sequence[str],
) -> tuple[list[str], list[float]]:
    """Return predicted classes and transaction probabilities."""

    features = vectorizer.transform(texts)
    predictions = model.predict(features).tolist()
    probabilities = model.predict_proba(features)
    transaction_index = list(model.classes_).index("transaction")
    transaction_probabilities = probabilities[:, transaction_index].tolist()

    return predictions, transaction_probabilities


@lru_cache(maxsize=1)
def load_saved_classifier() -> tuple[TfidfVectorizer, LogisticRegression] | None:
    """Load the optional local artifact, returning None when unavailable."""

    if not MODEL_FILE.exists():
        return None

    try:
        with MODEL_FILE.open("rb") as file:
            artifact = pickle.load(file)

        return artifact["vectorizer"], artifact["model"]

    except (AttributeError, KeyError, OSError, EOFError, pickle.UnpicklingError):
        return None


def predict_saved_classifier(text: str) -> tuple[str, float] | None:
    """Predict with the optional artifact without making it pipeline-critical."""

    artifact = load_saved_classifier()
    if artifact is None:
        return None

    vectorizer, model = artifact
    predictions, probabilities = predict_classifier(
        vectorizer,
        model,
        [text],
    )

    return predictions[0], probabilities[0]