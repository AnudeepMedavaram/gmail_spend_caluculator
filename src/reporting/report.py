from typing import Dict, List


def generate_report(
    summary: Dict,
    insights: List[str],
) -> str:
    """
    Generate a human-readable spending report.

    This is intentionally simple for the Phase 6
    reporting baseline.
    """

    total_spending = summary.get(
        "total_spending",
        0.0,
    )

    transaction_count = summary.get(
        "transaction_count",
        0,
    )

    by_category = summary.get(
        "by_category",
        {},
    )

    by_merchant = summary.get(
        "by_merchant",
        {},
    )

    by_month = summary.get(
        "by_month",
        {},
    )

    average_transaction = (
        total_spending / transaction_count
        if transaction_count > 0
        else 0.0
    )

    largest_transaction = summary.get(
        "largest_transaction",
    )

    report_lines = []

    report_lines.append(
        "\n========== SPENDING REPORT =========="
    )

    report_lines.append(
        f"\nTotal Spending: "
        f"{total_spending:.2f}"
    )

    report_lines.append(
        f"Transactions: "
        f"{transaction_count}"
    )

    report_lines.append(
        f"Average Transaction: "
        f"{average_transaction:.2f}"
    )

    if largest_transaction:

        merchant = largest_transaction.get(
            "merchant",
            "Unknown",
        )

        amount = largest_transaction.get(
            "amount",
            0.0,
        )

        report_lines.append(
            f"Largest Transaction: "
            f"{merchant} ({amount:.2f})"
        )

    # --------------------------------------------------
    # CATEGORY
    # --------------------------------------------------

    report_lines.append(
        "\n---------- BY CATEGORY ----------"
    )

    if by_category:

        for category, amount in sorted(
            by_category.items(),
            key=lambda item: item[1],
            reverse=True,
        ):

            report_lines.append(
                f"{category}: "
                f"{amount:.2f}"
            )

    else:

        report_lines.append(
            "No category data."
        )

    # --------------------------------------------------
    # MERCHANT
    # --------------------------------------------------

    report_lines.append(
        "\n---------- BY MERCHANT ----------"
    )

    if by_merchant:

        for merchant, amount in sorted(
            by_merchant.items(),
            key=lambda item: item[1],
            reverse=True,
        ):

            report_lines.append(
                f"{merchant}: "
                f"{amount:.2f}"
            )

    else:

        report_lines.append(
            "No merchant data."
        )

    # --------------------------------------------------
    # MONTH
    # --------------------------------------------------

    report_lines.append(
        "\n---------- MONTHLY ----------"
    )

    if by_month:

        for month, amount in sorted(
            by_month.items()
        ):

            report_lines.append(
                f"{month}: "
                f"{amount:.2f}"
            )

    else:

        report_lines.append(
            "No monthly data."
        )

    # --------------------------------------------------
    # INSIGHTS
    # --------------------------------------------------

    report_lines.append(
        "\n---------- INSIGHTS ----------"
    )

    if insights:

        for insight in insights:

            report_lines.append(
                f"• {insight}"
            )

    else:

        report_lines.append(
            "No insights available."
        )

    report_lines.append(
        "\n===================================="
    )

    return "\n".join(report_lines)