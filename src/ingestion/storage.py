import json
from pathlib import Path

from src.models.email import Email


EMAILS_FILE = Path("data/raw/emails.jsonl")


def ensure_storage_directory():
    """
    Make sure the directory used for raw email storage exists.
    """

    EMAILS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )


def email_to_dict(email: Email) -> dict:
    """
    Convert an Email model into a JSON-serializable dictionary.
    """

    if hasattr(email, "model_dump"):
        return email.model_dump()

    if hasattr(email, "dict"):
        return email.dict()

    return {
        "message_id": email.message_id,
        "thread_id": email.thread_id,
        "sender": email.sender,
        "recipient": email.recipient,
        "subject": email.subject,
        "date": email.date,
        "body": email.body,
        "snippet": getattr(email, "snippet", ""),
    }


def load_existing_emails():
    """
    Load existing emails from the JSONL file.

    Returns:
        dict: message_id -> email dictionary
    """

    ensure_storage_directory()

    if not EMAILS_FILE.exists():
        return {}

    emails = {}

    with EMAILS_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            try:
                email = json.loads(line)

            except json.JSONDecodeError:
                continue

            message_id = email.get("message_id")

            if message_id:
                emails[message_id] = email

    return emails


def save_emails(emails):
    """
    Save emails to the JSONL file.

    Existing emails are preserved.

    Emails are identified by Gmail message_id, so running
    ingestion repeatedly will not create duplicate records.
    """

    ensure_storage_directory()

    existing_emails = load_existing_emails()

    added_count = 0
    updated_count = 0

    for email in emails:

        email_dict = email_to_dict(email)

        message_id = email_dict.get("message_id")

        if not message_id:
            continue

        if message_id in existing_emails:

            existing_emails[message_id] = email_dict
            updated_count += 1

        else:

            existing_emails[message_id] = email_dict
            added_count += 1

    with EMAILS_FILE.open(
        "w",
        encoding="utf-8"
    ) as file:

        for email in existing_emails.values():

            file.write(
                json.dumps(
                    email,
                    ensure_ascii=False
                )
                + "\n"
            )

    print(
        f"Added: {added_count}"
    )

    print(
        f"Updated: {updated_count}"
    )

    print(
        f"Total stored emails: {len(existing_emails)}"
    )

    print(
        f"\nSaved emails to:\n{EMAILS_FILE}"
    )