import cv2
from profile_window import *
from register_gestures import register_gesture
from settings_menu import settings_menu
from Help import help_window
import database
import globals
import mediapipe as mp
import profile
from action import action_gui
from action import perform_action


# top-most window that contains UI for other windows and functionalities
def main_menu(global_vars):
    # assign camera and mediapipe information to variables
    cap = cv2.VideoCapture(global_vars.get_camIndex())
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    # variable to save cooldown timer
    cooldown = 10

    # variable to indicate whether a gesture will be registered and for gesture's name
    toRegister = False

    # name of the gesture to be saved in database
    gestureName = None

    # gesture initialized to prevent it from going out of scope later - MAY NOT NEED
    gesture = {}

    # holds the currently selected profile object
    current_profile = get_current_profile(global_vars.get_selectedProf())

    # Call Camera Index function to pass to settings menu
    indexList = getCameraIndexes()
    sg.theme('DarkBlue1')  # Add a touch of color
    recording = False  # Boolean to keep track of whether we are recording

    tbar = [[sg.Button(tooltip="Place for settings stuff", key="settings", image_filename='Images/settingsbutton.png'),
             sg.Button(tooltip="Create and edit profiles", key="profile", image_filename='Images/profilebutton.png'),
             sg.Button(image_filename='Images/registerbutton.png',
                       tooltip="Press to register gesture to current profile", key="register"),
             sg.Button(image_filename='Images/capturebutton.png', key="capture", visible=False),
             sg.Button(image_filename='Images/actionbutton.png', key="Actions")],
            [sg.HSeparator(color="Black")],
            [sg.Image(filename='', key='image')]
            ]

    # All the stuff inside your window.
    layout = [
        [sg.Column(tbar)],
        [sg.HSeparator(color="Black")],
        [sg.Button(image_filename='Images/exitbutton.png', key="Exit"),
         sg.Button(image_filename='Images/startbutton.png', tooltip="Turn on camera", key="start"),
         sg.Button(image_filename='Images/stopbutton.png', tooltip="Stop camera feed", key="stop")],
        [sg.Button(image_filename='Images/helpbutton.png', tooltip="Where help has been known to be found", key="Help")]
    ]

    # Create the Window
    window = sg.Window("Hands-Off: Main", layout, auto_size_text=True, auto_size_buttons=True, icon='Images/logo.ico')

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read(timeout=5)

        # if user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == "Exit":
            database.profile_upload()
            break

        # button text strings are the default event returned when a button is clicked
        # press buttons to open other sub-function windows
        if event == "settings":
            settings_menu(global_vars, indexList)
            cap = cv2.VideoCapture(global_vars.get_camIndex())
        if event == "profile":
            profile_menu(global_vars)
            current_profile = get_current_profile(global_vars.get_selectedProf())

        if event == "start":
            # Tells program to start recording image
            recording = True
        if event == "Help":
            help_window()
        if event == "Actions":
            action_gui(global_vars)

        if event == "stop":
            cap.release()
            cap = cv2.VideoCapture(global_vars.get_camIndex())
            window['image'].update()
            recording = False

        if recording:
            # if user wants to register a gesture
            if event == "register":
                # gets name of gesture from register_gesture() method
                gestureName = register_gesture(global_vars.get_gestures())

                if gestureName is not None:
                    # popup to count down
                    popup()
                    toRegister = True

            success, image = cap.read()
            with mp_hands.Hands(
                    model_complexity=0,
                    min_detection_confidence=0.7,
                    min_tracking_confidence=0.5) as hands:
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False

                # Detections image colors BGR -> RGB
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    # If debug mode is toggled on from settings menu output landmarks
                    if global_vars.get_debugMode():
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                image,
                                hand_landmarks,
                                mp_hands.HAND_CONNECTIONS,
                                mp_drawing_styles.get_default_hand_landmarks_style(),
                                mp_drawing_styles.get_default_hand_connections_style())
                    # If debug mode is not toggled on from settings menu do not output landmarks
                    else:
                        for hand_landmarks in results.multi_hand_landmarks:
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS

                    # Saves landmark data to a dictionary
                    gesture = {
                        "wrist": [0, 0],
                        "thumb1": [float(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                   float(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y) - float(
                                       hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "thumb2": [float(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                   float(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y) - float(
                                       hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "thumb3": [float(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                   float(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y) - float(
                                       hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "thumb4": [float(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                   float(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y) - float(
                                       hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "index1": [float(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                   float(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y) - float(
                                       hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "index2": [float(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                   float(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y) - float(
                                       hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "index3": [float(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                   float(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y) - float(
                                       hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "index4": [float(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                   float(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y) - float(
                                       hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "middle1": [float(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                    float(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y) - float(
                                        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "middle2": [float(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                    float(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y) - float(
                                        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "middle3": [float(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                    float(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y) - float(
                                        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "middle4": [float(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                    float(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y) - float(
                                        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "ring1": [float(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                  float(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y) - float(
                                      hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "ring2": [float(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                  float(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y) - float(
                                      hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "ring3": [float(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                  float(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y) - float(
                                      hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "ring4": [float(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                  float(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y) - float(
                                      hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "pinky1": [float(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                   float(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y) - float(
                                       hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "pinky2": [float(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                   float(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y) - float(
                                       hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "pinky3": [float(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                   float(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y) - float(
                                       hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)],
                        "pinky4": [float(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x) - float(
                            hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x),
                                   float(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y) - float(
                                       hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)]
                    }

                # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                imgbytes = cv2.imencode('.png', cv2.flip(image, 1))[1].tobytes()
                window['image'].update(data=imgbytes)

                # Compare landmarks (if gesture is an empty dictionary it returns false)
                if bool(gesture):
                    # Iterates through keys of saved gestures from globals
                    for key in global_vars.get_gestures():
                        # If the gestures are similar enough based on confidence level
                        # and the program's cooldown timer is greater than 10
                        if compareLandmarks(gesture, global_vars.get_gestures()[key],
                                            global_vars.get_confidenceLVL()) and cooldown >= 10:
                            try:
                                print(current_profile.mapping[key])
                                perform_action(current_profile.mapping[key])
                            except:
                                pass
                            # Resets cooldown
                            cooldown = 0
                            break

                        # If the key is the last saved gesture
                        if key == list(global_vars.get_gestures())[-1]:
                            cooldown = cooldown + 1
                else:
                    cooldown = cooldown + 1

                # Captures gesture data and adds/updates associated global value
                if toRegister:
                    if not gesture == {}:
                        # Temporarily stores saved gestures
                        tempGestures = global_vars.get_gestures()

                        # Adds (or overwrites) gesture based on given information
                        tempGestures[gestureName] = gesture

                        # Updates global variable
                        global_vars.set_gestures(tempGestures)

                        # Resets flag for whether user wants to register gesture
                        toRegister = False

                # Resets gesture to an empty dictionary
                gesture = {}
    cap.release()
    cv2.destroyAllWindows()
    window.close()


# Function to check what indexes OpenCV detects are valid camera sources
def getCameraIndexes():
    # Check the first 5 indexes for camera sources
    index = 0
    results = []
    i = 5
    # Checks each index for a valid camera
    while i > 0:
        cap = cv2.VideoCapture(index)
        # If camera displays, add its index to valid list
        if cap.read()[0]:
            results.append(index)
            cap.release()
        index += 1
        i -= 1
    return results


def popup():
    sg.theme('darkBlack1')
    layout = [[sg.Text('3', pad=(25, 25), key='-COUNTER-')]]
    win = sg.Window('title', layout, no_titlebar=True, keep_on_top=True,
                    location=(1000, 400), margins=(50, 50),
                    return_keyboard_events=True)
    win.read(timeout=1000)
    win['-COUNTER-'].update(2)
    win.read(timeout=1000)
    win['-COUNTER-'].update(1)
    win.read(timeout=1000)
    win.Close()
    return


# Compares landmarks together
def compareLandmarks(currentGesture, savedGesture, confidence):
    # Initializing and acquiring list of keys in the dictionary
    currentKeyList = []
    savedKeyList = []
    for currentGestureKey in currentGesture:
        currentKeyList.append(currentGestureKey)
    for savedGestureKey in savedGesture:
        savedKeyList.append(savedGestureKey)

    # Loop to iterate through both gesture data dictionaries
    for i in range(len(currentKeyList)):
        if i == 0:
            continue
        for j in range(len(currentGesture[currentGestureKey])):
            # If the final saved gesture data is 0
            if (savedGesture[savedKeyList[i]][j] == 0) and \
                    i == len(currentKeyList) - 1 and j == len(currentGesture[currentGestureKey]) - 1:
                return False
            if savedGesture[savedKeyList[i]][j] == 0:
                continue

            # If the values are too close compare by a static value of .03
            if currentGesture[currentKeyList[i]][j] < .1 and savedGesture[currentKeyList[i]][j] < .1 and \
                    abs(abs(currentGesture[currentKeyList[i]][j]) - abs(savedGesture[savedKeyList[i]][j])) < .03:
                continue

            # Compare values with a given confidence level from globals
            elif abs((abs(currentGesture[currentKeyList[i]][j]) - abs(savedGesture[savedKeyList[i]][j])) /
                     savedGesture[savedKeyList[i]][j]) > (1 - float(confidence)):
                return False
            else:
                pass
    return True


def get_current_profile(name):
    # List to hold file's content
    profiles = []

    file = open("profiles.txt")
    for x in file:
        temp = x.split("|")
        data = json.loads(temp[1])
        profiles.append(profile.Profile(temp[0], data))

    name_selected = name

    selected_prof = None
    if name_selected != 'Default':
        for obj in profiles:
            if obj.name == name_selected:
                selected_prof = obj
    return selected_prof


# main method
if __name__ == "__main__":
    # Initalize global variables for use
    globs = 0
    try:
        with open("global_vars.py"):
            globs = globals.Globals()
    except FileNotFoundError:
        database.init()
        database.download_profiles()
        # database.download_vars(globs)
        globs = globals.Globals()
    database.init()
    database.download_profiles()
    main_menu(globs)
    database.upload_vars(globs.get_globals())  # upload global vars to firebase
    globs.write_globals()  # globals are stored in settings
