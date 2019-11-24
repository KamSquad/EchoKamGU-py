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
    layout = BoxLayout(spacing=10)
    btn1 = Button(text='Hello', size_hint=(.7, 1))
    btn2 = Button(text='World', size_hint=(.3, 1))
    layout.add_widget(btn1)
    layout.add_widget(btn2)
    pass


class MainApp(App):
    def build(self):
        return Container()


if __name__ == '__main__':
    MainApp().run()
