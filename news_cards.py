"""
Информационные плитки для использованяи внутри MainBackdrop

- плитка с кучей текста
- плитка  картинкой и коротким текстом
"""
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivymd.uix.card import MDCardPost
from kivymd.uix.dialog import MDDialog
from kivymd.theming import ThemeManager
from kivymd.toast import toast

from functools import partial
from time import sleep


class CardPost(MDCardPost):
    def __init__(self, size=335, **kwargs):
        super().__init__(**kwargs)
        self.card_size[1] = size


def subscribe():
    toast('Вы записаны')


def news_cards(self):

    def callback_for_menu_items(text_item):
        subscribe()

    def event_reg(*args):
        if args[0] == 'Записаться':
            subscribe()

    def show_full_text(news_id, *args):
        if args[1] and isinstance(args[1], str):
            subscribe()
        else:
            dialog = MDDialog(
                title='Title',
                size_hint=(.8, .8),
                text='full text of {} '.format(news_id) * 100,
                text_button_ok='Записаться',
                text_button_cancel='Close',
                events_callback=event_reg)
            dialog.open()
            sleep(0.01)

            # Вариант с открытием нового окна с тектом, недоделан
            # self.ids.grid_full.add_widget(Label(text='full text of {} '.format(news_id) * 100))
            # self.current = 'full_text'

    instance_grid_card = self.ids.grid_card
    buttons = ['pen']
    menu_items = [{'viewclass': 'MDMenuItem',
                   'text': 'Записаться',
                   'callback': callback_for_menu_items}]

    if not self.cards_created:
        self.cards_created = True

        # for i in range(10):
        #     instance_grid_card.add_widget(Button(text='Hello {}'.format(i)))
        #     instance_grid_card.add_widget(Button(text='World {}'.format(i)))

        # instance_grid_card.add_widget(
        #     CardPost(
        #         path_to_avatar="data/pics/kamgu_logo.png",
        #         right_menu=menu_items,
        #         name_data='KamGU\n01.01.2020',
        #         size=350,
        #         tile_font_style="H5",
        #         text_post="Длинная текстовая новость №1 " * 50,
        #         with_image=False,
        #         #size_hint=None,
        #         #heigth=350,
        #         callback=partial(show_full_text, 1),
        #         buttons=buttons))
        #
        # instance_grid_card.add_widget(
        #     CardPost(
        #         source="data/pics/koshak_flat.png",
        #         tile_font_style="H5",
        #         text_post="Короткое описание второй новости",
        #         with_image=True,
        #         size=300,
        #         #size_hint=None,
        #         #heigth=250,
        #         callback=partial(show_full_text, 2),
        #         buttons=buttons))

