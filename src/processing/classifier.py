import re

from dataclasses import dataclass

from typing import List

from src.models.email import Email


@dataclass
class ClassificationResult:
    """
    Result of classifying an email as a potential
    spending/transaction email.
    """

    message_id: str
    is_transaction_candidate: bool
    confidence: float
    matched_signals: List[str]


# ============================================================
# STRONG TRANSACTION SIGNALS
# ============================================================

STRONG_TRANSACTION_KEYWORDS = [
    "payment successful",
    "payment received",
    "payment confirmed",
    "payment completed",
    "transaction successful",
    "transaction completed",
    "transaction confirmed",
    "purchase successful",
    "purchase confirmed",
    "order confirmed",
    "order placed",
    "order delivered",
    "invoice generated",
    "invoice attached",
    "receipt for",
    "amount paid",
    "total paid",
    "charged",
    "debited",
    "subscription renewed",
    "subscription charged",
    "payment processed",
    "payment has been processed",
    "your payment",
    "your order",
    "your purchase",
    "your receipt",
    "your invoice",
]


# ============================================================
# MEDIUM TRANSACTION SIGNALS
# ============================================================

MEDIUM_TRANSACTION_KEYWORDS = [
    "purchase",
    "payment",
    "transaction",
    "subscription",
    "order",
]


# ============================================================
# WEAK FINANCIAL SIGNALS
# ============================================================

WEAK_FINANCIAL_KEYWORDS = [
    "total",
    "paid",
    "price",
    "cost",
    "amount",
]


# ============================================================
# NEGATIVE / NON-TRANSACTION CONTEXT
# ============================================================

NEGATIVE_CONTEXT_KEYWORDS = [
    "newsletter",
    "blog post",
    "read more",
    "reader-supported publication",
    "article",
    "this article",
    "course",
    "courses",
    "lesson",
    "this lesson",
    "guide",
    "this guide",
    "tutorial",
    "interview",
    "system design",
    "career opportunities",
    "hiring",
    "job hunting",
    "how to",
    "here's how",
    "learn how",
    "recap",
    "long weekend",
    "save money",
    "discount",
    "50% off",
    "off on annual",
    "limited time offer",
    "special offer",
    "career",
    "jobs",
]


# ============================================================
# STRONG NEGATIVE CONTEXT
# ============================================================

STRONG_NEGATIVE_CONTEXT_KEYWORDS = [
    "reader-supported publication",
    "subscribe to download the article",
    "subscribe to download",
    "this article",
    "this guide",
    "this lesson",
    "this newsletter",
    "career opportunities",
    "job hunting",
    "50% off",
    "discount",
]


# ============================================================
# EXPLICIT TRANSACTION CONTEXT
#
# These phrases are stronger than generic words such as
# "order", "subscription", or "payment".
# ============================================================

EXPLICIT_TRANSACTION_CONTEXT = [
    r"\byour order\b",
    r"\border confirmation\b",
    r"\border number\b",
    r"\border id\b",
    r"\byour purchase\b",
    r"\bpurchase confirmation\b",
    r"\bpurchase date\b",
    r"\byour payment\b",
    r"\bpayment confirmation\b",
    r"\bpayment date\b",
    r"\bpayment method\b",
    r"\btransaction id\b",
    r"\btransaction date\b",
    r"\btransaction amount\b",
    r"\binvoice number\b",
    r"\binvoice date\b",
    r"\binvoice total\b",
    r"\breceipt number\b",
    r"\breceipt date\b",
    r"\bamount charged\b",
    r"\bamount paid\b",
    r"\btotal charged\b",
    r"\btotal paid\b",
    r"\bsubscription renewal\b",
    r"\bsubscription renewed\b",
    r"\bsubscription charged\b",
    r"\brenewal payment\b",
]


# ============================================================
# ACTION / PAYMENT VERBS
# ============================================================

ACTION_PATTERNS = [
    r"\bpaid\b",
    r"\bcharged\b",
    r"\bdebited\b",
    r"\bpurchased\b",
    r"\bordered\b",
    r"\brenewed\b",
    r"\brefunded\b",
]


# ============================================================
# CURRENCY / AMOUNT PATTERNS
#
# Only actual currency expressions count.
# Bare numbers, percentages, years, article numbers, etc.
# do NOT count as transaction amounts.
# ============================================================

AMOUNT_PATTERNS = [
    # ₹499 / ₹1,299 / ₹1,299.50
    r"₹\s*\d[\d,]*(?:\.\d{1,2})?",

    # Rs 499 / Rs. 499 / rs 1,299.50
    r"\brs\.?\s*\d[\d,]*(?:\.\d{1,2})?",

    # INR 499 / INR 1,299.50
    r"\binr\s*\d[\d,]*(?:\.\d{1,2})?",

    # $19 / $19.99 / $1,299.50
    r"\$\s*\d[\d,]*(?:\.\d{1,2})?",

    # USD 19 / USD 19.99
    r"\busd\s*\d[\d,]*(?:\.\d{1,2})?",

    # 499 ₹ / 499 INR / 499 USD
    r"\b\d[\d,]*(?:\.\d{1,2})?\s*(?:₹|rs\.?|inr|usd)\b",
]


