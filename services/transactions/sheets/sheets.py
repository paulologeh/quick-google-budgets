import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Sheets:
    def __init__(self) -> None:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            "sheets/credentials.json", scopes
        )  # access the json key you downloaded earlier
        # authenticate the JSON key with gspread
        self.client = gspread.authorize(credentials)
        self.transaction_types = {
            "EXPENSE": {
                "date": "B",
                "amount": "C",
                "description": "D",
                "category": "E",
            },
            "INCOME": {"date": "G", "amount": "H", "description": "I", "category": "J"},
        }

    def open_worksheet(self, sheet_name: str, worksheet: str) -> None:
        self.sheet = self.client.open(sheet_name).worksheet(worksheet)
        self.range_end = len(self.sheet.get_all_values()) + 1

    def clear_transactions(self) -> None:
        # clear from cell 5 to the length + 1
        self.sheet.batch_clear([f"B5:J{self.range_end}"])

    def bulk_write_transactions(
        self,
        _type: str,
        transactions: list[dict[str, float]],
        _format: list[str] = ["date", "amount", "description", "category"],
    ) -> None:

        if len(_format) != 4:
            raise ("Transaction format must have only 4 values")

        # find available row
        row = 5
        while row <= self.range_end:
            row_values = [
                self.sheet.acell(f"{self.transaction_types[_type][field]}{row}").value
                for field in self.transaction_types[_type]
            ]

            if not any(row_values):
                break

            row += 1

        # worksheet.update('A1:B2', [[1, 2], [3, 4]])
        all_values = [
            [
                transaction[_format[0]],
                transaction[_format[1]],
                transaction[_format[2]],
                transaction[_format[3]],
            ]
            for transaction in transactions
        ]

        for val in all_values:
            print(val)

        rows_end = len(all_values) + row

        if _type == "INCOME":
            self.sheet.update(f"G5:J{rows_end}", all_values)
        else:
            self.sheet.update(f"B5:E{rows_end}", all_values)

    def write_transaction(self, _type: str, **kwargs: str) -> None:
        # find available row
        row = 5
        while row <= self.range_end:
            row_values = [
                self.sheet.acell(f"{self.transaction_types[_type][field]}{row}").value
                for field in self.transaction_types[_type]
            ]

            if not any(row_values):
                break

            row += 1

        for field in _type:
            if field in kwargs:
                self.sheet.update(
                    f"{self.transaction_types[_type][field]}{row}", kwargs[field]
                )
