from gmail_utils import get_gmail_service, get_unread_emails

service = get_gmail_service()
emails = get_unread_emails(service)

for email in emails:
    print(email)