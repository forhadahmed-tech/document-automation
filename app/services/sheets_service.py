import gspread
from google.oauth2.service_account import Credentials

def fetch_sheet_data():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly"
    ]

    creds = Credentials.from_service_account_file(
        "credentials/service-account.json",
        scopes=scopes
    )

    client = gspread.authorize(creds)

    sheet_id = "1f4zYZQ5BZwO6As2QbgsJb2UOvWFMNzrTz3hT5mGgtIU"
    sheet = client.open_by_key(sheet_id)

    # Fetch Sheet1 (Style Config)
    sheet1 = sheet.worksheet("Sheet1")
    style_data = sheet1.get_all_values()

    # Fetch Sheet2 (Content)
    sheet2 = sheet.worksheet("Sheet2")
    content_data = sheet2.get_all_records()

    return style_data, content_data