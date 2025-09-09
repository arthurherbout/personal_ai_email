from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """
    This defines what an email is.
    """

    id: str
    sender: str
    subject: str
    body: str
