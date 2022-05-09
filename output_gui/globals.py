# File to hold global variables in one location


class Globals:
    def __init__(self):
        try:
            content = open("global_vars.py", 'r').read()
            remove_chars = ":,{}[]'''"
            for chars in remove_chars:
                content = content.replace(chars, " ")
            content = content.split()

            # pop out the global variables read and save them in their variables
            while content:
                #  camera index load
                content.pop(0)
                self.camIndex = int(content.pop(0))
                content.pop(0)
                if content[0] == "True":
                    self.debugMode = True
                else:
                    self.debugMode = False
                content.pop(0)
                content.pop(0)
                if content[0] == "True":
                    self.cursor_mode = True
                else:
                    self.cursor_mode = False
                content.pop(0)
                content.pop(0)
                if content[0] == "True":
                    self.two_hand_mode = True
                else:
                    self.two_hand_mode = False
                content.pop(0)
                content.pop(0)
                if content[0] == "True":
                    self.combination_mode = True
                else:
                    self.combination_mode = False
                content.pop(0)

                #  DatabaseID load
                content.pop(0)
                self.databaseID = content.pop(0)

                #  selected prof load
                content.pop(0)
                self.selected_prof = content.pop(0)

                #  confidence level load
                content.pop(0)
                self.confidenceLVL = float(content.pop(0))

                #  actions list
                self.actions = []
                content.pop(0)
                while content[0] != "gestures":
                    self.actions.append(content.pop(0))

                #  gestures load
                content.pop(0)
                self.gestures = {}
                while content:
                    name = content.pop(0)
                    gesture = {}
                    i = 0  # after grabbing all 21 landmark points get the next named gesture
                    while i < 21:
                        part = content.pop(0)
                        xLoc = float(content.pop(0))
                        yLoc = float(content.pop(0))
                        gesture[part] = [xLoc, yLoc]
                        i += 1
                    self.gestures[name] = gesture

        except FileNotFoundError:
            print("global_vars.py does not exist")

    def firstTime(self, x):
        self.databaseID = x
        self.camIndex = 0
        self.debugMode = True
        self.cursor_mode = False
        self.two_hand_mode = False
        self.combination_mode = False
        self.selected_prof = "Default"
        self.confidenceLVL = 0.7
        self.gestures = {'Palm': {'wrist': [0.0, 0.0], 'thumb1': [0.0, 0.0], 'thumb2': [0.0, 0.0], 'thumb3': [0.0, 0.0], 'thumb4': [0.0, 0.0], 'index1': [0.0, 0.0], 'index2': [0.0, 0.0], 'index3': [0.0, 0.0], 'index4': [0.0, 0.0], 'middle1': [0.0, 0.0], 'middle2': [0.0, 0.0], 'middle3': [0.0, 0.0], 'middle4': [0.0, 0.0], 'ring1': [0.0, 0.0], 'ring2': [0.0, 0.0], 'ring3': [0.0, 0.0], 'ring4': [0.0, 0.0], 'pinky1': [0.0, 0.0], 'pinky2': [0.0, 0.0], 'pinky3': [0.0, 0.0], 'pinky4': [0.0, 0.0]}}
        self.actions = ["Increase Volume", "Decrease Volume", "Mute", "Play/Pause Media", "Previous Track", "Next Track", "Stop Media", "Screenshot", "Open File Explorer"]
        storage = {"camIndex": self.get_camIndex(), "debugMode": self.get_debugMode(),
                   "cursor_mode": self.get_cursorMode(), "two_hand_mode": self.get_twoHand(),
                   "combination_mode": self.get_combination(), "databaseID": self.get_databaseID(),
                   "selected_prof": self.get_selectedProf(), "confidenceLVL": self.get_confidenceLVL(),
                   "actions": self.get_actions(),
                   "gestures": self.get_gestures()}

        stuff = repr(storage)
        with open('global_vars.py', 'w') as f:
            f.write(''.join(stuff))
        f.close()

    def get_camIndex(self):
        return self.camIndex

    def set_camIndex(self, x):
        self.camIndex = x

    def get_debugMode(self):
        return self.debugMode

    def set_debugMode(self, x):
        self.debugMode = x

    def get_cursorMode(self):
        return self.cursor_mode

    def set_cursorMode(self, x):
        self.cursor_mode = x

    def get_twoHand(self):
        return self.two_hand_mode

    def set_twoHand(self, x):
        self.two_hand_mode = x

    def get_combination(self):
        return self.combination_mode

    def set_combination(self, x):
        self.combination_mode = x

    def get_selectedProf(self):
        return self.selected_prof

    def set_selectedProf(self, p):
        self.selected_prof = p

    def get_databaseID(self):
        return self.databaseID

    def set_databaseID(self, x):
        self.databaseID = x

    def get_confidenceLVL(self):
        return self.confidenceLVL

    def set_confidenceLVL(self, x):
        self.confidenceLVL = x

    def get_gestures(self):
        return self.gestures

    def set_gestures(self, x):
        self.gestures = x

    def get_actions(self):
        return self.actions

    # set actions as some list of strings
    def set_actions(self, x):
        self.actions = [x]

    def write_globals(self):
        storage = {"camIndex": self.get_camIndex(), "debugMode": self.get_debugMode(),
                   "cursor_mode": self.get_cursorMode(), "two_hand_mode": self.get_twoHand(),
                   "combination_mode": self.get_combination(), "databaseID": self.get_databaseID(),
                   "selected_prof": self.get_selectedProf(), "confidenceLVL": self.get_confidenceLVL(),
                   "actions": self.get_actions(),
                   "gestures": self.get_gestures()}

        stuff = repr(storage)
        with open('global_vars.py', 'w') as f:
            f.write(''.join(stuff))
        f.close()

    # used to write into database right now
    def get_globals(self):
        return {"camIndex": self.get_camIndex(), "debugMode": self.get_debugMode(),
                "cursor_mode": self.get_cursorMode(),
                "two_hand_mode": self.get_twoHand(), "combination_mode": self.get_combination(),
                "databaseID": self.get_databaseID(),
                "selected_prof": self.get_selectedProf(), "confidenceLVL": self.get_confidenceLVL(),
                "actions": self.get_actions(),
                "gesture": self.get_gestures()}
