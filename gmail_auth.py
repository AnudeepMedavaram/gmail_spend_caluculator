from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
OAUTH_PORT = 8080


def authenticate_gmail():
    creds = None

    # Reuse an existing token if we already authenticated
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # If credentials are missing or expired, authenticate again
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=OAUTH_PORT)

        # Save the token locally
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


if __name__ == "__main__":
    service = authenticate_gmail()

    profile = service.users().getProfile(
        userId="me"
    ).execute()

    print("Successfully connected to Gmail!")
    print("Email:", profile["emailAddress"])
    print("Total messages:", profile["messagesTotal"])