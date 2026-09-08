import json
from pathlib import Path

from src.models.email import Email
from src.processing.classifier import classify_emails
from src.processing.extractor import extract_transaction


EMAILS_FILE = Path(
    "data/raw/emails.jsonl"
)


def load_emails() -> list[Email]:

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
                    f"Skipping invalid JSON on "
                    f"line {line_number}: {error}"
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

    print(
        "Loading normalized emails..."
    )

    emails = load_emails()

    print(
        f"Loaded {len(emails)} emails."
    )

    print(
        "Running transaction classification..."
    )

    classifications = classify_emails(
        emails
    )

    candidates = [
        email
        for email, result in zip(
            emails,
            classifications,
        )
        if result.is_transaction_candidate
    ]

    print(
        f"Transaction candidates: "
        f"{len(candidates)}"
    )

    print(
        "\n========== TRANSACTION EXTRACTION =========="
    )

    if not candidates:

        print(
            "No transaction candidates found."
        )

        print(
            "Nothing to extract."
        )

        return

    for email in candidates:

        result = extract_transaction(
            email
        )

        print(
            "\nMessage ID:",
            result.message_id,
        )

        print(
            "Merchant:",
            result.merchant or "Unknown",
        )

        print(
            "Amount:",
            result.amount
            if result.amount is not None
            else "Unknown",
        )

        print(
            "Currency:",
            result.currency or "Unknown",
        )

        print(
            "Transaction date:",
            result.transaction_date
            or "Unknown",
        )

        print(
            "Transaction type:",
            result.transaction_type
            or "Unknown",
        )

        print(
            f"Extraction confidence: "
            f"{result.confidence:.2f}"
        )

        print(
            "--------------------------------------------------"
        )


if __name__ == "__main__":
    main()