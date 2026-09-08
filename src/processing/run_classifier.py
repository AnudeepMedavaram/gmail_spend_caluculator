import json
from pathlib import Path

from src.models.email import Email
from src.processing.classifier import classify_emails


EMAILS_FILE = Path(
    "data/raw/emails.jsonl"
)


def load_emails() -> list[Email]:
    """
    Load normalized email records from JSONL
    and convert them back into Email objects.
    """

    if not EMAILS_FILE.exists():

        raise FileNotFoundError(
            f"Email dataset not found: {EMAILS_FILE}"
        )

    emails = []

    with EMAILS_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line_number, line in enumerate(
            file,
            start=1
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

            email = Email(
                message_id=record.get(
                    "message_id",
                    ""
                ),
                thread_id=record.get(
                    "thread_id",
                    ""
                ),
                sender=record.get(
                    "sender",
                    ""
                ),
                recipient=record.get(
                    "recipient",
                    ""
                ),
                subject=record.get(
                    "subject",
                    ""
                ),
                date=record.get(
                    "date",
                    ""
                ),
                body=record.get(
                    "body",
                    ""
                ),
                snippet=record.get(
                    "snippet",
                    ""
                ),
            )

            emails.append(email)

    return emails


def print_classification_report(
    emails: list[Email],
    results,
):
    """
    Print a human-readable classification report.
    """

    total = len(results)

    transaction_candidates = sum(
        1
        for result in results
        if result.is_transaction_candidate
    )

    non_transaction = (
        total - transaction_candidates
    )

    print(
        "\n========== TRANSACTION CLASSIFICATION =========="
    )

    print(
        f"Total emails: {total}"
    )

    print(
        f"Transaction candidates: "
        f"{transaction_candidates}"
    )

    print(
        f"Non-transaction emails: "
        f"{non_transaction}"
    )

    print(
        "\n--------------------------------------------------"
    )

    email_lookup = {
        email.message_id: email
        for email in emails
    }

    for result in results:

        email = email_lookup.get(
            result.message_id
        )

        if email is None:
            continue

        print(
            f"\nMessage ID: {result.message_id}"
        )

        print(
            f"Subject: {email.subject}"
        )

        print(
            "Candidate: "
            + (
                "YES"
                if result.is_transaction_candidate
                else "NO"
            )
        )

        print(
            f"Confidence: {result.confidence:.2f}"
        )

        if result.matched_signals:

            print("Signals:")

            for signal in result.matched_signals:

                print(
                    f"  - {signal}"
                )

        else:

            print(
                "Signals: none"
            )

        print(
            "--------------------------------------------------"
        )

    print(
        "\n=================================================="
    )


def main():
    """
    Run transaction candidate classification
    against the normalized email dataset.
    """

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

    results = classify_emails(
        emails
    )

    print_classification_report(
        emails,
        results
    )


if __name__ == "__main__":
    main()