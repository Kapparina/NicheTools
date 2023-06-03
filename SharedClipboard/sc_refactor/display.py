import shutil
from tabulate import tabulate


def terminal_dimensions():
    terminal_width = shutil.get_terminal_size()[0]
    return terminal_width


def tabulated_data(_data: dict):
    formatted_data: dict = {"KEY": [key for key in _data.keys()],
                            "VALUE": [value for value in _data.values()]}
    key_width = terminal_dimensions() * 0.10
    value_width = terminal_dimensions() * 0.70
    data_table = tabulate(formatted_data, headers=["KEYS", "VALUES"],
                          tablefmt="grid", maxcolwidths=[2, key_width, value_width],
                          showindex=[index for index, key in enumerate(data, 1)])
    return data_table


def view_all():
    if len(data.keys()) > 0:
        print(f"\n{tabulated_data(data)}\n")
    else:
        print("No values available to list!")