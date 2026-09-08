from src.analysis.aggregator import (
    build_spending_summary,
)

from src.analysis.analysis import (
    build_insights,
)


def main():

    print(
        "\n========== PHASE 5: SPENDING ANALYSIS =========="
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

    result = build_insights(
        transactions,
        summary,
    )

    print(
        f"\nTotal spending: "
        f"{result['total_spending']:.2f}"
    )

    print(
        f"Transaction count: "
        f"{result['transaction_count']}"
    )

    print(
        f"Highest category: "
        f"{result['highest_category']} "
        f"({result['highest_category_amount']:.2f})"
    )

    print(
        f"Highest merchant: "
        f"{result['highest_merchant']} "
        f"({result['highest_merchant_amount']:.2f})"
    )

    print(
        f"Average transaction: "
        f"{result['average_transaction']:.2f}"
    )

    largest = result["largest_transaction"]

    if largest:
        print(
            f"Largest transaction: "
            f"{largest['merchant']} "
            f"({float(largest['amount']):.2f})"
        )

    print("\nInsights:")

    for insight in result["insights"]:
        print(
            f"  - {insight}"
        )

    print(
        "\n=============================================="
    )


if __name__ == "__main__":
    main()