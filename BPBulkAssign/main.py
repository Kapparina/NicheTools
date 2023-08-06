import PySimpleGUI as psg

psg.theme("DarkAmber")

layout = [
    [psg.Text("Some text row 1")],
    [psg.Text("Enter something row 2"), psg.InputText()],
    [psg.Button("OK"), psg.Button("Cancel")]
]

window = psg.Window("Window Title", layout)

while True:
    event, values = window.read()

    if event == psg.WIN_CLOSED or event == "Cancel":
        break

    print(f"You entered {values[0]}")

window.close()
