from collections import defaultdict
from typing import Any


def _amount(transaction: dict[str, Any]) -> float:
    """
    Safely convert the transaction amount to float.
    """

    value = transaction.get("amount", 0)

    try:
        return float(value)

    except (TypeError, ValueError):
        return 0.0


def spending_by_category(
    transactions: list[dict[str, Any]],
) -> dict[str, float]:
    """
    Calculate total spending by category.
    """

    totals = defaultdict(float)

    for transaction in transactions:

        category = (
            transaction.get("category")
            or "uncategorized"
        )

        totals[category] += _amount(
            transaction
        )

    return dict(
        sorted(
            totals.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )


def spending_by_merchant(
    transactions: list[dict[str, Any]],
) -> dict[str, float]:
    """
    Calculate total spending by merchant.
    """

    totals = defaultdict(float)

    for transaction in transactions:

        merchant = (
            transaction.get("merchant")
            or "unknown"
        )

        totals[merchant] += _amount(
            transaction
        )

    return dict(
        sorted(
            totals.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )


def spending_by_month(
    transactions: list[dict[str, Any]],
) -> dict[str, float]:
    """
    Calculate total spending by month.

    Expected date format:
    YYYY-MM-DD
    or another string beginning with YYYY-MM.
    """

    totals = defaultdict(float)

    for transaction in transactions:

        date = str(
            transaction.get("date")
            or ""
        )

        month = (
            date[:7]
            if len(date) >= 7
            else "unknown"
        )

        totals[month] += _amount(
            transaction
        )

    return dict(
        sorted(
            totals.items()
        )
    )


def total_spending(
    transactions: list[dict[str, Any]],
) -> float:
    """
    Calculate total spending.
    """

    return round(
        sum(
            _amount(transaction)
            for transaction in transactions
        ),
        2,
    )


def transaction_count(
    transactions: list[dict[str, Any]],
) -> int:
    """
    Return the number of transactions.
    """

    return len(transactions)


def build_spending_summary(
    transactions: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Build the complete Phase 5 spending summary.
    """

    return {
        "transaction_count": transaction_count(
            transactions
        ),
        "total_spending": total_spending(
            transactions
        ),
        "by_category": spending_by_category(
            transactions
        ),
        "by_merchant": spending_by_merchant(
            transactions
        ),
        "by_month": spending_by_month(
            transactions
        ),
    }