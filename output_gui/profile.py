

# Class to represent profile data in system
import json


# Function to write a profile into the profiles.txt
def write_profile_local(p):
    file = open("profiles.txt", "a")
    file.write(p.name + "|" + json.dumps(p.mapping) + "\n")


class Profile:

    # Constructor that accepts dictionaries
    def __init__(self, name, mapping):
        self.name = name
        if mapping is None:
            # Load in values after this!
            self.mapping = {}
        else:
            self.mapping = mapping.copy()

    # Function to change a specific mapping in the gesture/action dict
    # Key is the key we want to change, action is the value being changed
    def change_mapping(self, key, action):
        # Check if key is actually in dictionary
        result = self.mapping.get(key, -1)
        # If an index is returned, valid key
        if result == -1:
            # Invalid index, print error to console
            print("Invalid key given")
        else:
            # Change value at key
            self.mapping["key"] = action

    # Function to allow mappings to be completly replaced by a new dictionary
    def new_mapping(self, dictionary):
        self.mapping = dictionary.copy()

    # function to add additional mappings to the dictionary
    # TODO: type check 'action' once we have system action type defined
    def add_mapping(self, key, action):
        self.mapping[key] = action

    # Function to remove a mapping from the dict
    def delete_mapping(self, key):
        # Check if key is actually in dictionary
        result = self.mapping.get(key, -1)
        # If an index is returned, valid key
        if result == -1:
            # Invalid index, print error to console
            print("Invalid key given")
        else:
            # remove given key from dict
            self.mapping.pop(key)

    def equals(self, name):
        return self.name == name

    def print_self(self):
        print(self.name)
        print(self.mapping)
