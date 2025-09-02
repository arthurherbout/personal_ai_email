import email
import imaplib
from .config import IMAP_SERVER, GMAIL_USER, GMAIL_APP_PASSWORD
from email.header import decode_header
from .email import Email



class GmailClient:
    """
    Client that connects to Gmail.
    """

    def __init__(
        self,
        user: str = GMAIL_USER,
        password: str = GMAIL_APP_PASSWORD,
    ):
        self.user = user
        self.password = password
        self.imap_server = IMAP_SERVER

        self.mail = None

    def connect(self) -> GmailClient:
        self.mail = imaplib.IMAP4_SSL(self.imap_server)
        self.mail.login(self.user, self.password)
        self.mail.select('"[Gmail]/All Mail"')
        return self

    def close(self) -> None:
        """
        This closes the connection to the email server.
        """
        if self.mail:
            self.mail.logout()

    def fetch_email_by_eid(self, eid: str) -> Email:
        """
        This method fetches an email by its id.
        It returns an email object.
        """
        _, msg_data = self.mail.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # decode subject properly
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8", errors="ignore")

        # extract plain-text body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain" and not part.get(
                    "Content-Disposition"
                ):
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")
        return Email(
            id=eid.decode(), sender=msg.get("From"), subject=subject, body=body.strip()
        )

    def fetch_unseen(self, limit: int = 5) -> list[Email]:
        """
        Fetch unseen emails (latest first).
        """
        status, messages = self.mail.search(None, "UNSEEN")
        if status != "OK":
            return []

        email_ids = messages[0].split()
        email_ids = email_ids[-limit:] if limit else email_ids

        results = []
        for eid in email_ids:
            fetched_email = self.fetch_email_by_eid(eid=eid)
            results.append(fetched_email)
        return results
