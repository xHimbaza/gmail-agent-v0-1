

import os
from dotenv import load_dotenv
from gmail_utils import get_gmail_service, get_unread_emails
from parse_email import extract_startup_info_with_gemini
from sheets_utils import append_to_sheet

# Replace with your actual Google Sheet ID (from the sheet URL)
load_dotenv()
SHEET_ID = os.getenv("SHEET_ID")

# Logging - Sheet ID
print(f"📄 Loaded SHEET_ID: {SHEET_ID}")

def main():
    # Logging - Gmail connection
    print("📬 Connecting to Gmail and fetching unread emails...")
    gmail_service = get_gmail_service()
    emails = get_unread_emails(gmail_service)
   
    print(f"📨 {len(emails)} unread emails found.")

    for email in emails:
        print(f"Processing email from: {email['from']}")
      
        print(f"📄 Email snippet:\n{email['body'][:200]}...")

        try:
            print("🤖 Sending to Gemini for parsing...")
            
            structured_data = extract_startup_info_with_gemini(email['body'])
            
            print("✅ Gemini response:")
            
            structured_data['sender_email'] = email['from']
            print("📤 Appending to Google Sheet...")
            
            append_to_sheet(SHEET_ID, structured_data)
            print("Appended to sheet.")
        except Exception as e:
            print(f"❌ Failed to process email: {e}")

if __name__ == "__main__":
    main()