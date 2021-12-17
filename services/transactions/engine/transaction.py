from typing import Union
from .categories import (
    income_categories_mapping,
    expense_categories_mappings,
    description_knowledge,
)

CREDIT_CARDS = ["Aqua"]


class Transaction:
    def __init__(self, bank: str) -> None:
        self.data = {"bank": bank}

    def classify_transaction(self) -> None:
        if "category" not in self.data:
            if self.data["bank"] in CREDIT_CARDS:
                categories = (
                    description_knowledge["INCOME"]
                    if self.data["amount"] <= 0
                    else description_knowledge["EXPENSE"]
                )
            elif self.data["amount"] >= 0:
                categories = description_knowledge["INCOME"]
            else:
                categories = description_knowledge["EXPENSE"]

            found = False
            for category in categories:
                if any(
                    keyword.upper() in self.data["description"].upper()
                    for keyword in categories[category]
                ):
                    self.data["category"] = category
                    found = True
                    break

            if not found:
                self.data["category"] = "Other"

            return
        elif self.data["category"] in ["Transfers"]:
            return

        # map category
        if self.data["amount"] >= 0:
            categories = income_categories_mapping
        else:
            categories = expense_categories_mappings

        found = False
        for category in categories:
            if self.data["category"] in categories[category]:
                self.data["category"] = category
                found = True
                break

        if not found:
            self.data["category"] = "Other"

    def format_data(self) -> None:
        def format_description(data: dict) -> str:
            if (
                not data["description"]
                or data["description"].lower() == "none"
                or len(data["description"]) <= 4
                and data["bank"] == "Monzo"
            ):
                description = f"{data['name']} {data['type']}"
            else:
                description = data["description"]

            return (" ".join(description.split())).title()

        self.data["description"] = format_description(self.data)
        self.data["amount"] = float(self.data["amount"])

    def set_transaction(self, *args: str, **kwargs: Union[str, float]) -> None:
        for arg in args:
            if arg in kwargs:
                self.data.update({arg.lower(): kwargs[arg]})

        self.format_data()
        self.classify_transaction()

    def get_transaction(self) -> dict:
        return self.data
