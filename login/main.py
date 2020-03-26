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
        check_password_res = self.check_password(login, password)
        if check_password_res:
            import libs.database as db
            localdb = db.LocalDB()
            localdb.set_startscreen(2)
            localdb.save_usertoken(check_password_res[0], check_password_res[1])
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
            LoginFunc_res = db.LoginFunc(login, password)
            if LoginFunc_res:
                return LoginFunc_res[0], LoginFunc_res[1]
            toast('Неправильный логин или пароль, повторите попытку')
            return None
