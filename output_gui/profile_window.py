import PySimpleGUI as sg
import profile
import json
import database

# List to hold profile objects
profiles = []
# List to hold profile names
profile_names = []


# window for top most profile menu
def profile_menu(global_vars):
    profiles.clear()
    profile_names.clear()
    selectedprof = global_vars.get_selectedProf()

    # Fill list with profile objects
    file = open("profiles.txt")
    for x in file:
        temp = x.split("|")
        data = json.loads(temp[1])
        profiles.append(profile.Profile(temp[0], data))
        profile_names.append(temp[0])

    layout = [
        [sg.Text("Current Profile"), sg.DropDown(profile_names, key="selectedprof",
                                                 default_value=selectedprof, expand_x=True)],
        [sg.Button(key="Edit Profile", image_filename='Images/profileedit.png')],
        [sg.Button(key="Create Profile", image_filename='Images/profilecreate.png')],
        [sg.Button(key="Duplicate Profile", image_filename='Images/profiledup.png')],
        [sg.Button(key="Import Profile from File", image_filename='Images/profileimport.png')],
        [sg.Button(key="delete", image_filename='Images/profiledelete.png')],
        [sg.Button(key="Exit", image_filename='Images/exitbutton.png')]
    ]

    window = sg.Window("Hands-Off: Profiles", layout, modal=True, size=(400, 325), enable_close_attempted_event=True)

    while True:
        event, values = window.read()

        if event == "Exit" or event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
            global_vars.set_selectedProf(values["selectedprof"])
            break
        # press buttons to open these sub windows
        if event == "Edit Profile":
            edit_profile(values["selectedprof"], global_vars)

            index = len(profile_names) - 1
            window.Element("selectedprof").update(values=profile_names, set_to_index=index)

        if event == "Create Profile":
            create_profile(global_vars)
            index = len(profile_names) - 1
            window.Element("selectedprof").update(values=profile_names, set_to_index=index)

        # this option to duplicate profile to other username
        if event == "Duplicate Profile":
            duplicate_profile()
        if event == "Print":
            for x in profiles:
                if x.equals(values["selectedprof"]):
                    x.print_self()
        if event == "delete":
            name = values["selectedprof"]
            confirm = sg.popup_yes_no('Are you sure you want to delete ' + name + '?')

            if confirm == 'Yes':
                database.profile_remove(name)
                profile_names.remove(name)
                index = len(profile_names) - 1
                window.Element("selectedprof").update(values=profile_names, set_to_index=index)
            else:
                pass

    window.close()


# sub-window within profile window to edit profile stuff
def edit_profile(name_selected, global_vars):
    # Create a copy of selected profile to edit
    selected_prof_copy = profile.Profile("text", None)

    # Additional copy to retain selected profile's original state
    selected_prof = None
    if name_selected != 'Default':
        for obj in profiles:
            if obj.name == name_selected:
                selected_prof_copy.name = obj.name
                selected_prof_copy.new_mapping(obj.mapping)
                # Shallow copy, use as reference only
                selected_prof = obj

    # Default list of gestures and actions
    # TODO: Get these from somewhere. Passed in or global?
    gesture_list = list(global_vars.get_gestures().keys())
    action_list = global_vars.get_actions()

    map_display = []
    for item in selected_prof_copy.mapping.keys():
        map_display.append(item + " -> " + str(selected_prof_copy.mapping[item]))

    layout = [
        [sg.Text("Profile Name:", key="new"), sg.InputText(name_selected, key="name", tooltip="Edit profile name")],
        [sg.Button("Save Mapping", tooltip="Saves your mapping to the profile's list"),
         sg.Button("Select Mapping", tooltip="Moves selected mapping from the list to the editing box")],
        [sg.Combo(gesture_list, key="gestures", size=23, disabled=True),
         sg.Combo(action_list, key="actions", size=23, disabled=True)],
        [sg.Listbox(map_display, key="mapList", expand_x=True, expand_y=True, tooltip="List of profile's mappings")],
        [sg.Button("Save", tooltip="Saves your changes to the profile and exits."),
         sg.Cancel(tooltip="Close without saving.")]
    ]

    window = sg.Window("Edit Profile", layout, modal=True, size=(400, 500))

    # Prevent user from editing default profile
    # TODO: popup window to inform user
    if name_selected == 'Default':
        print("Cannot edit default profile!")
        window.close()

    while True:
        event, values = window.read()

        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        if event == "Save":
            database.profile_remove(selected_prof.name)
            selected_prof_copy.name = values["name"]
            profile.write_profile_local(selected_prof_copy)
            database.profile_upload()

            # Update window's values
            profiles.append(selected_prof_copy)
            profile_names.append(selected_prof_copy.name)
            profiles.remove(selected_prof)
            profile_names.remove(selected_prof.name)

            break
        if event == "Select Mapping":
            # Get mapping info from list
            text = values["mapList"][0]
            texts = text.split(" -> ")

            # Update UI elements with mapping information
            window.Element("gestures").update([texts[0]])
            window.Element("actions").update(disabled=False)
            window.Element("mapList").update(disabled=True)

        if event == "Save Mapping":
            # Get previous mapping
            old_map = values["mapList"]
            if len(old_map) > 0:
                old_map = values["mapList"][0]
                old_key_val = old_map.split(" -> ")

                # Get users new mapping
                new_map = values["actions"]
                # elements = new_map.split(", ")

                # Remove old mappings from profile obj and display list
                selected_prof_copy.delete_mapping(old_key_val[0])
                map_display.remove(old_map)

                # enter new mapping into profile obj and display list
                map_display.append(old_key_val[0] + " -> " + new_map)
                selected_prof_copy.add_mapping(old_key_val[0], new_map)

                # Update window elements
                window.Element("actions").update(disabled=True, value="")
                window.Element("gestures").update(value="")
                window.Element("mapList").update(map_display, disabled=False)

        if event == "remove":
            break  # TODO: code for removing from profile

    window.close()


