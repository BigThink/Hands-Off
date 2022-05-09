#  put stuff here to document how to work the program for future users and us
import PySimpleGUI as sg


def help_window():

    top = [
        [sg.Text("Help window last updated 05/07/2022")],
    ]

    body = [
        [sg.Text("This program was developed by Brian Vuong, Sam Blawski, "
                 "Dylan Watson, Jonathan Nguyen-Pham, Dening Zhang")],
        [sg.Text("Program was intended for use in our computer science senior project with the idea that "
                 "it is a program to map hand gestures to actions on a desktop; Windows and Mac compatibile")],
        [sg.Text("The main menu controls the majority of the functionality of the program")],
        [sg.Text("The programs capability to recognize a gesture or hand is best used with a solid light-colored background within a few feet (1/2 meter) of the camera")],
        [sg.Text("Including all the modes (unfortunately removed due to time constraints): ")],
        [sg.T("Cursor mode: camera will track and control mouse cursor.      Two-Hands Mode: camera will track two hands       "
              "Combo Mode: Sequential combination of gestures leading to a mapped action")],
        [sg.Text("The settings menu contains a listbox for camera input, a checkbox for the debug mode, and confidence value to control how positive the program will capture be when it sees a gesture.")],
        [sg.Text("The profiles contains profile mappings from the developers and allows for user created and duplicate profile")],
        [sg.Text("The register gesture button allows for gestures to be captured and named for later use")],
        [sg.Text("The gesture's data are uploaded to the firebase by user desire")],
        [sg.T("Developers's Email: brain.vuong@student.csulb.edu       sam.blawski@student.csulb.edu      "
              "dylan watson@student.csulb.edu      dening.zhang@student.csulb.edu  jonathan.NguyenPham@student.csulb.edu")]
    ]

    layout = [
        [sg.Column(top)],
        [sg.HorizontalSeparator()],
        [sg.Column(body)],
        [sg.Exit()]
    ]

    window = sg.Window("Help Window", layout, auto_size_text=True, auto_size_buttons=True)

    while True:
        event, values = window.read()

        # if user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == "Exit":
            break

    window.close()
