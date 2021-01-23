from kivymd.app import MDApp
from kivymd.material_resources import STANDARD_INCREMENT

from kivy.lang import Builder
from kivy.core.window import Window


# Window Size
Window.size = (300, 600)

KV = '''
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


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)


MainApp().run()
