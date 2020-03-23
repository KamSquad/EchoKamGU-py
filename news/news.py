from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.properties import StringProperty

from kivymd.uix.button import MDTextButton
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.label import MDLabel

from random import randint
from math import ceil


def text_height(text, win_width):
    height = 0
    line_height = 0
    paragraphs = text.split("\n")
    for par in paragraphs:
        label = MDLabel(text=par)
        label.text_size = [None, None]
        label.texture_update()
        if not line_height:
            line_height = label.texture_size[1]
        height += ceil(label.texture_size[0] / win_width) * ceil(label.texture_size[1] * 1.5)
        print(par, label.texture_size, height)
    return height + line_height * 2


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


class NewsCard(MDCard):
    def __init__(self, text_text="", title_text="", image_text=""):
        super().__init__()

        img_flag = False
        # if randint(0, 1):
        #     img = Image(source="data/pics/koshak_flat.png")
        #     self.ids.news_image.source = "data/pics/koshak_flat.png"
        #     img_flag = True
        # else:
        #     self.remove_widget(self.ids.news_image)

        sub_flag = True
        if True:
            sub_flag = False
            self.remove_widget(self.ids.bottom_sep)
            self.remove_widget(self.ids.news_sub_button)

        if not text_text:
            title = self.ids.news_title
            title.text = 'title'
            title.texture_update()
            title.height = title.texture_size[1]

            text = self.ids.news_text
            text.text = "Длинная текстовая новость №1 " * randint(10, 20)
            text.texture_update()
            text.height = text.texture_size[1] / Window.width * text.texture_size[0] + 20

        else:
            title = self.ids.news_title
            title.text = title_text
            title.height = text_height(title_text, Window.width) + 5

            text = self.ids.news_text
            text.text = text_text
            text.height = text_height(text_text, Window.width) + 10

            img = Image(source=image_text)
            self.ids.news_image.source = image_text
            img_flag = True

        self.height = (title.height +
                       text.height +
                       (img.height if img_flag else 0) +
                       (self.ids.news_sub_button.height if sub_flag else 0))


class NewsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.news_grid = None
        self.nav_drawer = None
        self.nav_list = None
        self.news_list = []

    def _get_news(self):
        return [["title",
                 "text",
                 "data/pics/koshak_flat.png"],
                ["ПРОФИЛАКТИКА КОРОНАВИРУСНОЙ ИНФЕКЦИИ, ГРИППА И ДРУГИХ ОРВИ",
                 "Что нужно делать в период активной циркуляции возбудителей коронавирусной инфекции, гриппа и других "
                 "возбудителей острых респираторных вирусных инфекций (ОРВИ) для того, чтобы предотвратить "
                 "собственное заражение и обезопасить окружающих, если заболели вы?",
                 "data/pics/zastavka-virus.jpg"],
                ["ПРЕДВАРИТЕЛЬНЫЕ РЕЗУЛЬТАТЫ ОЛИМПИАДЫ ПО ИНФОРМАТИКЕ «ВИТУС БЕРИНГ 2019»",
                 "21 декабря в ФГБОУ ВО «КамГУ им. Витуса Беринга» прошла олимпиада по информатике «Витус Беринг – "
                 "2019». В олимпиаде приняло участие 52 обучающихся 8-11 классов школ города "
                 "Петропавловска-Камчатского и города Елизово.",
                 "data/pics/fon-uni.png"],
                ["НОВОГОДНИЙ ВЕЧЕР ФИЗИКО-МАТЕМАТИЧЕСКОГО ФАКУЛЬТЕТА!",
                 "Приглашаем вас принять участие в Новогоднем вечере физико-математического факультета!\nТолько у нас "
                 "вы узнаете о том, как проходят выборы сказочных существ на пост председателя ФСО, что такое "
                 "волшебство и справедливость.\nВас ждет куча сладостей, живая музыка и хорошее настроение.\nСпешите, "
                 "количество мест ограничено!\nГде? Когда? — актовый зал 2 корпуса, 24.12 в 18:00\nПодробности по "
                 "телефону: +7 996-034-24-89",
                 "data/pics/new_year.png"],
                ["ОЛИМПИАДА ПО ИНФОРМАТИКЕ «ВИТУС БЕРИНГ- 2019»",
                 "21 декабря 2019 года на базе физико-математического факультета ФГБОУ ВО\n«КамГУ им. Витуса Беринга» "
                 "состоится олимпиада по информатике «Витус Беринг- 2019».\nЦель олимпиады – выявление одаренных "
                 "детей в области информатики, способных к научно-исследовательской деятельности, "
                 "а также популяризации информатики среди учащихся общеобразовательных школ Камчатского края.\nВ "
                 "олимпиаде могут принимать участие школьники 8-11 классов. Участие в олимпиаде свободное и "
                 "бесплатное.",
                 "data/pics/tv.png"]]

    def on_enter(self):
        self.news_grid = self.ids.news_grid
        self.news_list = self._get_news()

        if self.news_list:
            for entry in self.news_list:
                self.news_grid.add_widget(NewsCard(text_text=entry[1],
                                                   title_text=entry[0],
                                                   image_text=entry[2]))
        else:
            for _ in range(10):
                self.news_grid.add_widget(NewsCard())
            # for card in self.news_grid.children:
                # card.height = card.ids.news_title.height + card.ids.news_text.height
                # print(card.height, card.ids.news_title.height, card.ids.news_text.height)

        self.nav_list = self.ids.content_drawer.ids.md_list
        self.nav_list.add_widget(ItemDrawer(icon='folder', text='Название страницы'))

        # self.nav_drawer = self.ids.nav_drawer
        # self.nav_drawer.set_state('closed')
