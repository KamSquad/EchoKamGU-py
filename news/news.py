from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.uix.popup import Popup

from kivymd.uix.button import MDTextButton
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog

from random import randint
from math import ceil


def get_texture_size(text):
    label = MDLabel(text=text.replace('\n', ''))
    label.text_size = [None, None]
    label.texture_update()
    return label.texture_size


# в label текстура текста - длинная линия. эта функция разбивает текст на параграфы
# и отдельно подсчитывает необходимую высоту для каждого. длина текстуры делится на количество
# знаков в тексте и мы получаем среднюю длину символа. проходя по словам в пвраграфе,
# функция засекает необходимость переноса на новую строку и увеличивает высоту
def text_height(text, win_width):
    # получаем среднюю длину символа и высоту шрифта
    text_size = get_texture_size(text)
    #print(text, text_size)
    avg_width = text_size[0] / len(text)
    line_height = text_size[1]

    height = 0
    line_count = 0

    paragraphs = text.split("\n")
    for par in paragraphs:
        par_size = get_texture_size(par)
        par_width = 0

        for word in par.split():
            par_width += len(word) * avg_width + avg_width
            if par_width > win_width - 46:
                height += line_height
                line_count += 1
                par_width = len(word)

        height += line_height
        line_count += 1

    print(text, line_count)
    # у длинного текста проблемы с этим, поэтому для них побольше
    return height + line_height * (2 if height < 100 else 4)


class ContentNavigationDrawer(BoxLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class NewsPopup(Popup):
    def __init__(self, title, text):
        super().__init__()
        self.title = title
        self.ids.popup_label.text = text


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class NewsCard(MDCard):
    def __init__(self, short_text="", title_text="", image_text="", full_text=""):
        super().__init__()

        img_flag = False
        sub_flag = False
        self.remove_widget(self.ids.bottom_sep)
        self.remove_widget(self.ids.news_sub_button)

        self.title = title_text
        self.short_text = short_text
        self.full_text = full_text
        self.image_path = image_text
        # self.dialog = MDDialog(
        #     title=self.title,
        #     size_hint=(.8, .8),
        #     text=self.full_text,
        #     text_button_ok='Назад'
        # )
        self.popup = NewsPopup(self.title, self.full_text)

        if not short_text:
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
            title.text = self.title
            title.height = text_height(title_text, Window.width)

            text = self.ids.news_text
            text.text = self.short_text
            text.height = text_height(self.short_text, Window.width)

            img = Image(source=self.image_path)
            self.ids.news_image.source = self.image_path
            img_flag = True

        self.height = (title.height +
                       text.height +
                       (img.height if img_flag else 0) +
                       (self.ids.news_sub_button.height if sub_flag else 0))

    def show_full(self):
        print('debug')
        self.popup.open()


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
            # for card in self.news_grid.children:
                # card.height = card.ids.news_title.height + card.ids.news_text.height
                # print(card.height, card.ids.news_title.height, card.ids.news_text.height)

        self.nav_list = self.ids.content_drawer.ids.md_list
        self.nav_list.add_widget(ItemDrawer(icon='folder', text='Название страницы'))

        # self.nav_drawer = self.ids.nav_drawer
        # self.nav_drawer.set_state('closed')