def normalize_text(email: Email) -> str:
    """
    Combine important email fields into one normalized
    lowercase text representation.
    """

    parts = [
        email.sender or "",
        email.subject or "",
        email.body or "",
        email.snippet or "",
    ]

    text = " ".join(parts)

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.lower().strip()


def find_keyword_signals(text: str) -> List[str]:
    """
    Find strong, medium, and weak transaction-related
    keyword signals.
    """

    signals = []

    for keyword in STRONG_TRANSACTION_KEYWORDS:

        if keyword in text:

            signals.append(
                f"strong:{keyword}"
            )

    for keyword in MEDIUM_TRANSACTION_KEYWORDS:

        if keyword in text:

            signals.append(
                f"medium:{keyword}"
            )

    for keyword in WEAK_FINANCIAL_KEYWORDS:

        if keyword in text:

            signals.append(
                f"weak:{keyword}"
            )

    return signals


def find_negative_signals(text: str) -> List[str]:
    """
    Find context suggesting that the email is content,
    newsletter, educational material, job content,
    promotional material, etc.
    """

    signals = []

    for keyword in NEGATIVE_CONTEXT_KEYWORDS:

        if keyword in text:

            signals.append(
                f"negative:{keyword}"
            )

    return signals


def find_strong_negative_signals(text: str) -> List[str]:
    """
    Find especially strong evidence that an email is
    informational, promotional, or content-oriented.
    """

    signals = []

    for keyword in STRONG_NEGATIVE_CONTEXT_KEYWORDS:

        if keyword in text:

            signals.append(
                f"strong_negative:{keyword}"
            )

    return signals


def find_explicit_transaction_signals(
    text: str,
) -> List[str]:
    """
    Find phrases that strongly indicate an actual
    transaction context rather than generic financial
    discussion.
    """

    signals = []

    for pattern in EXPLICIT_TRANSACTION_CONTEXT:

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):

            signals.append(
                f"context:{pattern}"
            )

    return signals


def find_action_signals(
    text: str,
) -> List[str]:
    """
    Find explicit financial action verbs.
    """

    signals = []

    for pattern in ACTION_PATTERNS:

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):

            signals.append(
                f"action:{pattern}"
            )

    return signals


def find_amount_signals(
    text: str,
) -> List[str]:
    """
    Detect recognizable currency amounts.

    Bare numbers are deliberately ignored.
    """

    signals = []

    for pattern in AMOUNT_PATTERNS:

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):

            signals.append(
                "amount_pattern"
            )

            break

    return signals


def calculate_confidence(
    strong_count: int,
    medium_count: int,
    weak_count: int,
    has_amount: bool,
    negative_count: int,
    strong_negative_count: int,
    explicit_context_count: int,
    action_count: int,
) -> float:
    """
    Calculate a deterministic confidence score.

    Strong transaction evidence and explicit transaction
    context receive the most weight.

    Generic financial words receive only a small weight.

    Negative/content signals reduce confidence.
    """

    score = 0.0

    # --------------------------------------------------------
    # Strong transaction phrases
    # --------------------------------------------------------

    score += min(
        strong_count * 0.45,
        0.90,
    )

    # --------------------------------------------------------
    # Explicit transaction context
    # --------------------------------------------------------

    score += min(
        explicit_context_count * 0.25,
        0.50,
    )

    # --------------------------------------------------------
    # Explicit action verbs
    # --------------------------------------------------------

    score += min(
        action_count * 0.12,
        0.24,
    )

    # --------------------------------------------------------
    # Medium keywords
    #
    # Generic words such as "order" and "subscription"
    # are intentionally given low weight.
    # --------------------------------------------------------

    score += min(
        medium_count * 0.05,
        0.15,
    )

    # --------------------------------------------------------
    # Weak financial words
    # --------------------------------------------------------

    score += min(
        weak_count * 0.02,
        0.06,
    )

    # --------------------------------------------------------
    # Actual currency amount
    # --------------------------------------------------------

    if has_amount:

        score += 0.20

    # --------------------------------------------------------
    # Ordinary negative context
    # --------------------------------------------------------

    score -= min(
        negative_count * 0.06,
        0.30,
    )

    # --------------------------------------------------------
    # Strong negative context
    # --------------------------------------------------------

    score -= min(
        strong_negative_count * 0.30,
        0.75,
    )

    return min(
        max(
            round(score, 2),
            0.0,
        ),
        1.0,
    )


