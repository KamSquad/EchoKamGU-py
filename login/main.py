from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage

from app import MDApp
from kivymd.toast import toast


class LogInScreen(Screen):
    login_button_pressed = False

    def login_press(self):
        login = self.ids.login.text
        password = self.ids.password.text
        if self.check_password(login, password):
            import libs.database as db
            localdb = db.LocalDB()
            localdb.set_startscreen(2)
            self.main_manager.current = "news_screen"
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
            if not self.login_button_pressed:
                self.login_button_pressed = True
                from kivy.core.audio import SoundLoader
                sound = SoundLoader.load("login/end.mp3")
                sound.play()
        else:
            #  real mode, ea >B-)
            import libs.database as db
            if db.LoginFunc(login, password):
                return True
            toast('Неправильный логин или пароль, повторите попытку')
            return False
