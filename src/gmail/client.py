from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

TOKEN_FILE = os.path.join(BASE_DIR, "token.json")


def get_gmail_service():
    """
    Create and return an authenticated Gmail API service.
    """

    creds = None

    # Load existing OAuth token
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    # Refresh expired credentials
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        raise RuntimeError(
            "Gmail authentication is missing or invalid. "
            "Run gmail_auth.py first."
        )

    return build(
        "gmail",
        "v1",
        credentials=creds
    )


def get_gmail_profile(service):
    """
    Return basic information about the authenticated Gmail account.
    """

    return (
        service.users()
        .getProfile(userId="me")
        .execute()
    )
def get_email(service, message_id):
    """
    Fetch a complete Gmail message by its ID.
    """

    return (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="full"
        )
        .execute()
    )