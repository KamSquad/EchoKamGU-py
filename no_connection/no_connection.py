from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivymd.app import MDApp

Window.size = (480, 853)

from kivy.config import Config

Config.set('kivy', 'keyboard_mode', 'systemanddock')

with open('no_connection.kv', encoding='utf8') as f:
    Builder.load_string(f.read())

from kivymd.theming import ThemeManager


class Container(GridLayout):
    pass


class MyApp(MDApp):

    def build(self):
        self.theme_cls.theme = 'Light'
        return Container()


if __name__ == '__main__':
    MyApp().run()
