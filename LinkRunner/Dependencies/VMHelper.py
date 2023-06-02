import webbrowser
import pandas as pd
from LinkRunner.CustomClasses import Dict


def connect(virtual_machines: dict | Dict, target: str) -> bool:
    """Connects to a specified virtual machine."""
    print(f"Opening {target}...")
    webbrowser.open(virtual_machines[target])
    return True


def search(virtual_machines: dict | Dict):
    """Performs a fuzzy search on a list of virtual machines."""
    print("\nWhich machine are you searching for?\n")
    search_query = input("Machine Name: ").upper()
    search_results: list[tuple] = virtual_machines.fuzz_keys(search_query)
    for index, result in enumerate(search_results):
        try:
            current_result = result
            next_result = search_results[index + 1]
            if search_results[0][1] == next_result[1]:
                print(f"\nBe more specific!\n"
                      f"Did you mean {search_results[0][0]}, or maybe {next_result[0]}?")
                return False
            else:
                print(f"Selected VM: {current_result[0]}")
                return current_result[0]
        except IndexError:
            pass


def validate(search_result: bool | tuple) -> bool:
    """Validates the outcome of a VMHelper search."""
    if search_result is False:
        return False
    else:
        return True


def view(virtual_machines: dict | Dict) -> pd.DataFrame:
    """Prints a pandas DataFrame with tailored data - in this case, virtual machines."""
    vm_df: pd.DataFrame = pd.DataFrame.from_dict({"VM Names": [k for k in virtual_machines.keys()],
                                                  "VM Links": [v for v in virtual_machines.values()]})
    print(vm_df.to_string())
    return vm_df


def search_connect(machines: dict | Dict) -> bool:
    """Performs a VMHelper search and validates the result - suitable for search & connect loops."""
    result = search(virtual_machines=machines)
    if validate(result) is False:
        return False
    else:
        connect(virtual_machines=machines, target=result)
        return True
