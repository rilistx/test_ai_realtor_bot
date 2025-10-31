import gspread


SERVICE_ACCOUNT_FILE = "service_account.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1fA7gJoIC6a6acY9qjg7duEUB6aFHJolDX1N0uulVlW0/edit?gid=0"


def read_gsheet(sheet_name: str):
    gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
    sh = gc.open_by_url(SHEET_URL)
    worksheet = sh.worksheet(sheet_name)
    records = worksheet.get_all_records()

    return records
