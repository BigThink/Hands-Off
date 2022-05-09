import os
import PySimpleGUI as sg
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import keyboard
import win32api


def media_control(value):
    code = win32api.MapVirtualKey(value, 0)
    win32api.keybd_event(value, code)


# takes a screenshot and saves into the default folder
def screenshot():
    keyboard.press_and_release("windows+printscreen")


# Set up Volume
# Get default audio device using PyCAW
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


# Volume scalar normalizes volume in a range from 0 - 1
# 0.01 change means a 1% change in volume
def increaseVolume():
    currentVolume = volume.GetMasterVolumeLevelScalar()
    volume.SetMasterVolumeLevelScalar(currentVolume + 0.01, None)


def decreaseVolume():
    currentVolume = volume.GetMasterVolumeLevelScalar()
    volume.SetMasterVolumeLevelScalar(currentVolume - 0.01, None)


# opens file explorer
def explorer():
    os.system('start ..')


# Needs error catching if file cannot be open
# Opens application at the file path specified
def openApp(filePath):
    os.startfile(filePath)


def action_gui(global_vars):
    macro = sg.Text("")
    file = sg.Text("")
    sg.theme("DarkBlue1")
    actions = ["Increase Volume", "Decrease Volume", "Mute", "Play/Pause Media", "Next Track",
               "Previous Track", "Stop Media", "Screenshot", "Open File Explorer"]
    layout = [[sg.Text('Choose Action', size=(20, 1))],
              [sg.Combo(actions, key="action", enable_events=True, readonly=True)],
              [sg.T("")],
              [sg.Button("Open App")],
              [file],
              [sg.T("")],
              [sg.Button("Macros")],
              [macro],
              [sg.T("")],
              [sg.Button("Cancel")],
              [sg.Button("Save")]]
    window = sg.Window('Action Mappings', layout, size=(600, 450))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "action":
            file.update(value='')
            macro.update(value='')
        elif event == "Open App":
            new_file = fileGUI(global_vars)
            if new_file != '':
                file.update(value=new_file)
                macro.update(value='')
                window.Element("action").update("")
        elif event == "Macros":
            new_macro = macroGUI(global_vars)
            if new_macro != '':
                macro.update(value=new_macro)
                file.update(value='')
                window.Element("action").update("")
        elif event == "Cancel":
            window.close()
        elif event == "Save":
            if macro.get() != "":
                global_vars.actions.append("macro" + macro.get())
            elif file.get() != "":
                global_vars.actions.append("file" + file.get())
            elif values["action"] != '':
                global_vars.actions.append(values["action"])
            window.close()


def macroGUI(global_vars):
    macro_string = sg.Text("      ")
    sg.theme("DarkBlue1")
    layout = [[sg.Button("Record Macro")], [macro_string], [sg.Button("Stop Recording")],
              [sg.T("")], [sg.Button("Submit")]]
    window = sg.Window('Recorded input', layout, size=(300, 250))
    macroStr = ''
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Record Macro":
            rec = []
            while not rec:
                keyboard.start_recording()
                while True:
                    event, values = window.read()
                    if event == sg.WIN_CLOSED or event == "Exit":
                        break
                    elif event == "Stop Recording":
                        rec = keyboard.stop_recording()

                        # data from the rec list is in key event format
                        # need to take out the names in a way that can be read and performed
                        finalRec = []
                        for key in rec:
                            if key.name not in finalRec:
                                finalRec.append(key.name)

                        # string is created in a format of key+key+key... that can be played

                        for str in finalRec:
                            macroStr = macroStr + str + '+'
                        macroStr = macroStr[:-1].lower()
                        macro_string.update(value=macroStr)

                        keyboard.unhook_all()
                        break

        elif event == "Stop Recording":
            window.close()
        elif event == "Submit":
            if macroStr == '':
                window.close()
                return ''
            else:
                window.close()
                return macroStr


def fileGUI(global_vars):
    sg.theme("DarkBlue1")
    layout = [[sg.T("")], [sg.Text("Choose App Location: "), sg.Input(), sg.FileBrowse(key="Input")],
              [sg.Button("Submit")]]
    window = sg.Window('File Browser', layout, size=(700, 250))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Submit":
            if values["Input"] == "":
                window.close()
            else:
                # load value into global vars actions list
                window.close()
                return values["Input"]


def perform_action(string):
    if string == "Increase Volume":
        if volume.GetMasterVolumeLevelScalar() < 100:
            increaseVolume()
    elif string == "Decrease Volume":
        if volume.GetMasterVolumeLevelScalar() > 0:
            decreaseVolume()
    elif string == "Mute":
        volume.SetMasterVolumeLevelScalar(0)
    elif string == "Play/Pause Media":
        media_control(0xB3)
    elif string == "Previous Track":
        media_control(0xB1)
    elif string == "Next Track":
        media_control(0xB0)
    elif string == "Stop Media":
        media_control(0xB2)
    elif string == "Screenshot":
        screenshot()
    elif string == "Open File Explorer":
        explorer()
    elif string[0:4] == "file":
        openApp(string[4:])
    elif string[0:5] == 'macro':
        keyboard.press_and_release(string[5:])
    else:
        keyboard.write(string)
