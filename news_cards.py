"""

Файлик с примером создания инф плиток

- плитка с кучей текста
- плитка  картинкой и коротким текстом

"""
from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.uix.card import MDCardPost
from kivymd.uix.dialog import MDDialog
from kivymd.theming import ThemeManager
from kivymd.toast import toast

from functools import partial

Window.size = (480, 853)

Builder.load_string('''
<ExampleCardPost@BoxLayout>
    orientation: 'vertical'
    spacing: dp(5)

    MDToolbar:
        id: toolbar
        title: app.title
        left_action_items: [['menu', lambda x: None]]
        elevation: 10
        md_bg_color: app.theme_cls.primary_color


    ScrollView:
        id: scroll
        size_hint: 1, 1
        do_scroll_x: False

        GridLayout:
            id: grid_card
            cols: 1
            spacing: dp(5)
            padding: dp(5)
            size_hint_y: None
            height: self.minimum_height
''')

class CardPost(MDCardPost):
    def __init__(self, size=335, **kwargs):
        super().__init__(**kwargs)
        self.card_size[1] = size


class Example(MDApp):
    title = "Card Post"
    cards_created = False

    def build(self):
        self.screen = Factory.ExampleCardPost()
        return self.screen

    def on_start(self):
        def callback_for_menu_items(text_item):
            toast('Вы записаны')

        def event_reg(*args):
            if args[0] == 'Записаться':
                toast('Вы записаны')

        def show_full_text(news_id, *args):
            if args[1] and isinstance(args[1], str):
                toast('Вы записаны')
            else:
                dialog = MDDialog(
                    title='Title',
                    size_hint=(.8, .8),
                    text='full text of {} '.format(news_id) * 100,
                    text_button_ok='Записаться',
                    text_button_cancel='Close',
                    events_callback=event_reg)
                dialog.open()

        instance_grid_card = self.screen.ids.grid_card
        buttons = ['vk']
        menu_items = [{'viewclass': 'MDMenuItem',
                       'text': 'Записаться',
                       'callback': callback_for_menu_items}]

        if not self.cards_created:
            self.cards_created = True

            instance_grid_card.add_widget(
                CardPost(
                    source="demos/kitchen_sink/assets/african-lion-951778_1280.png",
                    right_menu=menu_items,
                    name_data='KamGU\n01.01.2020',
                    size=350,
                    tile_font_style="H5",
                    text_post="Длинная текстовая новость №1 " * 50,
                    with_image=False,
                    callback=partial(show_full_text, 1),
                    buttons=buttons))

            instance_grid_card.add_widget(
                CardPost(
                    source="demos/kitchen_sink/assets/african-lion-951778_1280.png",
                    tile_font_style="H5",
                    text_post="Короткое описание второй новости",
                    with_image=True,
                    callback=partial(show_full_text, 2),
                    buttons=buttons))


Example().run()
