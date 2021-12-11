class Transaction:
    def __init__(self, bank):
        self.data = {"bank": bank}

    def classify_transaction(self):
        if "category" not in self.data:
            pass

    def format_data(self):
        def format_description(data):
            if (
                not data["description"] or
                data["description"].lower() == 'none' or
                len(data["description"]) <= 4 and
                data["bank"] == "Monzo"
            ):
                description = f"{data['name']} {data['type']}"
            else:
                description = data["description"]

            return (" ".join(description.split())).title()

        self.data["description"] = format_description(self.data)
        self.data["amount"] = float(self.data["amount"])

    def set_transaction(self, *args, **kwargs):
        for arg in args:
            if arg in kwargs:
                self.data.update({arg.lower(): kwargs[arg]})

        self.classify_transaction()
        self.format_data()

    def get_transaction(self) -> dict:
        return self.data
