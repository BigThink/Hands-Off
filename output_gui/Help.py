#  put stuff here to document how to work the program for future users and us
import PySimpleGUI as sg


def help_window():
    sg.theme('darkBlack1')
    top = [
        [sg.Text("Help window last updated 05/21/2022")],
    ]
    developer = [[sg.Text("This program was developed by Brian Vuong, Sam Blawski, "
                          "Dylan Watson, Jonathan Nguyen-Pham, Dening Zhang")],
                 [sg.T("Developers's Email: brain.vuong@student.csulb.edu       sam.blawski@student.csulb.edu      "
                       "dylan watson@student.csulb.edu      dening.zhang@student.csulb.edu  jonathan.NguyenPham@student.csulb.edu")]]

    prog_details = [[sg.Text("Program was intended for use in our computer science senior project with the idea that "
                             "it is a program to map hand gestures to actions on a desktop; Windows compatible (Mac is unstable)")],
                    [sg.Text("The main menu controls the majority of the functionality of the program")],
                    [sg.Text(
                        "The programs capability to recognize a gesture or hand is best used with a solid light-colored "
                        "background within a few feet (1/2 meter) of the camera")],
                    [sg.Text(
                        "The settings menu contains a listbox for camera input, a checkbox for the debug mode, and confidence "
                        "value to control how positive the program will be when capturing/recognizing a gesture.")],
                    [sg.Text(
                        "The profiles contains profile mappings from the developers and allows for user created and"
                        " duplicate profile")],
                    [sg.Text("The register gesture button allows for gestures to be captured and named for later use")],
                    [sg.Text("The gesture's data are uploaded to the firebase by user desire")]]

    instructions = [[sg.Text("To register a gesture:")],
                    [sg.Text("1. Press the Start button to turn on the camera ")],
                    [sg.Text("2. Press Register Gesture. A window will popup, name the gesture, press confirm")],
                    [sg.Text(
                        "3. Hold up a gesture before the 5 second countdown finishes, that gesture will now be included"
                        " in the profile window as a gesture to include in a profile")]]

    layout3 = [[sg.Text("Planned modes (unfortunately removed due to time constraints): ")],
               [sg.Text(
                   "Cursor mode: camera will track and control mouse cursor.      Two-Hands Mode: camera will track two hands       "
                   "Combo Mode: Sequential combination of gestures leading to a mapped action")]]

    Tabs = [[sg.TabGroup(
        [[sg.Tab('Developer Details', developer, border_width=10,
                 tooltip='Developer details'),
          sg.Tab("Program Details", prog_details),
          sg.Tab('Instructions', instructions),
          sg.Tab('Modes', layout3, tooltip='Info on modes (NOT IMPLEMENTED)')]], tab_location='centertop',
        tab_background_color='Gray', selected_title_color='Red',
        selected_background_color='DarkBlue', border_width=5)]]

    layout = [
        [sg.Column(top)],
        [sg.HorizontalSeparator()],
        [sg.Column(Tabs)],
        [sg.Exit()]
    ]

    window = sg.Window("Help Window", layout, auto_size_text=True, auto_size_buttons=True)

    while True:
        event, values = window.read()

        # if user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == "Exit":
            break

    window.close()
