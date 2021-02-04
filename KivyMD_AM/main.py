#  Kivy MD Imports
from kivymd.app import MDApp
from kivymd import icon_definitions
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.spinner import MDSpinner
from kivymd.material_resources import STANDARD_INCREMENT

# Kivy Imports
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition

# App Functions
import os
import json
from functools import partial
from PyFiles import AppFunctions


# Window Size
Window.size = (300, 500)


# Screens
class Intro_view_Screen(Screen):
    pass


class Login_view_Screen(Screen):
    pass


class Signup_view_Screen(Screen):
    pass


class Reset_pass_Screen(Screen):
    pass


class loader(Screen):
    pass


class MainApp(MDApp):
    def build(self):
        # Scren Widgets
        self.sm = ScreenManager(transition=NoTransition())
        self.sm.add_widget(Intro_view_Screen(name="intro_Screen"))
        self.sm.add_widget(Login_view_Screen(name="log_in_Screen"))
        self.sm.add_widget(Signup_view_Screen(name="sign_up_Screen"))
        self.sm.add_widget(Reset_pass_Screen(name="reset_pass_Screen"))
        self.sm.add_widget(loader(name="loader"))
        ssm = self.sm

        # Change Screen
        def change_screen(ssm, screen_name):
            ssm.current = screen_name

        # Log In Screen
        def log_in_scene(ssm, *args):
            ssm.current = "log_in_Screen"

        # Sign Up Screen
        def sign_up_scene(ssm, *args):
            ssm.current = "sign_up_Screen"

        # App Theme and title
        self.theme_cls.theme_style = "Dark"
        self.title = "Activity Manager"

        # On START
        self.sm.current = "intro_Screen"

        if os.path.exists("user.db"):
            Clock.schedule_once(partial(log_in_scene, ssm), 3)
        else:
            Clock.schedule_once(partial(sign_up_scene, ssm), 3)

        return ssm

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

            # Check Name Length
            if (res[0] != "Failed"):
                res = AppFunctions.name_length(first_name, last_name)

            # Check Phone Number
            if (res[0] != "Failed"):
                res = AppFunctions.verify_phonenumber(phone_number)

            # Verify User Identification Details
            if (res[0] != "Failed"):
                res = AppFunctions.verify(email, regpassword)

                # Check That both passwords are the same
                if (res[0] != "Failed"):
                    res = AppFunctions.same_password(regpassword, vregpassword)

            # On Verified Input
            if (res[0] != "Failed"):
                res = ["Success", "Please wait..."]

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
                    title="Sign Up Error", text=res[1], size_hint=[None, None], size=[250, 200]
                )
                dialog.open()

            elif(res[0] == "Success"):
                # Redirect To Loading Page
                self.root.current = "loader"

                # Make Sign Up Request To Server
                Req_res = AppFunctions.register_user(
                    first_name, last_name, company, email, phone_number, regpassword, vregpassword, usecase)

                # Print Request Response
                Req_res = Req_res.json()

                # Check Request Response
                if Req_res["status"] == "Success":

                    # Success Dialog Response
                    self.dialog = MDDialog(
                        type="alert",
                        title="Success",
                        text=Req_res["response"],
                        size_hint=[None, None],
                        size=[250, 200],
                    )
                    self.dialog.open()

                    # Switch To Log In Screen
                    self.root.current = "log_in_Screen"

                else:
                    # Failed Dialog Response
                    self.dialog = MDDialog(
                        type="alert",
                        title="Failed",
                        text=Req_res["response"],
                        size_hint=[None, None],
                        size=[250, 200],
                    )
                    self.dialog.open()

                    # Return to sign up Screen
                    self.root.current = "sign_up_Screen"


# Run App
if __name__ == "__main__":
    MainApp().run()
