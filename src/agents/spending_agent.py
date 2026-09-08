from collections import defaultdict
from datetime import datetime
from statistics import mean
from typing import Any


CATEGORY_RULES = {
    "subscription": "Subscriptions",
    "netflix": "Subscriptions",
    "spotify": "Subscriptions",
    "adobe": "Software",
    "aws": "Software",
    "uber": "Transport",
    "ola": "Transport",
    "airbnb": "Travel",
    "flight": "Travel",
    "hotel": "Travel",
    "amazon": "Shopping",
    "walmart": "Shopping",
    "restaurant": "Food",
    "food": "Food",
    "grocery": "Food",
    "electricity": "Utilities",
    "internet": "Utilities",
    "hospital": "Healthcare",
    "pharmacy": "Healthcare",
}


def categorize_transaction(transaction: dict[str, Any]) -> str:
    """Assign a transparent category from merchant and transaction text."""

    text = " ".join(
        str(transaction.get(field) or "")
        for field in ("merchant", "subject", "transaction_type")
    ).lower()

    for keyword, category in CATEGORY_RULES.items():
        if keyword in text:
            return category

    return transaction.get("category") or "Other"


def gmail_message_url(message_id: str | None) -> str | None:
    """Create a traceability link without requesting Gmail write access."""

    if not message_id:
        return None

    return f"https://mail.google.com/mail/u/0/#all/{message_id}"


def enrich_transactions(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Add category and Gmail traceability fields to transaction records."""

    enriched = []
    for transaction in transactions:
        record = dict(transaction)
        record["category"] = categorize_transaction(record)
        record["gmail_url"] = gmail_message_url(
            record.get("message_id")
        )
        enriched.append(record)

    return enriched


def _amount(transaction: dict[str, Any]) -> float:
    try:
        return float(transaction.get("amount") or 0)
    except (TypeError, ValueError):
        return 0.0


def _date(transaction: dict[str, Any]) -> datetime | None:
    value = str(transaction.get("date") or "")[:10]
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None


def recurring_payments(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Find merchants with repeated, similarly sized payments."""

    by_merchant: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for transaction in transactions:
        merchant = str(transaction.get("merchant") or "unknown")
        by_merchant[merchant].append(transaction)

    recurring = []
    for merchant, items in by_merchant.items():
        if len(items) < 2:
            continue

        amounts = [_amount(item) for item in items]
        average = mean(amounts)
        if average <= 0:
            continue

        similar = [
            amount
            for amount in amounts
            if abs(amount - average) / average <= 0.10
        ]
        if len(similar) < 2:
            continue

        recurring.append(
            {
                "merchant": merchant,
                "average_amount": round(mean(similar), 2),
                "occurrences": len(similar),
                "explanation": (
                    f"{merchant} appears {len(similar)} times "
                    "with similar payment amounts."
                ),
            }
        )

    return recurring


def unusual_transactions(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Flag first-time merchants and unusually large merchant payments."""

    by_merchant: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for transaction in transactions:
        by_merchant[str(transaction.get("merchant") or "unknown")].append(transaction)

    findings = []
    for merchant, items in by_merchant.items():
        amounts = [_amount(item) for item in items]
        if len(items) == 1:
            transaction = items[0]
            findings.append(
                {
                    "type": "new_merchant",
                    "merchant": merchant,
                    "amount": _amount(transaction),
                    "message": (
                        f"A payment of {_amount(transaction):.2f} was made "
                        f"to a merchant not seen elsewhere in this dataset."
                    ),
                    "gmail_url": transaction.get("gmail_url"),
                }
            )
            continue

        for index, transaction in enumerate(items):
            amount = _amount(transaction)
            comparison_amounts = amounts[:index] + amounts[index + 1:]
            baseline = mean(comparison_amounts) if comparison_amounts else 0.0
            if baseline > 0 and amount >= baseline * 2:
                findings.append(
                    {
                        "type": "amount_spike",
                        "merchant": merchant,
                        "amount": amount,
                        "message": (
                            f"The {_amount(transaction):.2f} payment to {merchant} "
                            f"is at least twice the merchant average of {baseline:.2f}."
                        ),
                        "gmail_url": transaction.get("gmail_url"),
                    }
                )

    return findings


def upcoming_payments(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Find transactions dated after today and explain why they are upcoming."""

    today = datetime.now().date()
    upcoming = []

    for transaction in transactions:
        transaction_date = _date(transaction)
        if transaction_date is None or transaction_date.date() <= today:
            continue

        merchant = str(transaction.get("merchant") or "unknown")
        amount = _amount(transaction)
        upcoming.append(
            {
                "merchant": merchant,
                "amount": amount,
                "date": transaction_date.strftime("%Y-%m-%d"),
                "message": (
                    f"An upcoming payment of {amount:.2f} to {merchant} "
                    f"is dated {transaction_date.strftime('%Y-%m-%d')}."
                ),
                "gmail_url": transaction.get("gmail_url"),
            }
        )

    return sorted(upcoming, key=lambda item: item["date"])


def run_spending_agent(
    transactions: list[dict[str, Any]],
) -> dict[str, Any]:
    """Coordinate deterministic category, recurring, anomaly, and traceability analysis."""

    enriched = enrich_transactions(transactions)
    recurring = recurring_payments(enriched)
    unusual = unusual_transactions(enriched)
    upcoming = upcoming_payments(enriched)

    return {
        "transactions": enriched,
        "recurring_payments": recurring,
        "unusual_transactions": unusual,
        "upcoming_payments": upcoming,
        "agent_insights": [
            item["explanation"]
            for item in recurring
        ]
        + [
            item["message"]
            for item in unusual
        ],
    }