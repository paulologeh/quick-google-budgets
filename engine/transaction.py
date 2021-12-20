from typing import Union

CREDIT_CARDS = ["Aqua"]


class Transaction:
    def __init__(self, rules: dict, bank: str) -> None:
        self.data = {"bank": bank}
        self.rules = rules

    def classify_transaction(self) -> None:
        if "category" not in self.data:
            if self.data["bank"] in CREDIT_CARDS:
                categories = (
                    self.rules["income"]["description_category"]
                    if self.data["amount"] <= 0
                    else self.rules["expense"]["description_category"]
                )
            elif self.data["amount"] >= 0:
                categories = self.rules["income"]["description_category"]
            else:
                categories = self.rules["expense"]["description_category"]

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
            categories = self.rules["income"]["category_category"]
        else:
            categories = self.rules["expense"]["category_category"]

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
