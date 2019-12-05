from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
# class SignInScreen(Screen):
#    pass
Window.size = (480, 853)

class Container(BoxLayout):
    pass


class MainApp(App):
    def build(self):
        return Container()


if __name__ == '__main__':
    MainApp().run()
