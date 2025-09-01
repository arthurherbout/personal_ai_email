from personal_ai_email.gmail_client import GmailClient

if __name__ == "__main__":
    client = GmailClient().connect()
    emails = client.fetch_unseen(limit=5)
    for e in emails:
        print(f"\nFrom: {e['from']}")
        print(f"Subject: {e['subject']}")
        print(f"Body preview: {e['body'][:200]}")
    client.close()
