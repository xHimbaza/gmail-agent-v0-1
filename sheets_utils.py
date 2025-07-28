import gspread
from google.oauth2.service_account import Credentials

# Define the required scope for Sheets access
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheets_client():
    """Authenticate and return a Google Sheets client."""
    creds = Credentials.from_service_account_file("key.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

def append_to_sheet(sheet_id, data_dict):
    """Append a row of startup data to the specified Google Sheet."""
    client = get_sheets_client()
    sheet = client.open_by_key(sheet_id).sheet1

    row = [
        data_dict.get("startup_name", ""),
        data_dict.get("sender_email", ""),
        data_dict.get("description", ""),
        data_dict.get("need", "")
    ]

    sheet.append_row(row)
