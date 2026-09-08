from typing import Any


def highest_spending_category(
    summary: dict[str, Any],
) -> tuple[str | None, float]:
    """
    Return the category with the highest total spending.
    """

    categories = summary.get(
        "by_category",
        {},
    )

    if not categories:
        return None, 0.0

    category, amount = max(
        categories.items(),
        key=lambda item: item[1],
    )

    return category, float(amount)


def highest_spending_merchant(
    summary: dict[str, Any],
) -> tuple[str | None, float]:
    """
    Return the merchant with the highest total spending.
    """

    merchants = summary.get(
        "by_merchant",
        {},
    )

    if not merchants:
        return None, 0.0

    merchant, amount = max(
        merchants.items(),
        key=lambda item: item[1],
    )

    return merchant, float(amount)


def largest_transaction(
    transactions: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """
    Return the largest transaction by amount.
    """

    if not transactions:
        return None

    return max(
        transactions,
        key=lambda transaction: float(
            transaction.get("amount", 0) or 0
        ),
    )


def average_transaction(
    transactions: list[dict[str, Any]],
) -> float:
    """
    Calculate the average transaction amount.
    """

    if not transactions:
        return 0.0

    amounts = [
        float(
            transaction.get("amount", 0) or 0
        )
        for transaction in transactions
    ]

    return round(
        sum(amounts) / len(amounts),
        2,
    )


def build_insights(
    transactions: list[dict[str, Any]],
    summary: dict[str, Any],
) -> dict[str, Any]:
    """
    Build a simple spending intelligence report.
    """

    category, category_amount = (
        highest_spending_category(summary)
    )

    merchant, merchant_amount = (
        highest_spending_merchant(summary)
    )

    largest = largest_transaction(
        transactions
    )

    average = average_transaction(
        transactions
    )

    insights = []

    if category:
        insights.append(
            f"Highest spending category is "
            f"{category} at {category_amount:.2f}."
        )

    if merchant:
        insights.append(
            f"Highest spending merchant is "
            f"{merchant} at {merchant_amount:.2f}."
        )

    if largest:
        largest_merchant = (
            largest.get("merchant")
            or "unknown"
        )

        largest_amount = float(
            largest.get("amount", 0) or 0
        )

        insights.append(
            f"Largest transaction is "
            f"{largest_merchant} at "
            f"{largest_amount:.2f}."
        )

    if transactions:
        insights.append(
            f"Average transaction amount is "
            f"{average:.2f}."
        )

    return {
        "total_spending": summary.get(
            "total_spending",
            0.0,
        ),
        "transaction_count": summary.get(
            "transaction_count",
            0,
        ),
        "highest_category": category,
        "highest_category_amount": category_amount,
        "highest_merchant": merchant,
        "highest_merchant_amount": merchant_amount,
        "largest_transaction": largest,
        "average_transaction": average,
        "insights": insights,
    }