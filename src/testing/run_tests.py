import json
from pathlib import Path

from src.models.email import Email
from src.processing.classifier import classify_email
from src.processing.extractor import extract_transaction
from src.processing.validator import validate_transaction
from src.processing import storage
from src.analysis.aggregator import build_spending_summary
from src.analysis.analysis import build_insights


TEST_OUTPUT = Path("data/processed/test_transactions.jsonl")


def test_classifier():
    print("\n[TEST 1] Classifier")

    email = Email(
        message_id="test-001",
        thread_id="thread-001",
        sender="Amazon <order@amazon.com>",
        recipient="user@example.com",
        subject="Your order is confirmed",
        date="2026-08-28",
        body="Payment successful. Total paid: $49.99.",
        snippet="Payment successful. Total paid: $49.99.",
    )

    result = classify_email(email)

    assert result.is_transaction_candidate is True

    print("PASS - transaction email classified as candidate")


def test_extractor():
    print("\n[TEST 2] Extractor")

    email = Email(
        message_id="test-002",
        thread_id="thread-002",
        sender="Amazon <order@amazon.com>",
        recipient="user@example.com",
        subject="Order confirmed",
        date="2026-08-28",
        body="Your order was confirmed. Total paid: $49.99 USD.",
        snippet="Total paid: $49.99 USD.",
    )

    transaction = extract_transaction(email)

    assert transaction is not None

    print("Extracted:", transaction)

    assert transaction.amount == 49.99
    assert transaction.currency == "USD"

    print("PASS - transaction fields extracted")


def test_validator():
    print("\n[TEST 3] Validator")

    valid_transaction = {
        "merchant": "Amazon",
        "amount": 49.99,
        "currency": "USD",
        "date": "2026-08-28",
    }

    result = validate_transaction(
        valid_transaction
    )

    assert result.is_valid is True
    assert result.errors == []

    print("PASS - valid transaction accepted")


def test_storage():
    print("\n[TEST 4] Storage")

    transactions = [
        {
            "merchant": "Amazon",
            "amount": 49.99,
            "currency": "USD",
            "date": "2026-08-28",
        },
        {
            "merchant": "Netflix",
            "amount": 15.99,
            "currency": "USD",
            "date": "2026-08-29",
        },
    ]

    original_output = storage.TRANSACTIONS_FILE
    storage.TRANSACTIONS_FILE = TEST_OUTPUT

    try:
        storage.save_transactions(
            transactions
        )

        loaded = storage.load_transactions()

    finally:
        storage.TRANSACTIONS_FILE = original_output

    assert len(loaded) == 2
    assert loaded[0]["merchant"] == "Amazon"

    print("PASS - transactions saved and loaded")


def test_aggregation():
    print("\n[TEST 5] Aggregation")

    transactions = [
        {
            "merchant": "Amazon",
            "amount": 49.99,
            "currency": "USD",
            "date": "2026-08-28",
            "category": "Shopping",
        },
        {
            "merchant": "Netflix",
            "amount": 15.99,
            "currency": "USD",
            "date": "2026-08-29",
            "category": "Entertainment",
        },
    ]

    summary = build_spending_summary(
        transactions
    )

    assert summary["total_spending"] == 65.98
    assert summary["transaction_count"] == 2

    print("PASS - spending aggregation works")


def test_analysis():
    print("\n[TEST 6] Analysis")

    transactions = [
        {
            "merchant": "Amazon",
            "amount": 49.99,
            "currency": "USD",
            "date": "2026-08-28",
            "category": "Shopping",
        },
        {
            "merchant": "Netflix",
            "amount": 15.99,
            "currency": "USD",
            "date": "2026-08-29",
            "category": "Entertainment",
        },
    ]

    summary = build_spending_summary(
        transactions
    )

    analysis = build_insights(
        transactions,
        summary,
    )

    assert analysis["highest_merchant"] == "Amazon"

    print("PASS - spending analysis works")


def cleanup():
    if TEST_OUTPUT.exists():
        TEST_OUTPUT.unlink()


def main():
    print("\n========== PHASE 9: TESTING ==========")

    try:
        test_classifier()
        test_extractor()
        test_validator()
        test_storage()
        test_aggregation()
        test_analysis()

        print("\n======================================")
        print("PHASE 9 TESTS PASSED")
        print("All core components are working.")
        print("======================================")

    except AssertionError as error:
        print("\n======================================")
        print("PHASE 9 TEST FAILED")
        print("======================================")
        print(error)
        raise

    finally:
        cleanup()


if __name__ == "__main__":
    main()