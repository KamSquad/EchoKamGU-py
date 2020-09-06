"""
Главный экран приложеня
"""
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.config import Config

from app import MDApp


def config():
    """
    Window configuration, that hopefully works.
    Half of it doesn't work.
    Probably.

    :return: Sufferings
    """
    Config.set('graphics', 'resizable', 0)
    # Set the background color for the window
    Window.clearcolor = (1, 1, 1, 1)
    Window.minimum_height = 500
    Window.minimum_width = 500
    Window.fullsize = 'auto'
    Window.release_all_keyboards()
    print(Window.size)


def load_files():
    """
    Load all our modules and their respectable .kv files.

    :return: None
    """

    from main_manager.greetings import greetings
    from main_manager.login import login
    from main_manager.sidebar_screen import sidebar
    from main_manager.sidebar_screen.news import news
    from main_manager.sidebar_screen.settings import settings
    from main_manager.sidebar_screen.notifications_settings import notifications_settings
    from main_manager.sidebar_screen.about import about
    from main_manager.sidebar_screen.general import general
    from main_manager.sidebar_screen.support import support

    for kvfile in ['EchoKamGU.kv',
                   'main_manager/sidebar_screen/news/news.kv',
                   'main_manager/login/login.kv',
                   'main_manager/greetings/greetings.kv',
                   'main_manager/sidebar_screen/sidebar.kv',
                   'main_manager/sidebar_screen/settings/settings.kv',
                   'main_manager/sidebar_screen/notifications_settings/notifications_settings.kv',
                   'main_manager/sidebar_screen/about/about.kv',
                   'main_manager/sidebar_screen/general/general.kv',
                   'main_manager/sidebar_screen/support/support.kv']:
        with open(kvfile, encoding='utf8') as f:
            Builder.load_string(f.read())


class MainScreenManager(ScreenManager):
    """
    Top-level screen manager for the app.
    """

    # TODO: add first_screen(name pending) internal function
    def __init__(self, localdb, **kwargs):
        """
        Initialization of ScreenManager AND determining of the first screen.
        Probably needs to be split into 2 functions.

        :param localdb: client's local database object
        :param kwargs: something internal for kivy
        """
        super().__init__(**kwargs)
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
            if db.check_usertoken():
                self.current = 'sidebar_screen'
            else:
                self.current = 'login'
                db.check_internet_connection()


class EchoKamGUApp(MDApp):
    """
    App class.

    Determines starter palette and app icon.
    Initializes local database.
    """
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


config()
load_files()
EchoKamGUApp().run()
