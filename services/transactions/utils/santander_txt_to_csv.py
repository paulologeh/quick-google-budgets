def convert_santander_text_to_csv(from_file: str, to_file: str) -> list:
    def format_text(text):
        return text.encode("ascii", "ignore").decode().strip()

    with open(to_file, "w+") as normalised_file:
        normalised_file.write("Date,Description,Amount\n")
        with open(from_file, 'r', encoding="ISO-8859-1") as bank_statement:
            statement = bank_statement.readlines()
            i = 0
            while i < len(statement):
                if "Date" in statement[i]:
                    date = format_text(statement[i].replace("Date:", ""))
                    description = format_text(
                        statement[i + 1].replace("Description:", "").replace(",", ""))
                    value = float(format_text(
                        statement[i + 2].replace("Amount:", "")))

                    normalised_file.write("%s,%s,%f\n" %
                                          (date, description, value))

                    i += 1
                i += 1
