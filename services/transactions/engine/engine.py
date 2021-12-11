import csv
from .transaction import Transaction


def format_text(text):
    return text.encode("ascii", "ignore").decode().strip()


class Engine:
    def __init__(self, month=None):
        self.transactions = []
        self.month = month

    def get_transactions(self, *args, **kwargs):
        with open(kwargs["filename"]) as csvfile:
            data = csv.DictReader(csvfile, delimiter=',')
            for row in data:
                # initialise transaction
                transaction = Transaction(kwargs["bank"])
                transaction.set_transaction(*args, **row)
                bank_transaction = transaction.get_transaction()

                if f"/{self.month}/" in bank_transaction["date"]:
                    self.transactions.append(bank_transaction)
                else:
                    print(f"ignoring transaction {bank_transaction}")

    def get_monzo_transactions(self, filename):
        self.get_transactions(self, "Date", "Description",
                              "Amount", "Name", "Type", filename=filename, bank="Monzo")

    def get_santander_transactions(self, filename):
        self.get_transactions(self, "Date", "Description",
                              "Amount", filename=filename, bank="Santander")

    def get_aqua_transactions(self, filename):
        self.get_transactions(self, "Date", "Description",
                              "Amount", filename=filename, bank="Aqua")

    def filter_internal_transfers(self):
        pass
