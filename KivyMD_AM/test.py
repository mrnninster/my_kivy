#  Kivy MD Imports
from kivymd.app import MDApp
from kivymd import icon_definitions
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.material_resources import STANDARD_INCREMENT

# Kivy Imports
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition

# App Functions
from PyFiles import AppFunctions


# Window Size
Window.size = (300, 500)


# Screen Manager
class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
    #     Clock.schedule_once(self.transit_scene, 3)

    # def transit_scene(self, *args):
    #     self.current = "log_in_Screen"


# Screens
class Intro_view_Screen(Screen):
    pass


class Login_view_Screen(Screen):
    pass


class Signup_view_Screen(Screen):
    pass


class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return ScreenManagement()

    def check(self, email, password):
        AppFunctions.sign_in_check(email, password)

    def submit_form(self, first_name, last_name, company, email, phone_number, regpassword, vregpassword, usecase):

        # Sign Up Error Checks
        try:

            # Check For Empty Fields
            required_fields = [first_name, last_name, email,
                               phone_number, regpassword, vregpassword, usecase]

            for field in required_fields:
                res = AppFunctions.empty_check(field)
                if (res[0] == "Failed"):
                    break

            if (res[0] != "Failed"):
                res = AppFunctions.verify_phonenumber(phone_number)
                print(res)

        # Connectivity Error
        except Exception as e:
            print(str(e))
            dialog = MDDialog(
                title="Sign Up Fail", text="Something went wrong while signing you up, try again", size_hint=[None, None], size=[200, 150]
            )
            dialog.open()

        else:
            if(res[0] == "Failed"):
                dialog = MDDialog(
                    title="Sign Up Error", text=res[1], size_hint=[None, None], size=[200, 150]
                )
                dialog.open()


MainApp().run()
