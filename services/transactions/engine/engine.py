import csv
from .transaction import Transaction


CREDIT_CARDS = ["Aqua"]


class Engine:
    def __init__(self, rules: dict, months: list = []) -> None:
        self.transactions = {"EXPENSE": [], "INCOME": []}
        self.months = months
        self.rules = rules

    def get_transaction_type(self, transaction: dict) -> str:
        if transaction["bank"] in CREDIT_CARDS:
            # negative credit card transanctions are income
            if transaction["amount"] <= 0:
                return "INCOME"
            else:
                return "EXPENSE"
        else:
            if transaction["amount"] >= 0:
                return "INCOME"
            else:
                return "EXPENSE"

    def get_transactions(self, *args: str, **kwargs: str) -> None:
        with open(kwargs["filename"]) as csvfile:
            data = csv.DictReader(csvfile, delimiter=",")
            for row in data:
                # initialise transaction
                transaction = Transaction(self.rules, kwargs["bank"])
                transaction.set_transaction(*args, **row)
                bank_transaction = transaction.get_transaction()

                if self.is_internal_transfer(bank_transaction):
                    # print(f"ignoring internal transfer {bank_transaction}")
                    continue

                if any(
                    f"/{month}/" in bank_transaction["date"] for month in self.months
                ):
                    transaction_type = self.get_transaction_type(bank_transaction)
                    bank_transaction["amount"] = abs(bank_transaction["amount"])
                    self.transactions[transaction_type].append(bank_transaction)
                else:
                    pass
                    # print(f"ignoring out of month transanction {bank_transaction}")

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

    def is_internal_transfer(self, transaction: dict) -> bool:
        return (
            any(
                [
                    description.upper() in transaction["description"].upper()
                    for description in self.rules["internal_transfers"]["description"]
                ]
            )
            or any(
                [
                    category.upper() in transaction["category"].upper()
                    for category in self.rules["internal_transfers"]["category"]
                ]
            )
            or transaction["amount"] == 0
            or (
                transaction["description"] == "PAYMENT"
                and transaction["bank"] == "Aqua"
            )
        )
