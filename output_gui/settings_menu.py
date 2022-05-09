import PySimpleGUI as sg


# window for settings menu
def settings_menu(global_vars, indexList):
    # Create list of valid indexes for cameras
    sources = indexList
    # List to hold stylized camera names for GUI
    displaySources = []
    # Create source names for display
    for item in sources:
        displaySources.append("Cam" + str(item))

    layout = [
        [sg.Text("Input Camera:", key="new")],
        [sg.Combo(displaySources, size=[10, 3], key="camIndex", default_value="Cam" + str(global_vars.get_camIndex())),
         sg.Checkbox("Debug Mode", default=global_vars.get_debugMode(), key="debug")],
        [sg.Text('Hand Match Confidence: '), sg.InputText(global_vars.get_confidenceLVL(), key='match')],
        [sg.Button(image_filename='Images/savebutton.png', key="Save"), sg.Button(image_filename='Images/cancelbutton.png', key="Cancel")]
    ]

    window = sg.Window("Settings", layout, modal=True, size=(300, 150))

    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        if event == "Save":
            # Capture selected element from Camera list element
            word = values["camIndex"]
            # Grab the index from list output (last character in output)
            global_vars.set_camIndex(int(word[-1:]))
            # Convert boolean to int (0 = false, 1 = True)
            global_vars.set_debugMode((values["debug"]))

            global_vars.set_confidenceLVL(values['match'])

            # Uploads current camera index to Firebase...
            # TODO: Maybe move this function to main? Not decided on here yet...
            # database.cameraUpload()
            break

    window.close()
