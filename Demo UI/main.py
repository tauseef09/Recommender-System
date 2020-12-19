from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from helpers import screens
from kivy.core.window import Window
from recommender import download_yr_movies
from kivy.clock import Clock

Window.size = (330, 600)


class AppLoad(Screen):
    pass


class LoginSignup(Screen):
    pass


class Login(Screen):
    pass


class Signup(Screen):
    pass


class Menu(Screen):
    pass


sm = ScreenManager()
sm.add_widget(AppLoad(name='appload'))
sm.add_widget(LoginSignup(name='login_signup'))
sm.add_widget(Login(name='login'))
sm.add_widget(Signup(name='signup'))
sm.add_widget(Signup(name='menu'))


class DemoUI(MDApp):
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

    def on_start(self):
        Clock.schedule_once(self.download_and_transition, 1)

    def handleFloatingActionButton(self, instance):
        if instance.icon is 'power':
            exit()
        elif instance.icon is 'logout':
            self.screen.transition.direction = 'right'
            self.screen.current = 'login_signup'


DemoUI().run()
