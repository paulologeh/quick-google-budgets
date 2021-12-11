from engine.engine import Engine
from sheets.sheets import Sheets
from utils.santander_txt_to_csv import convert_santander_text_to_csv

if __name__ == '__main__':
    # format non csv files
    convert_santander_text_to_csv(
        "./data/11_2021_Santander.txt", "./data/11_2021_Santander.csv")

    uploaded_statements = {
        "Santander": "./data/11_2021_Santander.csv",
        "Monzo": "./data/11_2021_Monzo.csv",
        "Aqua":  "./data/11_2021_Aqua.csv"
    }

    selected_month = "11"

    # Get and process all transactions
    bank_engine = Engine(selected_month)
    bank_engine.get_santander_transactions(uploaded_statements["Santander"])
    bank_engine.get_monzo_transactions(uploaded_statements["Monzo"])
    bank_engine.get_aqua_transactions(uploaded_statements["Aqua"])

    spreadsheet_name = "11. November"
    worksheet_name = "Transactions"

    # Open the spreadsheet
    budget_sheets = Sheets()
    budget_sheets.open_worksheet(spreadsheet_name, worksheet_name)
    budget_sheets.clear_transactions()

    # Write the transactions to google sheets
    for transaction in bank_engine.transactions:
        if transaction["amount"] > 0:
            budget_sheets.write_transaction("INCOME", **transaction)
        else:
            budget_sheets.write_transaction("EXPENSE", **transaction)