# sub-window within profile window to create profiles
def create_profile(global_vars):
    # Grab list of gestures and actions available to the user
    gesture_list = list(global_vars.get_gestures().keys())
    action_list = global_vars.get_actions()

    # Create a list to hold mappings the user defines for the profile
    added_gestures = []
    added_actions = []

    # List to store text representations of mappings. Adding
    map_list = []

    layout = [
        [sg.Text("Profile Name:"), sg.InputText(key="name", tooltip="New profile's name")],
        [sg.Text("Link Gestures to System Actions", justification='center'),
         sg.Button("Create Mapping", key="create_gesture", tooltip="Add mapping to profile", size=15)],
        [sg.Combo(gesture_list, key="gestures", size=23), sg.Combo(action_list, key="actions", size=23)],
        [sg.Listbox(added_gestures, size=25, expand_y=True, key="listG", no_scrollbar=True),
         sg.Listbox(added_actions, size=25, expand_y=True, key="listA", no_scrollbar=True)],
        [sg.Button("Save", tooltip="Save and create profile"), sg.Cancel()]
    ]

    window = sg.Window("Create Profile", layout, modal=True, size=(400, 350))

    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        if event == "Save":
            # TODO: Warn user unnamed profiles not allowed
            if values["name"] != "" and len(added_gestures) > 0:
                p = profile.Profile(values["name"], None)
                # Add in gesture names from screen to dictionary
                for i in range(len(added_gestures)):
                    p.add_mapping(added_gestures[i], added_actions[i])

                profile.write_profile_local(p)
                database.profile_upload()
                profiles.append(p)
                profile_names.append(p.name)

                break

        if event == "create_gesture":

            new_ges = values["gestures"]
            new_act = values["actions"]

            # Ensure input is not blank
            if new_ges != "" and new_act != "":
                # Check that this gesture is not already mapped
                indexes = [i for i in range(len(added_gestures)) if added_gestures[i] == new_ges]

                if len(indexes) > 0:
                    # Remove old mapping if its found
                    added_gestures.pop(indexes[0])
                    added_actions.pop(indexes[0])

                # Add new valid mapping to lists
                added_gestures.append(new_ges)
                added_actions.append(new_act)
                # Update window elements
                window.Element("listA").update(values=added_actions)
                window.Element("listG").update(values=added_gestures)
                window.Element("gestures").update(value="")
                window.Element("actions").update(value="")

            else:
                print("Invalid mapping attempt")

    window.close()


# function to duplicate profile from the stored file list
def duplicate_profile():
    # user profile can be duplicated from drop down menu
    user_profile = ["Keith", "Bob", "Steve", "David"]
    # the list stored new username
    new_username = []
    layout = [
        # Todo: choose which stored file from drop down menu.
        [sg.Text("Choose which user profile to duplicate:")],
        [sg.DropDown(user_profile, default_value="stored profile here", expand_x=True)],
        [sg.Text("Enter the new user name:  ", size=(20, 1)), sg.InputText(key="name")],
        [sg.Button("Save", ), sg.Cancel()]
    ]

    window = sg.Window("Duplicate Profile", layout, modal=True, size=(400, 300))

    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        if event == "Save":
            if values != " ":
                # TODO: save the duplicated profile with new user name.
                # dropdown list for user profile fixed, but the new username need to matching with the old profile
                p = profile.Profile(values["name"], None)
                print("The Profile with new user name: " + p.name + " created")

            break

    window.close()
