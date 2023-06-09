import webbrowser
import pandas as pd
from prettytable import PrettyTable, SINGLE_BORDER
from collections import namedtuple
from LinkRunner.CustomClasses import Dict


def connect(machines: dict | Dict, target: str) -> bool:
    """Connects to a specified virtual machine."""
    print(f"\nOpening {target}...\n")
    webbrowser.open(machines[target])
    return True


def search(machines: dict | Dict, target=None) -> bool | str:
    """Performs a fuzzy search on a list of virtual machines."""
    if target is None:
        print("Which machine are you searching for? (enter nothing to skip)")
        search_query: str = input("Machine Name: ").upper()
    else:
        search_query: str = target.upper()
    if len(search_query) > 0:
        search_results: list[namedtuple] = machines.fuzz_keys(search_query)
        if len(search_results) > 1 and search_results[0].likeness == search_results[1].likeness:
            print(f"\nBe more specific!\n"
                  f"Did you mean {search_results[0].name}, or maybe {search_results[1].name}?\n")
            return False
        else:
            print(f"Selected VM: {search_results[0].name}")
            return search_results[0].name
    else:
        print("Moving on...\n")
        pass


def validate(search_result: bool | tuple) -> bool | None:
    """Validates the outcome of a VMHelper search."""
    if search_result is False:
        return False
    elif search_result is None:
        return None
    else:
        return True


def tabulate_dict(machines: dict | Dict, engine: str = "prettytable", target=None) -> PrettyTable | pd.DataFrame:
    """Prints a pandas DataFrame with tailored data - in this case, virtual machines."""
    if engine == "pandas":
        vm_df: pd.DataFrame = pd.DataFrame.from_dict({"VM Names": [k for k in machines.keys()],
                                                      "VM Links": [v for v in machines.values()]})
        print(vm_df.to_string())
        return vm_df
    elif engine == "prettytable":
        vm_table: PrettyTable = PrettyTable()
        vm_table.set_style(SINGLE_BORDER)
        vm_table.add_column(fieldname="VM Names",
                            column=[key for key in machines.keys()])
        vm_table.add_column(fieldname="VM Links",
                            column=[value for value in machines.values()])
        vm_table.align["VM Links"] = "l"
        print(vm_table)
        return vm_table
    else:
        raise ValueError(f"'{engine}' is not a valid engine type!")


def search_connect(machines: dict | Dict, target=None) -> bool | None:
    """Performs a VMHelper search and validates the result - suitable for search & connect loops."""
    _machines: dict = machines
    _target: None | str = target
    result: bool | str = search(machines=_machines, target=_target)
    validated_result = validate(result)
    if validated_result is False:
        return False
    elif validated_result is True:
        connect(machines=_machines, target=result)
        return True
    elif validated_result is None:
        return True
