import json
from pathlib import Path


EMAILS_FILE = Path("data/raw/emails.jsonl")


REQUIRED_FIELDS = [
    "message_id",
    "thread_id",
    "sender",
    "recipient",
    "subject",
    "date",
    "body",
    "snippet",
]


def load_emails():
    """
    Load all email records from the JSONL file.
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

        for line_number, line in enumerate(file, start=1):

            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)

            except json.JSONDecodeError as error:
                print(
                    f"Invalid JSON on line "
                    f"{line_number}: {error}"
                )
                continue

            emails.append(record)

    return emails


def validate_required_fields(emails):
    """
    Check whether every email contains the required fields.
    """

    missing_fields = []

    for index, email in enumerate(emails, start=1):

        missing = [
            field
            for field in REQUIRED_FIELDS
            if field not in email
        ]

        if missing:
            missing_fields.append(
                {
                    "record": index,
                    "missing": missing,
                }
            )

    return missing_fields


def find_duplicate_message_ids(emails):
    """
    Find duplicate Gmail message IDs.
    """

    seen = set()
    duplicates = set()

    for email in emails:

        message_id = email.get("message_id")

        if not message_id:
            continue

        if message_id in seen:
            duplicates.add(message_id)

        seen.add(message_id)

    return duplicates


def count_empty_fields(emails):
    """
    Count records containing empty important fields.
    """

    fields_to_check = [
        "sender",
        "recipient",
        "subject",
        "date",
        "body",
    ]

    empty_counts = {
        field: 0
        for field in fields_to_check
    }

    for email in emails:

        for field in fields_to_check:

            value = email.get(field)

            if value is None or str(value).strip() == "":
                empty_counts[field] += 1

    return empty_counts


def print_validation_report(emails):
    """
    Print a validation report for the stored dataset.
    """

    print("\n========== DATASET VALIDATION ==========")

    print(
        f"Total records: {len(emails)}"
    )

    missing_fields = validate_required_fields(
        emails
    )

    if missing_fields:
        print(
            f"Records with missing fields: "
            f"{len(missing_fields)}"
        )

        for item in missing_fields:
            print(
                f"  Record {item['record']}: "
                f"{', '.join(item['missing'])}"
            )

    else:
        print(
            "Required fields: PASS"
        )

    duplicates = find_duplicate_message_ids(
        emails
    )

    if duplicates:
        print(
            f"Duplicate message IDs: "
            f"{len(duplicates)}"
        )

        for message_id in duplicates:
            print(
                f"  {message_id}"
            )

    else:
        print(
            "Duplicate message IDs: NONE"
        )

    empty_counts = count_empty_fields(
        emails
    )

    print("\nEmpty field counts:")

    for field, count in empty_counts.items():
        print(
            f"  {field}: {count}"
        )

    print(
        "\n========================================"
    )


if __name__ == "__main__":

    emails = load_emails()

    print_validation_report(emails)