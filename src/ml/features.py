from collections.abc import Iterable


def email_to_text(subject: str = "", body: str = "") -> str:
    """Combine the email fields used by the ML baseline."""

    return f"{subject or ''} {body or ''}".strip()


def emails_to_text(emails: Iterable[dict[str, str]]) -> list[str]:
    """Convert email records into subject-plus-body text."""

    return [
        email_to_text(
            email.get("subject", ""),
            email.get("body", ""),
        )
        for email in emails
    ]