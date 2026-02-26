import gspread
from google.oauth2.service_account import Credentials

def fetch_sheet_data():
    # scopes required to read sheets
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly"
    ]

    creds = Credentials.from_service_account_file(
        "credentials/service-account.json",
        scopes=scopes
    )

    client = gspread.authorize(creds)

    # Use your Sheet ID here
    sheet_id = "1f4zYZQ5BZwO6As2QbgsJb2UOvWFMNzrTz3hT5mGgtIU"
    sheet = client.open_by_key(sheet_id)

    # you can fetch specific tab like:
    worksheet = sheet.sheet1  # first tab
    data = worksheet.get_all_records()

    return data