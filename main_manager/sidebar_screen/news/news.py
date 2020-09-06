from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton

from libs import database
from os.path import exists

NEWS_CHECK = False


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
    # TODO: split initialization into multiple functions.
    def __init__(self, short_text="", title_text="", image_path="", full_text="", sidebar=None):
        super().__init__()

        self.sidebar = sidebar

        self.title = title_text
        self.short_text = short_text
        # print(title_text)
        self.full_text = ''.join('      {}\n'.format(x) for x in full_text.split('\n\n'))
        self.image_path = image_path
        self.popup = NewsPopup(self.title, self.full_text)

        title = self.ids.news_title
        title.text = self.title
        title.height = text_height(title_text, Window.width)
        # print(title.height, end=' ')

        text = self.ids.news_text
        text.text = self.short_text
        text.height = text_height(self.short_text, Window.width)
        # print(text.height, end=' ')

        self.image = self.ids.news_image
        if self.image_path != 'default' and exists(self.image_path):
            self.image.source = self.image_path
            self.image.size = self.image.texture_size
            self.image.height = min(self.image.size[1], Window.height / 2)
        else:
            self.remove_widget(self.image)
            self.remove_widget(self.ids.image_separator)

        self.height = (sum(child.height for child in self.children)
                       + (len(self.children) - 1) * self.spacing
                       + self.padding[1] + self.padding[3])
        # print(self.children)

    def show_full(self):
        #self.popup.open()
        article_screen = self.sidebar.ids.article
        article_screen.ids.text_label.text = self.full_text
        article_screen.ids.title_label.text = self.title

        self.sidebar.ids.toolbar.title = 'Новость университета'
        self.sidebar.ids.sidebar_manager.current = article_screen.name

    def get_image_size(self, image_h, rest_h):
        return image_h / (image_h + rest_h)


class NewsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.news_grid = None
        self.nav_drawer = None
        self.nav_list = None
        self.news_list = []
        self.added = False

    def _get_news(self):
        news = database.get_remote_news()
        if news:
            # титул, короткая, вся, картинка
            news = ((x[2], x[4], (x[4]+' '), x[3]) for x in news)
            return news
        else:
            return [["ПРОФИЛАКТИКА КОРОНАВИРУСНОЙ ИНФЕКЦИИ, ГРИППА И ДРУГИХ ОРВИ",
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

    # TODO: it tries to run twice and self.added not helping.
    #  global variable check works, but i don't like that.
    #  there needs to be a better solution
    def add_news(self, *args):
        """
        Adding news cards to news list.

        Must be run once(on enter), but tries to run twice.

        :param args: something clock-related? maybe
        :return: None
        """
        global NEWS_CHECK
        if self.added or NEWS_CHECK:
            return None

        # print('add_news', id(self))
        self.added = True
        NEWS_CHECK = True

        self.news_grid = self.ids.news_grid
        self.news_list = self._get_news()

        if self.news_list:
            for entry in self.news_list:
                self.news_grid.add_widget(NewsCard(title_text=entry[0],
                                                   short_text=entry[1],
                                                   full_text=entry[2],
                                                   image_path=entry[3],
                                                   sidebar=self.sidebar))
        else:
            for _ in range(10):
                self.news_grid.add_widget(NewsCard())

        # self.nav_list = self.ids.content_drawer.ids.md_list
        # self.nav_list.add_widget(ItemDrawer(icon='folder', text='Название страницы'))

    class TestButton(MDRaisedButton):

        def something(self):
            print(database.get_remote_news())
