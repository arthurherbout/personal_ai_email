import email
import imaplib
from .config import IMAP_SERVER, GMAIL_USER, GMAIL_APP_PASSWORD
from email.header import decode_header


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

    def close(self):
        if self.mail:
            self.mail.logout()

    def fetch_unseen(self, limit: int = 5) -> list[dict]:
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
            results.append(
                {
                    "id": eid.decode(),
                    "from": msg.get("From"),
                    "subject": subject,
                    "body": body.strip(),
                }
            )
        return results
