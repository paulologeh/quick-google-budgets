from typing import Union
from .categories import income_categories_mapping, expense_categories_mappings


class Transaction:
    def __init__(self, bank: str) -> None:
        self.data = {"bank": bank}

    def classify_transaction(self) -> None:
        if "category" not in self.data:
            self.data["category"] = ""

        else:
            # map category
            if self.data["amount"] >= 0:
                categories = income_categories_mapping
            else:
                categories = expense_categories_mappings

            for category in categories:
                if self.data["category"] in categories[category]:
                    print(f"{self.data['category']} -> {category}")
                    self.data["category"] = category

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
