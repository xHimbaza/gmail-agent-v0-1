from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build 

# Scope for read-only Gmail access
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Authenticate and return a Gmail API service client."""
    creds = None

    # Look for existing token file (re-used access)
    if creds is None:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    service = build('gmail', 'v1', credentials=creds)
    return service


def get_unread_emails(service, max_results=10):
    """Fetch unread emails from inbox."""
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread', maxResults=max_results).execute()
    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_data['payload']['headers']
        body_snippet = msg_data.get('snippet', '')

        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')

        emails.append({
            'id': msg['id'],
            'subject': subject,
            'from': sender,
            'body': body_snippet
        })

    return emails