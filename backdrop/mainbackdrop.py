"""
Экран новостей

Screen - MainBackdrop
"""
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.core.window import Window

from kivymd.theming import ThemableBehavior
from kivymd.uix.card import MDCardPost

from random import randint
from math import ceil
import news_cards


class CardPost(MDCardPost):
    def __init__(self, size=335, **kwargs):
        super().__init__(**kwargs)
        self.card_size[1] = size


class MainBackdropFrontLayer(ScreenManager):
    cards_created = False

    def on_open(self):
        news_cards.news_cards(self)

    def add_news(self):
        text = "Длинная текстовая новость №1 " * randint(10, 50)

        # get element height
        # if anyone can rewrite this, then please do
        l = Label(text=text)
        l.texture_update()
        height = (ceil(l.texture_size[0] / Window.size[0]) * l.texture_size[1]) + l.texture_size[1] * 4

        self.ids.grid_card.add_widget(
            CardPost(
                path_to_avatar="data/pics/kamgu_logo.png",
                name_data='KamGU\n01.01.2020',
                text_post=text,
                size=height,
                with_image=False))


class MainBackdrop(Screen):
    pass


class ItemBackdropBackLayer(ThemableBehavior, BoxLayout):
    icon = StringProperty("android")
    text = StringProperty()
    selected_item = BooleanProperty(False)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            for item in self.parent.children:
                if item.selected_item:
                    item.selected_item = False
            self.selected_item = True
        return super().on_touch_down(touch)
