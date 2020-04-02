from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock

from kivymd.uix.button import MDTextButton
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog

from random import randint
from math import ceil


def text_height(text, win_width):
    label = MDLabel(text=text)
    label.text_size = [None, None]
    label.width = win_width - 40
    label.texture_update()
    return label.texture_size[1]


class NewsPopup(Popup):
    def __init__(self, title, text):
        super().__init__()
        self.title = title
        self.ids.popup_label.text = text


class NewsCard(MDCard):
    def __init__(self, short_text="", title_text="", image_text="", full_text=""):
        super().__init__()

        #self.remove_widget(self.ids.news_image)
        # self.remove_widget(self.ids.news_sub_button)

        self.title = title_text
        self.short_text = short_text
        self.full_text = full_text
        self.image_path = image_text
        self.popup = NewsPopup(self.title, self.full_text)

        title = self.ids.news_title
        title.text = self.title
        title.height = text_height(title_text, Window.width)

        text = self.ids.news_text
        text.text = self.short_text
        text.height = text_height(self.short_text, Window.width)

        self.image = self.ids.news_image
        img = Image(source=self.image_path)
        self.image.source = self.image_path
        self.image.size = self.image.texture_size
        self.image.height = min(self.image.size[1], Window.height / 2)

        self.ids.buttons_box.height = self.ids.news_show_all_button.height

        self.height = sum(child.height for child in self.children)
        #print(self.height)

    def show_full(self):
        print('debug')
        self.popup.open()

    def get_image_size(self, image_h, rest_h):
        return image_h / (image_h + rest_h)


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
                 "",
                 "data/pics/koshak_flat.png"],
                ["ПРОФИЛАКТИКА КОРОНАВИРУСНОЙ ИНФЕКЦИИ, ГРИППА И ДРУГИХ ОРВИ",
                 "Что нужно делать в период активной циркуляции возбудителей коронавирусной инфекции, гриппа и других "
                 "возбудителей острых респираторных вирусных инфекций (ОРВИ) для того, чтобы предотвратить "
                 "собственное заражение и обезопасить окружающих, если заболели вы?",
                 "Что нужно делать в период активной циркуляции возбудителей коронавирусной инфекции, гриппа и других "
                 "возбудителей острых респираторных вирусных инфекций (ОРВИ) для того, чтобы предотвратить "
                 "собственное заражение и обезопасить окружающих, если заболели вы?\nВозбудители всех этих "
                 "заболеваний высоко заразны и передаются преимущественно воздушно-капельным путем.\nПри чихании и "
                 "кашле в воздухе вокруг больного человека распространяются микрокапли его слюны, мокроты и "
                 "респираторных выделений, которые содержат вирусы. Более крупные капли оседают на окружающих "
                 "предметах, и поверхностях, мелкие — долго находятся в воздухе и переносятся на расстояния до "
                 "нескольких сот метров, при этом вирусы сохраняют способность к заражению от нескольких часов до "
                 "нескольких дней. Основные меры гигиенической профилактики направлены на предотвращение контакта "
                 "здоровых людей с содержащими вирусы частицами выделений больного человека.",
                 "data/pics/zastavka-virus.jpg"],
                ["ПРЕДВАРИТЕЛЬНЫЕ РЕЗУЛЬТАТЫ ОЛИМПИАДЫ ПО ИНФОРМАТИКЕ «ВИТУС БЕРИНГ 2019»",
                 "21 декабря в ФГБОУ ВО «КамГУ им. Витуса Беринга» прошла олимпиада по информатике «Витус Беринг – "
                 "2019». В олимпиаде приняло участие 52 обучающихся 8-11 классов школ города "
                 "Петропавловска-Камчатского и города Елизово.",
                 "",
                 "data/pics/fon-uni.png"],
                ["НОВОГОДНИЙ ВЕЧЕР ФИЗИКО-МАТЕМАТИЧЕСКОГО ФАКУЛЬТЕТА!",
                 "Приглашаем вас принять участие в Новогоднем вечере физико-математического факультета!\nТолько у нас "
                 "вы узнаете о том, как проходят выборы сказочных существ на пост председателя ФСО, что такое "
                 "волшебство и справедливость.\nВас ждет куча сладостей, живая музыка и хорошее настроение.\nСпешите, "
                 "количество мест ограничено!\nГде? Когда? — актовый зал 2 корпуса, 24.12 в 18:00\nПодробности по "
                 "телефону: +7 996-034-24-89",
                 "",
                 "data/pics/new_year.png"],
                ["ОЛИМПИАДА ПО ИНФОРМАТИКЕ «ВИТУС БЕРИНГ- 2019»",
                 "21 декабря 2019 года на базе физико-математического факультета ФГБОУ ВО\n«КамГУ им. Витуса Беринга» "
                 "состоится олимпиада по информатике «Витус Беринг- 2019».\nЦель олимпиады – выявление одаренных "
                 "детей в области информатики, способных к научно-исследовательской деятельности, "
                 "а также популяризации информатики среди учащихся общеобразовательных школ Камчатского края.\nВ "
                 "олимпиаде могут принимать участие школьники 8-11 классов. Участие в олимпиаде свободное и "
                 "бесплатное.",
                 "",
                 "data/pics/tv.png"]]

    def on_enter(self):
        Clock.schedule_once(self.add_news)

    def add_news(self, *args):
        # print(self, self.children)

        self.news_grid = self.ids.news_grid
        self.news_list = self._get_news()

        if self.news_list:
            for entry in self.news_list:
                self.news_grid.add_widget(NewsCard(short_text=entry[1],
                                                   title_text=entry[0],
                                                   full_text=entry[2],
                                                   image_text=entry[3]))
        else:
            for _ in range(10):
                self.news_grid.add_widget(NewsCard())

        # self.nav_list = self.ids.content_drawer.ids.md_list
        # self.nav_list.add_widget(ItemDrawer(icon='folder', text='Название страницы'))
