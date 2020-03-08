from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from app import MDApp
from kivymd.toast import toast


class LogInScreen(Screen):
    def login_press(self):
        login = self.ids.login.text
        password = self.ids.password.text
        if self.check_password(login, password):
            toast("you're in!")
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
        print(login, password)
        return True
