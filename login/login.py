from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage

from app import MDApp
from kivymd.toast import toast


class LogInScreen(Screen):
    def login_press(self):
        login = self.ids.login.text
        password = self.ids.password.text
        if self.check_password(login, password):
            self.main_manager.current = "sidebar_screen"

            app = MDApp.get_running_app()
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

    def check_password(self, login, password):
        import libs.ztweaks as ztweaks
        if ztweaks.GlobalVars().meme_mode:
            from kivy.core.audio import SoundLoader
            sound = SoundLoader.load("login/end.mp3")
            sound.play()
        else:
            #  real mode
            import libs.database as db
            # if db.LoginFunc(login, password):
            #     return True
            import kivymd.toast
            toast('Welcome back')
            return True
