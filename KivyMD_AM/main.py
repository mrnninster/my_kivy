from kivymd.app import MDApp
from kivymd import icon_definitions
from kivymd.material_resources import STANDARD_INCREMENT

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager


# Window Size
Window.size = (300, 600)

Intro = '''
Screen:
    Image:
        id: logo
        source: "assets/i4.jpg"
        size_hint: None, None
        size: 200, 50
        allow_stretch: True
        keep_ratio: False
        pos_hint: {"center_x" : 0.5}
        y : root.height * 0.8

    BoxLayout:
        id: Welcome
        orientation: "vertical"
        adaptive_size: True
        pos_hint: {"center_x": .5}

        MDLabel:
            theme_text_color: "Custom"
            text_color: 235/255, 235/255, 235/255, 0.7
            adaptive_size: True
            halign: "center"
            valign: "center"
            font_style: "H5"
            text: "ACTIVITY MANAGER"

        MDLabel:
            theme_text_color: "Custom"
            text_color: 235/255, 235/255, 235/255, 0.7
            adaptive_height: True
            halign: "center"
            font_style: "Button"
            text: "Powered By\\n AGRO AI"


'''
SignIn = """
Screen:
    GridLayout:
        id:sign_in_page 
        rows: 4

        MDLabel:
            theme_text_color: "Custom"
            text_color: 235/255, 235/255, 235/255, 0.7
            adaptive_size: True
            halign: "center"
            valign: "center"
            font_style: "H5"
            text: "SIGN IN"

        GridLayout:
            cols: 3
            rows: 2
            row_force_default: True
            row_default_height: 80
            
            MDLabel:
                adaptive_size: True
                halign: "center"
                valign: "center"


            MDTextField:
                hint_text: "Enter Email"
                size_hint_x:None
                width: 250
                icon_right: "account"
                theme_text_color: "Custom"
                text_color: 235/255, 235/255, 235/255, 0.7
            
            MDLabel:
                adaptive_size: True
                halign: "center"
                valign: "center"
            
            MDLabel:
                adaptive_size: True
                halign: "center"
                valign: "center"


            MDTextField:
                hint_text: "Password"
                size_hint_x:None
                width: 250
                icon_right: "account-key"
                theme_text_color: "Custom"
                text_color: 235/255, 235/255, 235/255, 0.7
            
            MDLabel:
                adaptive_size: True
                halign: "center"
                valign: "center"
            
        MDLabel:
            theme_text_color: "Custom"
            text_color: 235/255, 235/255, 235/255, 0.7
            adaptive_size: True
            halign: "center"
            valign: "center"
            font_style: "H5"
            text: "SIGN IN"

        GridLayout:
            cols: 2
            row_force_default: True
            row_default_height: 40
                
            MDLabel:
                theme_text_color: "Custom"
                text_color: 235/255, 235/255, 235/255, 0.7
                size_hint: root.center_x - dp(10), 50
                adaptive_size: True
                halign: "center"
                valign: "center"
                font_style: "Subtitle1"
                text: "SIGN UP"
            
            MDLabel:
                theme_text_color: "Custom"
                text_color: 235/255, 235/255, 235/255, 0.7
                size_hint: root.center_x + dp(10), 50
                adaptive_size: True
                halign: "center"
                valign: "center"
                font_style: "Subtitle1"
                text: "RESET PASSWORD"

    

"""


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(SignIn)


MainApp().run()
