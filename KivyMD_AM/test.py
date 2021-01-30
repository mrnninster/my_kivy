#  Kivy MD Imports
from kivymd.app import MDApp
from kivymd import icon_definitions
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
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
from PyFiles import AppFunctions


# Window Size
Window.size = (300, 500)


# Screen Manager
class ScreenManagement(ScreenManager):
    def log_in_scene(self, *args):
        self.current = "log_in_Screen"

    def sign_up_scene(self, *args):
        self.current = "sign_up_Screen"

    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        if os.path.exists("user.db"):
            Clock.schedule_once(self.log_in_scene, 3)
        else:
            Clock.schedule_once(self.sign_up_scene, 3)


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

    # def check(self, email, password):
    #     AppFunctions.sign_in_check(email, password)

    def submit_form(self, first_name, last_name, company, email, phone_number, regpassword, vregpassword, usecase):

        # Sign Up Error Checks
        try:

            # # Check For Empty Fields
            # required_fields = [first_name, last_name, email,
            #                    phone_number, regpassword, vregpassword, usecase]

            # for field in required_fields:
            #     res = AppFunctions.empty_check(field)
            #     if (res[0] == "Failed"):
            #         break

            # # Check Name Length
            # if (res[0] != "Failed"):
            #     res = AppFunctions.name_length(first_name, last_name)

            # # Check Phone Number
            # if (res[0] != "Failed"):
            #     res = AppFunctions.verify_phonenumber(phone_number)

            # # Verify User Identification Details
            # if (res[0] != "Failed"):
            #     res = AppFunctions.verify(email, regpassword)

            # if (res[0] != "Failed"):
            #     res = AppFunctions.same_password(regpassword, vregpassword)

            res = [""]
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
                    title="Sign Up Error", text=res[1], size_hint=[None, None], size=[200, 150]
                )
                dialog.open()

            elif(res[0] == "Success"):
                dialog = MDDialog(
                    text="Your Account Has Been Created", buttons=[MDRaisedButton(text="SIGN IN")], on_realease=Login_view_Screen, size_hint=[None, None], size=[200, 150],
                )
                dialog.open()
                # print("Making Request")
                # AppFunctions.register_user(
                #     first_name, last_name, company, email, phone_number, regpassword, vregpassword, usecase)
                # print("Request Completed")
                # MDSpinner(
                #     size_hint=(None, None),
                #     size=[46, 46],
                #     pos_hint={'center_x': .5, 'center_y': .5},
                #     active=True,
                #     palette=[
                #         [0.28627450980392155, 0.8431372549019608,
                #             0.596078431372549, 1],
                #         [0.3568627450980392, 0.3215686274509804,
                #             0.8666666666666667, 1],
                #         [0.8862745098039215, 0.36470588235294116,
                #             0.592156862745098, 1],
                #         [0.8784313725490196, 0.9058823529411765,
                #             0.40784313725490196, 1]
                #     ]
                # )


MainApp().run()
