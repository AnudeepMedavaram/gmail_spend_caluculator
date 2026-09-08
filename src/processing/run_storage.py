from src.processing.storage import (
    save_transactions,
    load_transactions,
)


def main():
    """
    Run a basic transaction storage test.
    """

    print(
        "========== TRANSACTION STORAGE =========="
    )

    test_transactions = [
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

    print(
        f"Saving {len(test_transactions)} transactions..."
    )

    save_transactions(
        test_transactions
    )

    loaded_transactions = load_transactions()

    print(
        f"Loaded {len(loaded_transactions)} transactions."
    )

    for transaction in loaded_transactions:
        print(
            f"  {transaction}"
        )

    print(
        "\nStorage test completed."
    )

    print(
        "=========================================="
    )


if __name__ == "__main__":
    main()