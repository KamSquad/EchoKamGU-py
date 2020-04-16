"""
Главный экран приложеня
"""
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.config import Config

from app import MDApp
from news import news
from login import login
from greetings import greetings
from sidebar_screen import sidebar
from settings import settings
from notifications_settings import notifications_settings

Config.set('graphics', 'resizable', 0)
# Set the background color for the window
Window.clearcolor = (1, 1, 1, 1)
Window.minimum_height = 500
Window.minimum_width = 500
Config.set('graphics', 'resizable', 0)
Window.fullsize = 'auto'
Window.release_all_keyboards()
print(Window.size)


for kvfile in ['EchoKamGU.kv',
               'news/news.kv',
               'login/login.kv',
               'greetings/greetings.kv',
               'sidebar_screen/sidebar.kv',
               'settings/settings.kv',
               'notifications_settings/notifications_settings.kv']:
    with open(kvfile, encoding='utf8') as f:
        Builder.load_string(f.read())


class MainScreenManager(ScreenManager):
    def __init__(self, localdb, **kwargs):
        super().__init__(**kwargs)
        # self.current = 'sidebar_screen'
        import libs.database as db
        import libs.ztweaks as ztweaks

        res = localdb.get_startscreen()
        if res == 0:
            self.current = 'greetings'
            localdb.set_startscreen(1)
        elif res == 1:
            self.current = 'login'
            db.check_internet_connection()
        else:
            self.current = 'news_screen'


class EchoKamGUApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Green"

    def build(self):
        self.icon = 'logo.png'
        import libs.ztweaks as ztweaks
        import libs.database as db
        print('[*] [INFO]\t[App name] \t\t\t= ' + self.get_application_name())
        print('[*] [INFO]\t[Data Fold Path] \t= ' + ztweaks.ProjectFolder(""))
        print('[*] [INFO]\t[Local DB Path] \t= ' + ztweaks.ReturnLocalDBPath())
        localdb = db.LocalDB()  # init local db

        return MainScreenManager(localdb)


EchoKamGUApp().run()
