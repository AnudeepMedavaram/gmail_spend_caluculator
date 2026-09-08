from dataclasses import dataclass
from typing import Optional


@dataclass
class Email:
    message_id: str
    thread_id: str
    sender: str
    recipient: str
    subject: str
    date: str
    body: str
    snippet: Optional[str] = None