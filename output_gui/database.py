import json
import profile

import firebase_admin
import globals
from firebase_admin import credentials
from firebase_admin import db


# Function to initalize the Database
def init():
    # Check to ensure app is not initalized
    if not firebase_admin._apps:
        cred = credentials.Certificate("datakey.json")
        default_app = firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://hands-off-d412d-default-rtdb.firebaseio.com/'})
        try:
            with open("global_vars.py"):
                pass
        except:
            i = 0
            databaseID = str(i)
            ref = db.reference(databaseID)
            while ref.get():
                i = i + 1
                databaseID = str(i)
                ref = db.reference(databaseID)
            stuff = repr(ref.get())
            with open('global_vars.py', 'w') as f:
                f.write(''.join(stuff))
                globals.Globals().firstTime(databaseID)

            f.close()
            defaultProf = profile.Profile("Empty_Profile", [])
            profile.write_profile_local(defaultProf)


# Function to upload the camera's current index to the Database
def cameraUpload():
    temp = globals.Globals()
    # Set reference position in DB
    ref = db.reference(temp.get_databaseID() + '/Cam')
    # Create a data set (dict) of camera index
    data_set = {"CamIndex": globals.get_camIndex()}
    # Convert dict into json format
    json_dump = json.dumps(data_set)
    # Create a json object
    json_obj = json.loads(json_dump)
    # No data exists for cameraIndex, set new child in DB
    if ref.get() is None:
        # Push json object to database
        ref.set(json_obj)
    # Data already exists, update existing child
    else:
        ref.update(json_obj)


# Function to get Camera index data from the database. Rough implementation
def cameraDownload():
    temp = globals.Globals()
    # Grab a reference in the camera index branch
    ref = db.reference(temp.get_databaseID() + '/Cam')
    # Get the children from /Cam
    datalist = ref.get()
    # Return the saved camera index
    return int(datalist['CamIndex'])


# Download profiles from the database and puts em somewhere
def download_profiles():
    # Clear the profiles file
    open('profiles.txt', 'w').close()
    # Grab reference at profile tree in DB
    temp = globals.Globals()
    ref = db.reference(temp.get_databaseID() + '/profiles')
    # Create an empty list to hold found profiles
    result = []
    # Get profiles from db
    datalist = ref.get()
    file = open("profiles.txt", "a")

    if datalist is not None:
        for key, value in datalist.items():
            file.write(key + "|" + json.dumps(value))
            file.write("\n")

    file.close()
    # return result


# Function to upload a profile to the DB

def profile_upload():
    # read profile objects from text file
    file = open("profiles.txt")
    for x in file:
        temp = x.split("|")
        # Split profiles into names and dictionaries
        key = temp[0]
        data = json.loads(temp[1])
        tempGlobal = globals.Globals()
        # Set reference in profiles as name
        ref = db.reference(tempGlobal.get_databaseID() + '/profiles/' + key)
        # Upload data as json
        ref.set(data)


# Function to remove a profile from the database and update local file
def profile_remove(name):
    temp = globals.Globals()
    ref = db.reference(temp.get_databaseID() + '/profiles/' + name)
    ref.delete()

    # Retrieves updated database and writes it to file again
    download_profiles()


def upload_test(data):
    ref = db.reference('/Jonathan')
    ref.update(
        {
            'Jonathan\'s-up test':
                {
                    'Global variables':
                        data
                }
        }
    )


def uploadGesture(currentGesture):
    # Put Database saving process in here
    # Set reference position in DB
    ref = db.reference('/test')
    # Create a data set (dict) of camera index
    data_set = {'Gesture Name': globals.globalGesture}
    # Convert dict into json format
    json_dump = json.dumps(data_set)
    # Create a json object
    json_obj = json.loads(json_dump)
    # No data exists for cameraIndex, set new child in DB
    if ref.get() is None:
        # Push json object to database
        ref.set(json_obj)
    # Data already exists, update existing child
    else:
        ref.update(json_obj)
    return


def getGestureList():
    # TODO: Put Database retrieval of gesture list here
    return


def upload_vars(data):
    temp = globals.Globals()
    ref = db.reference(temp.get_databaseID())
    ref.update(data)


#  pull global variables if the file does not exist locally
def download_vars(global_vars):
    ref = db.reference(global_vars.get_databaseID())
    # print("firebase stuff:" + str(ref.get()))
    stuff = repr(ref.get())
    with open('global_vars.py', 'w') as f:
        f.write(''.join(stuff))
    f.close()
