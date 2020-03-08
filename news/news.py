from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.uix.button import MDTextButton

from random import randint


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
