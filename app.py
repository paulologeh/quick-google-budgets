import json
from engine.engine import Engine
from sheets.sheets import Sheets

# from utils.santander_txt_to_csv import convert_santander_text_to_csv

if __name__ == "__main__":
    with open("./rules.json", "r") as rules_files:
        rules = json.load(rules_files)

    with open("./config.json", "r") as config_json:
        configs = json.load(config_json)

    uploaded_statements = configs["uploaded_statements"]

    selected_months = int(configs["month"])

    # Get and process all transactions
    print("processing transactions")
    bank_engine = Engine(rules, selected_months)

    bank_engine.get_santander_transactions(uploaded_statements["Santander"])
    bank_engine.get_monzo_transactions(uploaded_statements["Monzo"])
    bank_engine.get_aqua_transactions(uploaded_statements["Aqua"])
    bank_engine.sort_transactions()

    spreadsheet_name = configs["spreadsheet"]
    worksheet_name = "Transactions"

    # Open the spreadsheet
    print("preparing worksheet")
    budget_sheets = Sheets()
    budget_sheets.open_worksheet(spreadsheet_name, worksheet_name)
    budget_sheets.clear_transactions()

    # Write the transactions to google sheets
    print("writing transactions")
    budget_sheets.bulk_write_transactions("INCOME", bank_engine.transactions["INCOME"])
    budget_sheets.bulk_write_transactions(
        "EXPENSE", bank_engine.transactions["EXPENSE"]
    )

    print("Done")
