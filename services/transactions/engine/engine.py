import csv
from .transaction import Transaction


def format_text(text: str) -> str:
    return text.encode("ascii", "ignore").decode().strip()


class Engine:
    def __init__(self, month: str = None) -> None:
        self.transactions = {"EXPENSE": [], "INCOME": []}
        self.month = month

    def get_transactions(self, *args: str, **kwargs: str) -> None:
        with open(kwargs["filename"]) as csvfile:
            data = csv.DictReader(csvfile, delimiter=",")
            for row in data:
                # initialise transaction
                transaction = Transaction(kwargs["bank"])
                transaction.set_transaction(*args, **row)
                bank_transaction = transaction.get_transaction()

                if f"/{self.month}/" in bank_transaction["date"]:
                    if bank_transaction["amount"] >= 0:
                        self.transactions["INCOME"].append(bank_transaction)
                    else:
                        bank_transaction["amount"] = abs(bank_transaction["amount"])
                        self.transactions["EXPENSE"].append(bank_transaction)
                else:
                    print(f"ignoring transaction {bank_transaction}")

    def get_monzo_transactions(self, filename: str) -> None:
        self.get_transactions(
            self,
            "Date",
            "Description",
            "Amount",
            "Category",
            "Name",
            "Type",
            filename=filename,
            bank="Monzo",
        )

    def get_santander_transactions(self, filename: str) -> None:
        self.get_transactions(
            self, "Date", "Description", "Amount", filename=filename, bank="Santander"
        )

    def get_aqua_transactions(self, filename: str) -> None:
        self.get_transactions(
            self, "Date", "Description", "Amount", filename=filename, bank="Aqua"
        )

    def sort_transactions(self) -> None:
        self.transactions["INCOME"] = sorted(
            self.transactions["INCOME"], key=lambda x: x["date"]
        )
        self.transactions["EXPENSE"] = sorted(
            self.transactions["EXPENSE"], key=lambda x: x["date"]
        )
