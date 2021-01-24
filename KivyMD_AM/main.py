#  Kivy MD Imports
from kivymd.app import MDApp
from kivymd import icon_definitions
from kivymd.uix.button import MDRaisedButton
from kivymd.material_resources import STANDARD_INCREMENT

# Kivy Imports
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition


# Window Size
Window.size = (300, 600)


# Screen Manager
class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        Clock.schedule_once(self.transit_scene, 3)

    def transit_scene(self, *args):
        self.current = "log_in_Screen"


# Screens
class Intro_view_Screen(Screen):
    pass


class Login_view_Screen(Screen):
    pass


class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return ScreenManagement()

    def verify(self, email, password):
        print(email, password)


MainApp().run()
