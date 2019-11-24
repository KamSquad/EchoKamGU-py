from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemeManager
from kivy.lang import Builder

# FOR SREEN SWITCH
from kivy.uix.screenmanager import Screen, ScreenManager 
s_manager = ScreenManager()

Window.size = (480, 653)

class FirstRunWindow(Screen):
    def __init__(self):
        global s_manager
        super().__init__()
        self.manager = s_manager

class Second(Screen):
    pass

class CreateAccountScreenWindow(Screen):
    pass

buildKV = Builder.load_file("main.kv")

class MainApp(App):
    theme_cls = ThemeManager()
    def build(self):
        return FirstRunWindow() #buildKV0

'''
#USING CHANGE SCREEN WITH VARIABLE OF SCREEN PROPS
 
Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Goto settings'
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'settings'
        Button:
            text: 'Quit'

<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'menu'
""")

# Declare both screens
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))

class TestApp(App):

    def build(self):
        return sm
'''

if __name__ == '__main__':
    MainApp().run()