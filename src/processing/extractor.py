import re
from dataclasses import dataclass
from typing import Optional

from src.models.email import Email


@dataclass
class TransactionExtractionResult:
    """
    Structured transaction information extracted
    from a transaction candidate email.
    """

    message_id: str
    merchant: Optional[str]
    amount: Optional[float]
    currency: Optional[str]
    transaction_date: Optional[str]
    transaction_type: Optional[str]
    confidence: float


# ============================================================
# AMOUNT EXTRACTION
# ============================================================

AMOUNT_PATTERNS = [
    (
        r"₹\s*([\d,]+(?:\.\d{1,2})?)",
        "INR",
    ),
    (
        r"\bINR\s*([\d,]+(?:\.\d{1,2})?)",
        "INR",
    ),
    (
        r"\bRs\.?\s*([\d,]+(?:\.\d{1,2})?)",
        "INR",
    ),
    (
        r"\$\s*([\d,]+(?:\.\d{1,2})?)",
        "USD",
    ),
    (
        r"\bUSD\s*([\d,]+(?:\.\d{1,2})?)",
        "USD",
    ),
]


def extract_amount(text: str):
    """
    Extract the first recognizable currency amount.
    """

    for pattern, currency in AMOUNT_PATTERNS:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:

            amount_text = match.group(1)

            amount_text = amount_text.replace(
                ",",
                "",
            )

            return float(amount_text), currency

    return None, None


# ============================================================
# MERCHANT EXTRACTION
# ============================================================

MERCHANT_PATTERNS = [
    r"payment\s+to\s+([A-Za-z0-9&.,' -]{2,60})",
    r"paid\s+to\s+([A-Za-z0-9&.,' -]{2,60})",
    r"purchase\s+from\s+([A-Za-z0-9&.,' -]{2,60})",
    r"order\s+from\s+([A-Za-z0-9&.,' -]{2,60})",
    r"merchant\s*:\s*([A-Za-z0-9&.,' -]{2,60})",
    r"seller\s*:\s*([A-Za-z0-9&.,' -]{2,60})",
]


def extract_merchant(text: str):
    """
    Extract merchant name using common transaction
    email patterns.
    """

    for pattern in MERCHANT_PATTERNS:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:

            merchant = match.group(1).strip()

            # Remove common trailing transaction words.
            merchant = re.split(
                r"\s+(?:for|on|at|amount|total|₹|\$|INR|USD)\b",
                merchant,
                flags=re.IGNORECASE,
            )[0].strip()

            return merchant

    return None


# ============================================================
# TRANSACTION TYPE
# ============================================================

def extract_transaction_type(text: str):
    """
    Determine a basic transaction type.
    """

    text = text.lower()

    if any(
        phrase in text
        for phrase in [
            "subscription renewed",
            "subscription charged",
            "recurring payment",
        ]
    ):
        return "subscription"

    if any(
        phrase in text
        for phrase in [
            "refund",
            "refunded",
            "money returned",
        ]
    ):
        return "refund"

    if any(
        phrase in text
        for phrase in [
            "payment",
            "paid",
            "charged",
            "purchase",
            "order",
            "transaction",
            "debited",
        ]
    ):
        return "purchase"

    return None


# ============================================================
# DATE EXTRACTION
# ============================================================

DATE_PATTERNS = [
    r"\b\d{4}-\d{2}-\d{2}\b",
    r"\b\d{1,2}/\d{1,2}/\d{4}\b",
    r"\b\d{1,2}-\d{1,2}-\d{4}\b",
]


def extract_transaction_date(text: str):
    """
    Extract a simple transaction date if explicitly
    present in the email body.
    """

    for pattern in DATE_PATTERNS:

        match = re.search(
            pattern,
            text,
        )

        if match:
            return match.group(0)

    return None


# ============================================================
# CONFIDENCE
# ============================================================

def calculate_extraction_confidence(
    amount,
    merchant,
    transaction_type,
    transaction_date,
):
    """
    Deterministic extraction confidence.

    This is intentionally simple for the Phase 4
    baseline.
    """

    score = 0.0

    if amount is not None:
        score += 0.40

    if merchant:
        score += 0.30

    if transaction_type:
        score += 0.20

    if transaction_date:
        score += 0.10

    return round(
        min(score, 1.0),
        2,
    )


# ============================================================
# MAIN EXTRACTION
# ============================================================

def extract_transaction(
    email: Email,
) -> TransactionExtractionResult:
    """
    Extract structured transaction information
    from a single email.
    """

    text = " ".join(
        [
            email.subject or "",
            email.body or "",
            email.snippet or "",
        ]
    )

    amount, currency = extract_amount(text)

    merchant = extract_merchant(text)

    transaction_type = extract_transaction_type(
        text
    )

    transaction_date = extract_transaction_date(
        text
    )

    confidence = calculate_extraction_confidence(
        amount=amount,
        merchant=merchant,
        transaction_type=transaction_type,
        transaction_date=transaction_date,
    )

    return TransactionExtractionResult(
        message_id=email.message_id,
        merchant=merchant,
        amount=amount,
        currency=currency,
        transaction_date=transaction_date,
        transaction_type=transaction_type,
        confidence=confidence,
    )


def extract_transactions(
    emails: list[Email],
) -> list[TransactionExtractionResult]:
    """
    Extract transactions from a list of emails.
    """

    return [
        extract_transaction(email)
        for email in emails
    ]


if __name__ == "__main__":

    print(
        "extractor.py provides transaction "
        "extraction functions."
    )