from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    id: str
    sender: str
    subject: str
    body: str