def classify_email(
    email: Email,
) -> ClassificationResult:
    """
    Classify a single email as a potential transaction email.

    The classifier distinguishes between:

    1. Strong transaction language
    2. Explicit transaction context
    3. Financial action language
    4. Generic financial keywords
    5. Actual currency amounts
    6. Newsletter/content/promotional context

    Generic words alone should not classify an email as
    a transaction.
    """

    text = normalize_text(email)

    keyword_signals = find_keyword_signals(
        text
    )

    negative_signals = find_negative_signals(
        text
    )

    strong_negative_signals = (
        find_strong_negative_signals(
            text
        )
    )

    explicit_transaction_signals = (
        find_explicit_transaction_signals(
            text
        )
    )

    action_signals = find_action_signals(
        text
    )

    amount_signals = find_amount_signals(
        text
    )

    # ========================================================
    # COUNT SIGNAL TYPES
    # ========================================================

    strong_count = sum(
        1
        for signal in keyword_signals
        if signal.startswith("strong:")
    )

    medium_count = sum(
        1
        for signal in keyword_signals
        if signal.startswith("medium:")
    )

    weak_count = sum(
        1
        for signal in keyword_signals
        if signal.startswith("weak:")
    )

    negative_count = len(
        negative_signals
    )

    strong_negative_count = len(
        strong_negative_signals
    )

    explicit_context_count = len(
        explicit_transaction_signals
    )

    action_count = len(
        action_signals
    )

    has_amount = (
        "amount_pattern"
        in amount_signals
    )

    # ========================================================
    # CONFIDENCE
    # ========================================================

    confidence = calculate_confidence(
        strong_count=strong_count,
        medium_count=medium_count,
        weak_count=weak_count,
        has_amount=has_amount,
        negative_count=negative_count,
        strong_negative_count=strong_negative_count,
        explicit_context_count=explicit_context_count,
        action_count=action_count,
    )

    # ========================================================
    # TRANSACTION DECISION
    # ========================================================

    has_strong_transaction = (
        strong_count >= 1
    )

    has_explicit_context = (
        explicit_context_count >= 1
    )

    has_financial_action = (
        action_count >= 1
    )

    # --------------------------------------------------------
    # Rule 1:
    #
    # Strong transaction phrase + no strong content context.
    # --------------------------------------------------------

    rule_strong_transaction = (
        has_strong_transaction
        and strong_negative_count == 0
        and confidence >= 0.45
    )

    # --------------------------------------------------------
    # Rule 2:
    #
    # Explicit transaction context + currency amount.
    #
    # Example:
    # "Your order ... ₹499"
    # "Invoice total ... $19.99"
    # --------------------------------------------------------

    rule_explicit_amount = (
        has_explicit_context
        and has_amount
        and strong_negative_count == 0
        and confidence >= 0.40
    )

    # --------------------------------------------------------
    # Rule 3:
    #
    # Explicit transaction context + financial action.
    #
    # This handles legitimate transaction emails where the
    # currency expression may not be immediately recognizable.
    # --------------------------------------------------------

    rule_explicit_action = (
        has_explicit_context
        and has_financial_action
        and strong_negative_count == 0
        and confidence >= 0.40
    )

    # --------------------------------------------------------
    # Rule 4:
    #
    # Strong transaction phrase + amount.
    # --------------------------------------------------------

    rule_strong_amount = (
        has_strong_transaction
        and has_amount
        and strong_negative_count == 0
    )

    # --------------------------------------------------------
    # Generic financial words are NOT enough.
    #
    # This intentionally rejects things like:
    #
    # "subscription"
    # "order"
    # "purchase"
    # "amount"
    #
    # when they occur inside articles/newsletters.
    # --------------------------------------------------------

    is_transaction_candidate = (
        rule_strong_transaction
        or rule_explicit_amount
        or rule_explicit_action
        or rule_strong_amount
    )

    # ========================================================
    # NEGATIVE OVERRIDES
    # ========================================================

    # Strong content evidence overrides weak/ambiguous
    # transaction language.

    if (
        strong_negative_count >= 1
        and not has_strong_transaction
        and not has_explicit_context
    ):

        is_transaction_candidate = False

    # Promotional/content emails should not become
    # transaction candidates merely because they mention
    # subscription, payment, price, etc.

    promotional_content = (
        negative_count >= 2
        and not has_strong_transaction
        and not has_explicit_context
    )

    if promotional_content:

        is_transaction_candidate = False

    # Generic medium keywords + amount are still insufficient
    # without explicit transaction context.

    if (
        has_amount
        and medium_count >= 1
        and not has_strong_transaction
        and not has_explicit_context
    ):

        is_transaction_candidate = False

    # Generic action words such as "paid" inside an article
    # are not sufficient on their own.

    if (
        action_count >= 1
        and not has_strong_transaction
        and not has_explicit_context
    ):

        is_transaction_candidate = False

    # ========================================================
    # FINAL SIGNAL LIST
    # ========================================================

    signals = (
        keyword_signals
        + amount_signals
        + explicit_transaction_signals
        + action_signals
        + negative_signals
        + strong_negative_signals
    )

    return ClassificationResult(
        message_id=email.message_id,
        is_transaction_candidate=(
            is_transaction_candidate
        ),
        confidence=confidence,
        matched_signals=signals,
    )


def classify_emails(
    emails: List[Email],
) -> List[ClassificationResult]:
    """
    Classify a list of normalized emails.
    """

    return [
        classify_email(email)
        for email in emails
    ]


if __name__ == "__main__":

    print(
        "classifier.py provides the transaction "
        "candidate classification functions."
    )