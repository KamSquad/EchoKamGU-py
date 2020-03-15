from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

from kivymd.uix.button import MDTextButton
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.navigationdrawer import MDNavigationDrawer

from random import randint


class ContentNavigationDrawer(BoxLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class ButtonForNews(MDTextButton):
    def __init__(self, text=""):
        super().__init__()
        if not text:
            self.text = "Длинная текстовая новость №1 " * randint(10, 50)
        self.text_size = (Window.size[0], None)


class NewsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.news_grid = None
        self.nav_drawer = None
        self.nav_list = None
        self.news_list = []

    def _get_news(self):
        return []

    def on_enter(self):
        self.news_grid = self.ids.news_grid
        self.news_list = self._get_news()

        if self.news_list:
            for entry in self.news_list:
                self.news_grid.add_widget(ButtonForNews(text=entry))
        else:
            for _ in range(10):
                self.news_grid.add_widget(ButtonForNews())

        self.nav_list = self.ids.content_drawer.ids.md_list
        self.nav_list.add_widget(ItemDrawer(icon='folder', text='Название страницы'))

        self.nav_drawer = self.ids.nav_drawer
        self.nav_drawer.set_state('closed')
