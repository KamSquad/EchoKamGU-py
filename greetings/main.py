import os

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.metrics import dp

from kivymd.uix.card import MDCard
from kivymd.utils.cropimage import crop_image
from kivymd.uix.managerswiper import MDSwiperPagination

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


class GreetSwiperManager(BoxLayout):
    pass


class GreetCard(MDCard):
    text = StringProperty("")
    win_height = Window.size[1]
    image_path = str(get_relative_path(IMAGE_PATH))


class GreetingsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        crop_image_for_card(get_relative_path(IMAGE_PATH))
