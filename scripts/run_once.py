from personal_ai_email.gmail_client import GmailClient
from personal_ai_email.modules import EmailClassificationModule
import dspy

if __name__ == "__main__":
    client = GmailClient().connect()

    lm = dspy.LM("ollama_chat/gemma:2b", api_base="http://localhost:11434", api_key="")
    dspy.configure(lm=lm)

    classifier = EmailClassificationModule()
    emails = client.fetch_unseen(limit=5)
    for e in emails:
        print(f"\nFrom: {e.sender}")
        print(f"Subject: {e.subject}")
        print(f"Body preview: {e.body[:200]}")
        response = classifier(email=e.__dict__)
        print(response.answer)

    client.close()
