from src.processing.storage import load_transactions
from src.analysis.aggregator import build_spending_summary


def main():
    print("\n========== PHASE 5: SPENDING AGGREGATION ==========")

    transactions = load_transactions()

    print(
        f"Loaded {len(transactions)} transactions."
    )

    if not transactions:
        print(
            "\nNo stored transactions found."
        )
        print(
            "Aggregation code is ready, but the current "
            "20-email dataset contains no transaction candidates."
        )
        print(
            "\nRunning aggregation smoke test with sample data..."
        )

        transactions = [
            {
                "merchant": "Amazon",
                "amount": 49.99,
                "currency": "USD",
                "category": "Shopping",
                "date": "2026-08-28",
            },
            {
                "merchant": "Netflix",
                "amount": 15.99,
                "currency": "USD",
                "category": "Entertainment",
                "date": "2026-08-29",
            },
            {
                "merchant": "Amazon",
                "amount": 25.00,
                "currency": "USD",
                "category": "Shopping",
                "date": "2026-08-29",
            },
        ]

    summary = build_spending_summary(
        transactions
    )

    print("\n---------- SPENDING SUMMARY ----------")

    print(
        f"Transaction count: "
        f"{summary['transaction_count']}"
    )

    print(
        f"Total spending: "
        f"{summary['total_spending']:.2f}"
    )

    print("\nBy category:")

    for category, amount in summary["by_category"].items():
        print(
            f"  {category}: {amount:.2f}"
        )

    print("\nBy merchant:")

    for merchant, amount in summary["by_merchant"].items():
        print(
            f"  {merchant}: {amount:.2f}"
        )

    print("\nBy month:")

    for month, amount in summary["by_month"].items():
        print(
            f"  {month}: {amount:.2f}"
        )

    print(
        "\n======================================"
    )


if __name__ == "__main__":
    main()