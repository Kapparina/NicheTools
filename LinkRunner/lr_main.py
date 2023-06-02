from LinkRunner.CustomClasses import Command, Dict
from LinkRunner.Dependencies import DataHelper, DictHelper, VMHelper

# noinspection SpellCheckingInspection
url: str = r"file://melcorpsmb.apac.linkgroup.corp/BluePrism/SmartAuto/Process%20On%20Demand/Data/RPAVMLinks.html"
vital_prefix: str = "vmrc"


# ---------------------- Start of Helper Functions ----------------------
def view(virtual_machines: dict) -> bool:
    """VMHelper.view() prints the virtual_machines parameter in either a PrettyTable or pandas DataFrame."""
    print("/* Behold: Tabulated data!\n")
    VMHelper.view(machines=virtual_machines, engine="prettytable")
    return True


def connect(virtual_machines: dict) -> bool:
    """VMHelper's search_connect() function wrapped in a while loop."""
    print("/* Initiating remote connection routine...")
    connection_attempt: bool = False
    while connection_attempt is False:
        connection_attempt = VMHelper.search_connect(machines=virtual_machines)
    else:
        print("/* Connected!")
        return True
# ----------------------- End of Helper Functions -----------------------


def startup() -> Dict:
    """Function runs on startup; retrieves, cleans and returns necessary data."""
    hyperlinks = DataHelper.get_data(url=url)
    hyperlinks_clean_keys = DictHelper.dict_cleanup(data=hyperlinks,
                                                    target=r"LG | VB")
    offensive_values: list = [v for v in hyperlinks_clean_keys.values() if not v.startswith(vital_prefix)]
    hyperlinks_filtered = Dict(DictHelper.filter_values(data=hyperlinks_clean_keys,
                                                        values=offensive_values))
    return hyperlinks_filtered


def main() -> None:
    print("/* Welcome to LinkRunner 2049 - Fetching links...")
    vm_links: Dict = startup()
    print("/* Data aggregation complete!\n")
    commands: Command = Command(
        cmd_list=Dict({
            "view": view,  # Keys can be customized, altering the options available to the user.
            "run": connect,  # Values are to be function names. For simplicity, all functions take the same argument.
        })
    )

    print("/* What would you like to do?\n\t"
          "'view': View a list of available Virtual Machines.\n\t"
          "'run': Connect to a specific Virtual Machine.\n")
    while True:
        try:
            user_input: str = input("> ")
            if user_input.lower() != "quit":
                commands.cmd_list[user_input.lower()](vm_links)
            else:
                break
        except KeyError:
            print("/* You can choose from the following:\t",
                  *commands.cmd_list.keys(), sep="\n\t")


if __name__ == "__main__":
    main()
