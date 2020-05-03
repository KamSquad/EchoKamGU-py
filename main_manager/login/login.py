from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from app import MDApp
from kivymd.toast import toast

import libs.ztweaks as zt
import libs.database as db


class LogInScreen(Screen):
    def login_press(self):
        login = self.ids.login.text
        password = self.ids.password.text
        if self.check_password(login, password):
            self.main_manager.current = "sidebar_screen"
            with db.LocalDB() as ldb:
                ldb.set_startscreen(2)
            app = MDApp.get_running_app()
            '''
            if login == "Luna":
                app.theme_cls.primary_palette = "Blue"
            elif login == "Harry":
                app.theme_cls.primary_palette = "Red"
                app.theme_cls.primary_hue = "600"
            elif login == "Lord":
                app.theme_cls.primary_palette = "Green"
            elif login == "Cedric":
                app.theme_cls.primary_palette = "Orange"
            elif login == "Sybill":
                app.theme_cls.primary_palette = "DeepPurple"
            '''

    def check_password(self, login, password):
        if zt.GlobalVars().meme_mode:
            from kivy.core.audio import SoundLoader
            sound = SoundLoader.load("login/end.mp3")
            sound.play()
        else:
            #  real mode
            import libs.database as db
            if zt.checkinternet_and_notify():
                user_hashed = db.LoginFunc(login, password)
                if user_hashed:
                    with db.LocalDB() as ldb:
                        ldb.save_usertoken(user_hashed[0], user_hashed[1])
                    return True
                else:
                    zt.invalidlogin_notify()
                    return False
            else:
                return False


