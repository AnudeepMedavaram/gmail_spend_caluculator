from dataclasses import dataclass
from typing import List, Optional

from src.models.email import Email


@dataclass
class ValidationResult:
    """
    Result of validating an extracted transaction.
    """

    is_valid: bool
    errors: List[str]


# ============================================================
# REQUIRED TRANSACTION FIELDS
# ============================================================

REQUIRED_FIELDS = [
    "merchant",
    "amount",
    "currency",
    "date",
]


# ============================================================
# VALIDATION HELPERS
# ============================================================

def validate_merchant(
    merchant: Optional[str],
    errors: List[str],
) -> None:
    """
    Validate merchant information.
    """

    if not merchant:
        errors.append("missing_merchant")
        return

    if not merchant.strip():
        errors.append("empty_merchant")


def validate_amount(
    amount,
    errors: List[str],
) -> None:
    """
    Validate transaction amount.
    """

    if amount is None:
        errors.append("missing_amount")
        return

    try:
        numeric_amount = float(amount)

    except (TypeError, ValueError):
        errors.append("invalid_amount")
        return

    if numeric_amount < 0:
        errors.append("negative_amount")


def validate_currency(
    currency: Optional[str],
    errors: List[str],
) -> None:
    """
    Validate currency code.
    """

    if not currency:
        errors.append("missing_currency")
        return

    currency = str(currency).strip().upper()

    if len(currency) != 3:
        errors.append("invalid_currency")


def validate_date(
    date,
    errors: List[str],
) -> None:
    """
    Validate transaction date presence.

    Detailed date parsing is intentionally deferred for
    the Phase 4 baseline.
    """

    if not date:
        errors.append("missing_date")


# ============================================================
# TRANSACTION VALIDATION
# ============================================================

def validate_transaction(
    transaction: dict,
) -> ValidationResult:
    """
    Validate one extracted transaction.

    Phase 4 baseline validation checks:
    - merchant
    - amount
    - currency
    - date
    """

    errors: List[str] = []

    if not isinstance(transaction, dict):
        return ValidationResult(
            is_valid=False,
            errors=["transaction_not_dict"],
        )

    validate_merchant(
        transaction.get("merchant"),
        errors,
    )

    validate_amount(
        transaction.get("amount"),
        errors,
    )

    validate_currency(
        transaction.get("currency"),
        errors,
    )

    validate_date(
        transaction.get("date"),
        errors,
    )

    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
    )


def validate_transactions(
    transactions: List[dict],
) -> List[ValidationResult]:
    """
    Validate a list of extracted transactions.
    """

    return [
        validate_transaction(transaction)
        for transaction in transactions
    ]


# ============================================================
# EMAIL-LEVEL VALIDATION
# ============================================================

def validate_extracted_transaction(
    email: Email,
    transaction: dict,
) -> ValidationResult:
    """
    Validate an extracted transaction while keeping the
    source email available for future validation rules.

    The email parameter is intentionally retained so that
    later phases can verify extracted fields against the
    source email.
    """

    if email is None:
        return ValidationResult(
            is_valid=False,
            errors=["missing_source_email"],
        )

    return validate_transaction(transaction)


if __name__ == "__main__":
    print(
        "validator.py provides transaction validation functions."
    )