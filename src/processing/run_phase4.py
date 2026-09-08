import json
from pathlib import Path

from src.models.email import Email
from src.processing.classifier import classify_emails
from src.processing.extractor import extract_transaction
from src.processing.validator import validate_transaction
from src.processing.storage import save_transactions


EMAILS_FILE = Path(
    "data/raw/emails.jsonl"
)


def load_emails() -> list[Email]:
    """
    Load email records from JSONL and convert them
    into Email objects.
    """

    if not EMAILS_FILE.exists():
        raise FileNotFoundError(
            f"Email dataset not found: {EMAILS_FILE}"
        )

    emails = []

    with EMAILS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line_number, line in enumerate(
            file,
            start=1,
        ):

            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)

            except json.JSONDecodeError as error:
                print(
                    f"Skipping invalid JSON on line "
                    f"{line_number}: {error}"
                )
                continue

            emails.append(
                Email(
                    message_id=record.get(
                        "message_id",
                        "",
                    ),
                    thread_id=record.get(
                        "thread_id",
                        "",
                    ),
                    sender=record.get(
                        "sender",
                        "",
                    ),
                    recipient=record.get(
                        "recipient",
                        "",
                    ),
                    subject=record.get(
                        "subject",
                        "",
                    ),
                    date=record.get(
                        "date",
                        "",
                    ),
                    body=record.get(
                        "body",
                        "",
                    ),
                    snippet=record.get(
                        "snippet",
                        "",
                    ),
                )
            )

    return emails


def main():
    """
    Run the complete Phase 4 transaction pipeline.

    Pipeline:

        Emails
          ↓
        Classification
          ↓
        Extraction
          ↓
        Validation
          ↓
        Storage
    """

    print(
        "\n========== PHASE 4 PIPELINE =========="
    )

    # --------------------------------------------------------
    # 1. LOAD EMAILS
    # --------------------------------------------------------

    print("\n[1/5] Loading emails...")

    emails = load_emails()

    print(
        f"Loaded {len(emails)} emails."
    )

    # --------------------------------------------------------
    # 2. CLASSIFICATION
    # --------------------------------------------------------

    print(
        "\n[2/5] Classifying transaction candidates..."
    )

    classification_results = classify_emails(
        emails
    )

    candidate_ids = {
        result.message_id
        for result in classification_results
        if result.is_transaction_candidate
    }

    candidates = [
        email
        for email in emails
        if email.message_id in candidate_ids
    ]

    print(
        f"Transaction candidates: {len(candidates)}"
    )

    # --------------------------------------------------------
    # 3. EXTRACTION
    # --------------------------------------------------------

    print(
        "\n[3/5] Extracting transactions..."
    )

    extracted_transactions = []

    for email in candidates:

        transaction = extract_transaction(
            email
        )

        if transaction is None:
            print(
                f"Extraction failed: {email.message_id}"
            )
            continue

        transaction_record = {
            "message_id": email.message_id,
            "merchant": transaction.merchant,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "date": (
                transaction.transaction_date
                or email.date
            ),
            "transaction_type": transaction.transaction_type,
        }

        extracted_transactions.append(
            transaction_record
        )

    print(
        f"Transactions extracted: "
        f"{len(extracted_transactions)}"
    )

    # --------------------------------------------------------
    # 4. VALIDATION
    # --------------------------------------------------------

    print(
        "\n[4/5] Validating transactions..."
    )

    valid_transactions = []

    for transaction in extracted_transactions:

        validation = validate_transaction(
            transaction
        )

        if validation.is_valid:

            valid_transactions.append(
                transaction
            )

        else:

            print(
                "\nInvalid transaction:"
            )

            print(
                transaction
            )

            print(
                "Errors:"
            )

            for error in validation.errors:
                print(
                    f"  - {error}"
                )

    print(
        f"Valid transactions: "
        f"{len(valid_transactions)}"
    )

    # --------------------------------------------------------
    # 5. STORAGE
    # --------------------------------------------------------

    print(
        "\n[5/5] Saving transactions..."
    )

    save_transactions(
        valid_transactions
    )

    print(
        f"Saved {len(valid_transactions)} "
        f"transactions."
    )

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    print(
        "\n========== PHASE 4 SUMMARY =========="
    )

    print(
        f"Emails loaded:       {len(emails)}"
    )

    print(
        f"Candidates:           {len(candidates)}"
    )

    print(
        f"Extracted:            "
        f"{len(extracted_transactions)}"
    )

    print(
        f"Valid:                "
        f"{len(valid_transactions)}"
    )

    print(
        "Output:               "
        "data/processed/transactions.jsonl"
    )

    print(
        "\nPhase 4 pipeline completed."
    )

    print(
        "======================================"
    )


if __name__ == "__main__":
    main()