#  put stuff here to document how to work the program for future users and us
import PySimpleGUI as sg


def help_window():
    sg.theme('darkBlue1')
    top = [
        [sg.Text("Help window last updated 05/25/2022")],
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
                    [sg.Text("The gesture's data are uploaded to the firebase by user desire")]
                    ]

    settings = [[sg.Text(
        "The Settings sub-menu controls which camera is being used for input and output, debug mode and Hand Match Confidence")],
        [sg.Text("Use the dropdown menu to change the being camera used")],
        [sg.Text("Check debug mode to show the wireframe and uncheck to NOT show wireframe")],
        [sg.Text(
            "Hand Match Confidence will determine how rigorous the camera and the program will match the hand gesture (input a number between 0 to 1) a higher value will be more picky while a lower value will be loose with its certainty")]]

    reg_gesture = [[sg.Text("To register a gesture:")],
                   [sg.Text("1. Press the Start button to turn on the camera ")],
                   [sg.Text("2. Press Register Gesture. A window will popup, name the gesture, press confirm")],
                   [sg.Text(
                       "3. Hold up a gesture before the 5 second countdown finishes, that gesture will now be included in the profile window as a gesture to be added to a profile")]]

    profile = [[sg.Text("Profiles:")],
               [sg.Text(
                   "The profiles sub-menu contains various buttons that allow the creation and editting of profiles")],
               [sg.Text("As well as the capability to duplicate and delete profiles already created")],
               [sg.Text("Currently the Import from File button is not implemented")],
               [sg.Text(
                   "It would have allowed a file to be pulled and included in the program to allow an externally created profile to be used in your current program.")]
               ]

    action = [[sg.Text("From this sub-menu you can create action mappings to various files and shortcuts")],
              [sg.Text("Use the Open App button to create a path to a file to later map it in profiles")],
              [sg.Text("By either copy and pasting a file path or using the file explorer to map to that file")],
              [sg.Text("Use the Macros button to create a button shortcut")],
              [sg.Text(
                  "Press Record Macro then press a set of key(s) (like 'a' or 'ctrl+c') then press Stop Recording to capture the set of keys, then press submit to save it for a later profile mapping")],
              [sg.Text("Remember to hit Save after creating your actions!!")]]

    instructions = [[sg.TabGroup([[sg.Tab("Settings", settings),
                                   sg.Tab("Profiles", profile),
                                   sg.Tab("Register Gesture", reg_gesture),
                                   sg.Tab("Actions", action)
                                   ]],
                                 selected_background_color="DarkGreen",
                                 tab_background_color="Gray"
                                 )
                     ]]

    layout3 = [[sg.Text("Planned modes (unfortunately removed due to time constraints): ")],
               [sg.Text("Cursor mode: camera will track and control mouse cursor.")],
               [sg.Text("Two-Hands Mode: camera will track two hands")],
               [sg.Text("Combo Mode: Sequential combination of gestures leading to a mapped action")]
               ]

    Tabs = [[sg.Text("Set/create a profile with the mappings in a profile then just press Start to turn on camera to allow the gestures to be used for stuff")],
            [sg.TabGroup([[sg.Tab('Developer Details', developer, border_width=10,
                                  tooltip='Contact details for developers'),
                           sg.Tab("Program Details", prog_details, tooltip="Program specifics"),
                           sg.Tab('Instructions', instructions),
                           sg.Tab('Modes', layout3, tooltip='Info on Modes (NOT IMPLEMENTED)')]],
                         tab_location='center',
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
