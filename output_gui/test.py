import os
import unittest.mock
from unittest.mock import Mock
import globals
from output_gui.main import main_menu, getCameraIndexes, compareLandmarks
from output_gui.profile_window import profile_menu
from output_gui.register_gestures import register_gesture
from output_gui.settings_menu import settings_menu

globs = globals.Globals()


# place unit tests and other testing stuff below
# TODO: test functions names MUST begin with word "test" to be recognized as a test by Pycharm
class MyTestCase(unittest.TestCase):

    #   file existence tests below
    #   global vars file exist
    def test_globalvars_exists(self):
        location = os.path.exists("global_vars.py")
        if location:
            self.assertTrue("global_vars.py exists")
        else:
            self.assertFalse("global_vars.py does not exist")

    #   Firebase access key file exist
    def test_datakey_exists(self):
        location = os.path.exists("datakey.json")
        if location:
            self.assertTrue("datakey.json exists")
        else:
            self.assertFalse("datakey.json does not exist")

    #   output image directory
    def test_outputimages_exists(self):
        location = os.path.isdir("Images")
        if location:
            self.assertTrue("output images exists")
        else:
            self.assertFalse("output images does not exist")

    # button tests from main menu below
    def test_mainrun(self):
        try:
            mock = Mock(main_menu(globs), return_value=True)
            if mock.return_value:
                self.assertTrue("Main menu assertTrue fail")
            else:
                self.assertFalse("Main menu assertFail")
        except RuntimeError:
            self.assertFalse("Main menu failed to run")
        except ValueError:
            self.assertTrue("Main menu ran but did not want to run upload")

    # cursor mode test
    def test_cursorMode(self):
        if globs.get_cursorMode():
            self.assertTrue("cursor mode exists")

    # combination mode test
    def test_combinationMode(self):
        if globs.get_combination():
            self.assertTrue("Combination mode exists")

    # two-hand mode test
    def test_twohandMode(self):
        if globs.get_twoHand():
            self.assertTrue("Two-hand mode exists")

    # settings menu test
    def test_settingsrun(self):
        indexList = getCameraIndexes()
        try:
            mock = Mock(settings_menu(globs, indexList), return_value=True)
            if mock.return_value:
                self.assertTrue("Settings menu did not run")
            else:
                self.assertFalse("Settings menu assertFail")
        except RuntimeError:
            self.assertFalse("Main menu failed to run")

    # profiles menu test
    def test_profilerun(self):
        try:
            mock = Mock(profile_menu(globs), return_value=True)
            if mock.return_value:
                self.assertTrue("Profile menu assertTrue fail")
            else:
                self.assertFalse("Profile menu assertFail")
        except RuntimeError:
            self.assertFalse("Profile menu failed to run")

    # register menu test
    def test_registerrun(self):
        try:
            mock = Mock(register_gesture(globs.get_gestures()), return_value=True)
            if mock.return_value:
                self.assertTrue("Register gesture menu assertTrue fail")
        except RuntimeError:
            self.assertFalse("Register gesture menu failed to run")

    # compare landmarks test
    def test_compareLandmarks(self):
        try:
            mock = compareLandmarks(globs.get_gestures().get('Palm'), globs.get_gestures().get('Palm'),
                                    globs.get_confidenceLVL())
            if mock:
                self.assertTrue("Comparison fail assertTrue fail")
        except RuntimeError:
            self.assertFalse("Comapare landmarks failed to run")

    # register gesture truthy test
    def test_register_gesture(self):
        gestureReturn = register_gesture(globs.get_gestures())
        if gestureReturn:
            self.assertTrue("Something went wrong in truth case")
        else:
            self.assertFalse("Failed gesture entered already exists")

    # test for importing profiles
    def test_importprofiles(self):
        self.assertTrue("NOTHING HERE RIGHT NOW")

    # test for exporting profiles
    def test_exportprofiles(self):
        self.assertTrue("NOTHING HERE RIGHT NOW")


if __name__ == '__main__':
    unittest.main()
