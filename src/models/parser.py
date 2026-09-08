import base64

from src.models.email import Email


def decode_body(data):
    """Decode a Gmail base64url encoded body."""

    if not data:
        return ""

    try:
        return base64.urlsafe_b64decode(data).decode(
            "utf-8",
            errors="replace"
        )
    except Exception:
        return ""


def get_headers(message):
    """Convert Gmail headers into a simple dictionary."""

    headers = message.get("payload", {}).get("headers", [])

    return {
        header["name"].lower(): header["value"]
        for header in headers
    }


def extract_body(payload):
    """
    Extract readable text from a Gmail message payload.
    Handles simple and multipart messages.
    """

    body = payload.get("body", {})

    if body.get("data"):
        return decode_body(body["data"])

    parts = payload.get("parts", [])

    text_parts = []

    for part in parts:
        mime_type = part.get("mimeType", "")

        if mime_type == "text/plain":
            data = part.get("body", {}).get("data")

            if data:
                text_parts.append(
                    decode_body(data)
                )

        elif mime_type.startswith("multipart/"):
            nested_body = extract_body(part)

            if nested_body:
                text_parts.append(nested_body)

    return "\n".join(text_parts)


def normalize_email(message):
    """
    Convert a raw Gmail API message
    into a Polaris Email object.
    """

    headers = get_headers(message)

    payload = message.get("payload", {})

    return Email(
        message_id=message.get("id", ""),
        thread_id=message.get("threadId", ""),
        sender=headers.get("from", ""),
        recipient=headers.get("to", ""),
        subject=headers.get("subject", ""),
        date=headers.get("date", ""),
        body=extract_body(payload),
        snippet=message.get("snippet", "")
    )