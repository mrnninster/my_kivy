import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

#################
### Functions ###
#################

# Function for Inner Layout Contents


def inner_grid_widget(self):
    # Page widget For First Name
    self.inner.add_widget(Label(text="First Name :"))
    self.first_name = TextInput(multiline=False)
    self.inner.add_widget(self.first_name)

    # Page widget For Last Name
    self.inner.add_widget(Label(text="Last Name :"))
    self.last_name = TextInput(multiline=False)
    self.inner.add_widget(self.last_name)

    # Page widget For Email
    self.inner.add_widget(Label(text="Email :"))
    self.email = TextInput(multiline=False)
    self.inner.add_widget(self.email)


###############
### Classes ###
###############

# Page Display
class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)

        # Page Division
        self.cols = 1

        # Inner Page Layout
        self.inner = GridLayout()
        self.inner.cols = 2

        # Inner Grid Widgets
        inner_grid_widget(self)

        # Append Inner Layout To Outer Layout
        self.add_widget(self.inner)

        # Page Button
        self.submit = Button(text="Submit", font_size=40)
        self.submit.bind(on_press=self.btn_click)
        self.add_widget(self.submit)

    # Button Click Function
    def btn_click(self, instances):
        first_name = self.first_name.text
        last_name = self.last_name.text
        Email = self.email.text
        print(f"Name is {first_name} {last_name} with an email of {Email}")
        self.first_name.text = ""
        self.last_name.text = ""
        self.email.text = ""


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
