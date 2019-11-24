from kivy.app import App

from kivymd.theming import ThemeManager
from kivymd.utils.cropimage import crop_image


class MainApp(App):
    theme_cls=ThemeManager()
    pass

MainApp().run()