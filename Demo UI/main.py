from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from helpers import screens
from kivy.core.window import Window
from recommender import download_yr_movies
from kivy.clock import Clock
from kivymd.uix.list import MDList, OneLineListItem

Window.size = (330, 600)


class AppLoad(Screen):
    pass


class LoginSignup(Screen):
    pass


class Login(Screen):
    pass


class Signup(Screen):
    pass


class MainMenu(Screen):
    pass


class ContentChoice(Screen):
    pass


class ContentList(Screen):
    pass


sm = ScreenManager()
sm.add_widget(AppLoad(name='appload'))
sm.add_widget(LoginSignup(name='login_signup'))
sm.add_widget(Login(name='login'))
sm.add_widget(Signup(name='signup'))
sm.add_widget(MainMenu(name='mainmenu'))
sm.add_widget(ContentChoice(name='contentchoice'))
sm.add_widget(ContentList(name='contentlist'))


class DemoUI(MDApp):
    current_content_choice = ""

    def build(self):
        self.screen = Builder.load_string(screens)
        return self.screen

    def download_and_transition(self, obj):
        y_movies, r_movies = download_yr_movies()
        self.screen.get_screen('appload').ids.progress_bar.value = 33

        y_books, r_books = download_yr_movies()
        self.screen.get_screen('appload').ids.progress_bar.value = 66

        y_songs, r_songs = download_yr_movies()
        self.screen.get_screen('appload').ids.progress_bar.value = 99

        self.screen.current = 'login_signup'

    def choice_movies(self):
        self.current_content_choice = "movies"
        self.screen.current = 'mainmenu'
        self.screen.get_screen('mainmenu').ids.main_menu_label.text = "Exploring movies!"

    def choice_songs(self):
        self.current_content_choice = "songs"
        self.screen.current = 'mainmenu'
        self.screen.get_screen('mainmenu').ids.main_menu_label.text = "Exploring songs!"

    def choice_books(self):
        self.current_content_choice = "books"
        self.screen.current = 'mainmenu'
        self.screen.get_screen('mainmenu').ids.main_menu_label.text = "Exploring books!"

    def return_content_dict(self):
        content_dict = dict()
        for i in range(1, 21):
            content_dict[i] = "Item " + str(i)
        return content_dict

    def show_content(self):
        self.screen.current = 'contentlist'
        content_dict = self.return_content_dict()
        for key, value in content_dict.items():
            item = OneLineListItem(text=value)
            self.screen.get_screen('contentlist').ids.list_view.add_widget(item)

    def on_start(self):
        Clock.schedule_once(self.download_and_transition, 2.5)


DemoUI().run()
