import os

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.metrics import dp

from kivymd.uix.card import MDCard
from kivymd.utils.cropimage import crop_image
from kivymd.uix.button import MDRaisedButton
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar

IMAGE_PATH = '../data/pics/kamgu_logo.png'


# Получить относительный путь к файлу
def get_relative_path(path):
    from pathlib import Path
    base_path = Path(__file__).parent
    file_path = (base_path / path).resolve()
    return file_path


def crop_image_for_card(path):
    path_to_crop_image = cropped_image_path(path)
    if not os.path.exists(path_to_crop_image):
        crop_image(
            (int(Window.width - dp(10)), int(dp(250))),
            path,
            path_to_crop_image
        )


def cropped_image_path(path):
    return '{}_cropped.png'.format(str(path).rstrip('.png'))


class MainWelcomeElement(Screen):
    def __init__(self, **kwargs):
        super(MainWelcomeElement, self).__init__(**kwargs)
        self.slide_number = 0

    def greet_button(self):
        if self.slide_number != 4:
            self.ids.carousel_id.load_next()
        else:
            self.main_manager.current = "login"

    def slide_change(self, slide_number):
        self.slide_number = slide_number
        if slide_number == 0:
            self.ids.caption_text.text = 'Добро пожаловать в приложение\nEchoKamGU!'
            self.ids.log_in_button.text = 'Начать'
        if slide_number == 1:
            self.ids.caption_text.text = 'Преимущество 1'
            self.ids.log_in_button.text = 'Далее'
        if slide_number == 2:
            self.ids.caption_text.text = 'Преимущество 2'
            self.ids.log_in_button.text = 'Далее'
        if slide_number == 3:
            self.ids.caption_text.text = 'Преимущество 3'
            self.ids.log_in_button.text = 'Далее'
        if slide_number == 4:
            self.ids.caption_text.text = ''
            self.ids.log_in_button.text = 'Войти'


class GreetCard(MDCard):
    text = StringProperty("")
    win_height = Window.size[1]
    image_path = str(get_relative_path(IMAGE_PATH))


class GreetingsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        # crop_image_for_card(get_relative_path(IMAGE_PATH))
