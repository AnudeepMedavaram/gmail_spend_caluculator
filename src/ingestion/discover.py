from src.gmail.client import get_gmail_service, get_email
from src.models.parser import normalize_email
from src.ingestion.storage import save_emails


def search_emails(service, query, max_results=20):
    """
    Search Gmail and return message metadata.
    """

    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            q=query,
            maxResults=max_results
        )
        .execute()
    )

    return response.get("messages", [])


def discover_spending_emails(service, max_results=20):
    """
    Discover emails that may contain spending information.
    """

    query = (
        "receipt OR invoice OR payment OR purchase "
        "OR order OR subscription OR transaction"
    )

    return search_emails(
        service,
        query,
        max_results
    )


def fetch_and_normalize_emails(service, messages):
    """
    Fetch Gmail messages and convert them
    into normalized Polaris Email objects.
    """

    emails = []

    for message in messages:

        message_id = message["id"]

        try:
            raw_email = get_email(
                service,
                message_id
            )

            email = normalize_email(
                raw_email
            )

            emails.append(email)

        except Exception as error:

            print(
                f"Failed to process "
                f"{message_id}: {error}"
            )

    return emails


if __name__ == "__main__":

    MAX_EMAILS = 20

    service = get_gmail_service()

    messages = discover_spending_emails(
        service,
        max_results=MAX_EMAILS
    )

    print(
        f"Discovered {len(messages)} "
        f"candidate emails"
    )

    emails = fetch_and_normalize_emails(
        service,
        messages
    )

    print(
        f"Successfully normalized "
        f"{len(emails)} emails"
    )

    save_emails(emails)

    print(
        "\nSaved normalized emails to:"
    )

    print(
        "data/raw/emails.jsonl"
    )