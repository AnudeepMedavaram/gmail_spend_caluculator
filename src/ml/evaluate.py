from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

from src.ml.classifier import train_classifier, predict_classifier
from src.ml.train import synthetic_training_data


def evaluate_baseline() -> None:
    """Evaluate the ML baseline on a held-out synthetic test split."""

    texts, labels = synthetic_training_data()
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=labels,
    )

    vectorizer, model = train_classifier(
        train_texts,
        train_labels,
    )
    predictions, _ = predict_classifier(
        vectorizer,
        model,
        test_texts,
    )

    print("ML baseline evaluation")
    print(f"Training examples: {len(train_texts)}")
    print(f"Test examples: {len(test_texts)}")
    print(f"Accuracy: {accuracy_score(test_labels, predictions):.3f}")
    print(
        "Precision: "
        f"{precision_score(test_labels, predictions, pos_label='transaction', zero_division=0):.3f}"
    )
    print(
        "Recall: "
        f"{recall_score(test_labels, predictions, pos_label='transaction', zero_division=0):.3f}"
    )
    print(
        "F1 score: "
        f"{f1_score(test_labels, predictions, pos_label='transaction', zero_division=0):.3f}"
    )
    print("Labels: non_transaction, transaction")
    print("Confusion matrix:")
    print(confusion_matrix(test_labels, predictions, labels=["non_transaction", "transaction"]))
    print("Evaluation uses synthetic data only; no comparison with the rule-based classifier is claimed.")


if __name__ == "__main__":
    evaluate_baseline()