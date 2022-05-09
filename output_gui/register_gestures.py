import PySimpleGUI as sg


# window from main menu to register gestures
def register_gesture(gestureDict):
    layout = [
        [sg.Text('Enter the gesture\'s name here'), sg.InputText()],
        [sg.Button('Confirm', key="Confirm"), sg.Cancel()]
    ]

    returnValue = None

    # NOTE: modal = True prevents interaction with other windows but this one
    window = sg.Window("Gesture Name", layout, modal=False)

    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        if event == "Confirm":
            if values[0] != "" and values[0] not in gestureDict.keys():
                returnValue = values[0]
            else:
                sg.Window('Countdown', [[sg.T("Gesture Name is empty or exists already. Please try again.")]],
                          auto_close=True, auto_close_duration=2).read()
            break
    window.close()
    return returnValue
