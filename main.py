"""
Главный экран приложеня
"""
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window

from app import MDApp

from backdrop import mainbackdrop
from login import main


for kvfile in ['main.kv', 'backdrop/mainbackdrop.kv', 'login/main.kv', 'greetings/main.kv']:
    with open(kvfile, encoding='utf8') as f:
        Builder.load_string(f.read())

# Window.size = (360, 640)
# Config.set('graphics', 'resizable', '0')
# Config.set('graphics', 'width', '360')
# Config.set('graphics', 'height', '640')


class MainScreenManager(ScreenManager):
    pass


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Green"

    def build(self):
        return MainScreenManager()


MainApp().run()

