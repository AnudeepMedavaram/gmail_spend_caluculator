from pathlib import Path
import pickle

from src.ml.classifier import train_classifier
from src.ml.features import email_to_text


ARTIFACT_DIR = Path("data/ml_artifacts")
MODEL_FILE = ARTIFACT_DIR / "transaction_classifier.pkl"


def synthetic_training_data() -> tuple[list[str], list[str]]:
    """Return safe, synthetic examples; no Gmail data is used for training."""

    examples = [
        ("Your order is confirmed", "Payment successful. Total paid: $49.99.", "transaction"),
        ("Receipt for your purchase", "Your card was charged INR 799.", "transaction"),
        ("Invoice generated", "Amount due for your completed order is USD 25.", "transaction"),
        ("Subscription renewed", "Your monthly payment of $12.00 was processed.", "transaction"),
        ("Payment received", "Transaction ID 12345. Amount paid: $80.", "transaction"),
        ("Your delivery is ready", "Order number 555 and total charged $42.50.", "transaction"),
        ("Purchase confirmation", "Thank you for your purchase of INR 499.", "transaction"),
        ("Debit alert", "Your account was debited USD 18 for the purchase.", "transaction"),
        ("Weekly engineering newsletter", "Read our article about testing techniques.", "non_transaction"),
        ("How to save money", "This guide explains budgeting and lower costs.", "non_transaction"),
        ("Career opportunities this week", "Explore new jobs and interview advice.", "non_transaction"),
        ("50% off annual course", "Limited time offer for online lessons.", "non_transaction"),
        ("Product launch newsletter", "Read the latest technology news and updates.", "non_transaction"),
        ("Weekend travel guide", "Our article covers the best places to visit.", "non_transaction"),
        ("System design interview tips", "Learn how to prepare for engineering interviews.", "non_transaction"),
        ("Community blog recap", "This post discusses trends, ideas, and readers.", "non_transaction"),
    ]

    texts = [email_to_text(subject, body) for subject, body, _ in examples]
    labels = [label for _, _, label in examples]
    return texts, labels


def train_and_save() -> tuple[object, object]:
    """Train on synthetic examples and save a local, ignored artifact."""

    texts, labels = synthetic_training_data()
    vectorizer, model = train_classifier(texts, labels)

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    with MODEL_FILE.open("wb") as file:
        pickle.dump(
            {
                "vectorizer": vectorizer,
                "model": model,
            },
            file,
        )

    print("ML baseline training completed.")
    print(f"Training examples: {len(texts)}")
    print(f"Features: {len(vectorizer.vocabulary_)} TF-IDF terms")
    print("Model: LogisticRegression")
    print(f"Saved local artifact: {MODEL_FILE}")

    return vectorizer, model


if __name__ == "__main__":
    train_and_save()