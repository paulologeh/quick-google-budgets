import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Sheets:
    def __init__(self):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            "sheets/credentials.json", scopes
        )  # access the json key you downloaded earlier
        # authenticate the JSON key with gspread
        self.client = gspread.authorize(credentials)

    def open_worksheet(self, sheet_name="11. November", worksheet="Transactions"):
        self.sheet = self.client.open(sheet_name).worksheet(worksheet)
        self.range_end = len(self.sheet.get_all_values()) + 1

    def clear_transactions(self):
        # clear from cell 5 to the length + 1
        self.sheet.batch_clear([f"B5:J{self.range_end}"])

    def write_transaction(self, _type, **kwargs):
        if _type == "EXPENSE":
            _type = {
                "date": "B",
                "amount": "C",
                "description": "D",
                "category": "E"
            }

        if _type == "INCOME":
            _type = {
                "date": "G",
                "amount": "H",
                "description": "I",
                "category": "J"
            }

        # find available row
        row = 5
        while row <= self.range_end:
            row_values = [
                self.sheet.acell(f"{_type[field]}{row}").value
                for field in _type
            ]

            if not any(row_values):
                print(row_values, not any(row_values))
                break

            row += 1

        for field in _type:
            if field in kwargs:
                print(f"{_type[field]}{row}", kwargs[field])
                self.sheet.update(f"{_type[field]}{row}", kwargs[field])
