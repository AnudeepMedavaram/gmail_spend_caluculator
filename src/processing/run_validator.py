from src.processing.validator import validate_transaction


def main():
    """
    Run a small validation smoke test for Phase 4.
    """

    print(
        "========== TRANSACTION VALIDATION =========="
    )

    valid_transaction = {
        "merchant": "Amazon",
        "amount": 49.99,
        "currency": "USD",
        "date": "2026-08-28",
    }

    invalid_transaction = {
        "merchant": "",
        "amount": -20,
        "currency": "US",
        "date": None,
    }

    print("\nValid transaction:")
    print(valid_transaction)

    valid_result = validate_transaction(
        valid_transaction
    )

    print(
        f"Valid: {valid_result.is_valid}"
    )

    print(
        f"Errors: {valid_result.errors}"
    )

    print("\nInvalid transaction:")
    print(invalid_transaction)

    invalid_result = validate_transaction(
        invalid_transaction
    )

    print(
        f"Valid: {invalid_result.is_valid}"
    )

    print(
        f"Errors: {invalid_result.errors}"
    )

    print(
        "\n============================================="
    )


if __name__ == "__main__":
    main()