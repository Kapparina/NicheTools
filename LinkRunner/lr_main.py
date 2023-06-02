from LinkRunner.CustomClasses import Command, Dict
from LinkRunner.Dependencies import DataHelper, DictHelper, VMHelper

# noinspection SpellCheckingInspection
vm_links: Dict = DataHelper.get_data(_url=r"file://melcorpsmb.apac.linkgroup.corp/BluePrism/SmartAuto/"
                                          r"Process%20On%20Demand/Data/RPAVMLinks.html")
vm_links = Dict(DictHelper.dict_cleanup(data=vm_links, target=r"LG | VB"))
# noinspection SpellCheckingInspection
vm_links.pop(vm_links.find_key(value="file://melcorpsmb.apac.linkgroup.corp/BluePrism/SmartAuto/"
                                     "Process%20On%20Demand/data/HUD/Dashboard_HUD_1.html"))


def view(virtual_machines: dict):
    VMHelper.view(virtual_machines=virtual_machines)
    return True


def connect(virtual_machines: dict):
    connection_attempt = False
    while connection_attempt is False:
        connection_attempt = VMHelper.search_connect(machines=virtual_machines)
    else:
        print("Connected!")
        return True


def main():
    # noinspection SpellCheckingInspection
    commands: Command = Command(
        cmd_list=Dict({
            "view": view,
            "run": connect,
        })
    )

    print("What would you like to do?\n\t"
          "'view' : View a list of available Virtual Machines.\n\t"
          "'run' : Connect to a specific Virtual Machine.\n")
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() != "quit":
                commands.cmd_list[user_input.lower()](vm_links)
            else:
                break
        except KeyError:
            print("You can choose from the following:\t",
                  *commands.cmd_list.keys(), sep="\n\t")


if __name__ == "__main__":
    main()
