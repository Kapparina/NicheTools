from prettytable import PrettyTable, SINGLE_BORDER


def tabulate_data(data: dict):
    table: PrettyTable = PrettyTable()
    table.set_style(SINGLE_BORDER)
    table.add_column(fieldname="KEYS",
                     column=[key for key in data.keys()])
    table.add_column(fieldname="VALUES",
                     column=[value for value in data.values()])
    table.align["VALUES"] = "l"
    return table
