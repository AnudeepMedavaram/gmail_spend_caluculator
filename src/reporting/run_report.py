from src.analysis.aggregator import build_spending_summary
from src.analysis.analysis import build_insights
from src.reporting.report import generate_report


def main():

    print(
        "\n========== PHASE 6: REPORTING =========="
    )

    # --------------------------------------------------
    # Smoke-test data
    #
    # We use this because the current 20-email dataset
    # contains no transaction emails.
    # --------------------------------------------------

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
        {
            "merchant": "Amazon",
            "amount": 25.00,
            "currency": "USD",
            "date": "2026-08-30",
            "category": "Shopping",
        },
    ]

    summary = build_spending_summary(
        transactions
    )

    analysis = build_insights(
        transactions,
        summary,
    )

    insights = analysis.get(
        "insights",
        [],
    )

    report = generate_report(
        summary,
        insights,
    )

    print(report)

    print(
        "\nPhase 6 reporting completed."
    )


if __name__ == "__main__":
    main()