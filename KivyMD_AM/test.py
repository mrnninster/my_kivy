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
""" Loading Screens """
class loader(Screen):
    pass


class log_in_loader(Screen):
    pass

""" Content Screens """
class Intro_view_Screen(Screen):
    pass


class Login_view_Screen(Screen):
    pass


class Signup_view_Screen(Screen):
    pass


class Reset_pass_Screen(Screen):
    pass


class Todays_view_Screen(Screen):
    pass


class MainApp(MDApp):
    def build(self):
        # Scren Widgets
        self.sm = ScreenManager(transition=NoTransition())
        self.sm.add_widget(loader(name="loader"))
        self.sm.add_widget(log_in_loader(name="log_in_loader"))
        self.sm.add_widget(Intro_view_Screen(name="intro_Screen"))
        self.sm.add_widget(Login_view_Screen(name="log_in_Screen"))
        self.sm.add_widget(Signup_view_Screen(name="sign_up_Screen"))
        self.sm.add_widget(Reset_pass_Screen(name="reset_pass_Screen"))
        self.sm.add_widget(Todays_view_Screen(name="todays_Screen"))
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


    """ User Log In Function take required variables 'email','password' """
    def check(self, email, password):

        # Login Loader Screen
        self.root.current = "log_in_loader"
        
        # Log User In
        try:
            check_response = AppFunctions.sign_in_check(email, password)

            if (check_response[0] == "Failed"):
                # Failed Response
                self.dialog = MDDialog(
                    type="alert",
                    title="Failed",
                    text=check_response[1],
                    size_hint=[None, None],
                    size=[250, 200],
                )
                self.dialog.open()

                # Remain At Log In Screen
                self.root.current = "log_in_Screen"

            elif(check_response[0] == "Success"):
                # User Info
                print(check_response[1])

                # Todays Page Data
                try:
                    # Check If User has logged In before
                    if (check_response[1][7] == 0):

                        try:
                            # Create Task Tables If Not
                            Task_Service = AppFunctions.Task_Table()

                        except:
                            # Failed Response
                            self.dialog = MDDialog(
                                type="alert",
                                text="SET UP FAILED",
                                size_hint=[None, None],
                                size=[250, 200],
                            )
                            self.dialog.open()

                            # Remain At Log In Screen
                            self.root.current = "log_in_Screen"

                        else:
                            # If system was Unable To Create DB Table
                            if (Task_Service[0] == "Failed"):

                                # Failed Response
                                self.dialog = MDDialog(
                                    type="alert",
                                    title="Failed",
                                    text=Task_Service[1],
                                    size_hint=[None, None],
                                    size=[250, 200],
                                )
                                self.dialog.open()

                                # Remain At Log In Screen
                                self.root.current = "log_in_Screen"
                        
                            else:

                                # Update The User Account Status To Signed In
                                status = AppFunctions.Status_Update(email,password)

                                if (status[0] == "Failed"):
                                    
                                    # Failed Response
                                    self.dialog = MDDialog(
                                        type="alert",
                                        title="Failed",
                                        text=status[1],
                                        size_hint=[None, None],
                                        size=[250, 200],
                                    )
                                    self.dialog.open()
                
                except Exception as e:
                    print(str(e))
                    self.root.current = log_in_Screen

                else:
                    print("Fetching Todays Tasks")
                    # # Fetch Tasks Stored On Mobile For Today
                    # Today_Local = AppFunctions.Today_Local()

                    # # Fetch Task Stored On Server For Today
                    # Today_Server = AppFunctions.Today_Server()

                    # # Redirect To User Landing Page
                    # self.root.current = "todays_Screen"

                    # # Sort and Display all Tasks For Today


        except:
            # Sign Up Exception Dialog Response
            self.dialog = MDDialog(
                type="alert",
                text="We are currently unable to sign you in.\nKindly contact support@agroai.farm for assistance.",
                size_hint=[None, None],
                size=[250, 200],
            )
            self.dialog.open()

            # Return To Log In Screen
            self.root.current = "log_in_Screen"

    


    """ User Registration Function, takes requored variables 'first_name', 'last_name', 'phone_number', 'email', 'regpassword', 'vregpassword' and 'usecase' and a Non required variable 'company' """
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
        except:
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
                try:
                    Req_res = AppFunctions.register_user(
                        first_name, last_name, company, email, phone_number, regpassword, vregpassword, usecase)
                except:
                    # Success Dialog Response
                    self.dialog = MDDialog(
                        type="alert",
                        text="Network Connection Failed",
                        size_hint=[None, None],
                        size=[250, 200],
                    )
                    self.dialog.open()

                    # Remain At Sign Up Screen
                    self.root.current = "sign_up_Screen"

                # When Connection Succeeds
                else:
                    # Print Request Response
                    Req_res = Req_res.json()

                    # Check Request Response
                    if Req_res["status"] == "Success":

                        # Create Local Storage
                        status = 0  # Defaults to not signed in
                        AppFunctions.create_db(first_name, last_name, company, email.lower(
                        ), phone_number, regpassword, usecase, status)

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



    """ Password Recovery Function, takes required password 'email' """
    def recover(self, email, *args):

        # Failed Dialog Response
        self.dialog = MDDialog(
            type="alert",
            text="A recovery email has been sent to you, kindly check your inbox.\n\nThanks.",
            size_hint=[None, None],
            size=[250, 200],
        )
        self.dialog.open()

        # Return to sign up Screen
        self.root.current = "log_in_Screen"


# Run App
if __name__ == "__main__":
    MainApp().run()
