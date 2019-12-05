"""
Главный экран приложеня
"""
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from app import MDApp

from backdrop import mainbackdrop


for kvfile in ['main.kv', 'backdrop/mainbackdrop.kv', 'registration/main.kv', 'greetings/main.kv']:
    with open(kvfile, encoding='utf8') as f:
        Builder.load_string(f.read())


class MainScreenManager(ScreenManager):
    pass


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "DeepPurple"

    def build(self):
        return MainScreenManager()


MainApp().run()

