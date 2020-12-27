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


class MoodPhotoChoice(Screen):
    pass


sm = ScreenManager()
sm.add_widget(AppLoad(name='appload'))
sm.add_widget(LoginSignup(name='login_signup'))
sm.add_widget(Login(name='login'))
sm.add_widget(Signup(name='signup'))
sm.add_widget(ContentChoice(name='contentchoice'))
sm.add_widget(MainMenu(name='mainmenu'))
sm.add_widget(ContentList(name='contentlist'))
sm.add_widget(MoodPhotoChoice(name='moodphotochoice'))


class DemoUI(MDApp):
    current_content_choice = ""

    def build(self):
        self.screen = Builder.load_string(screens)
        self.previousScreen = list()  # to hold the screen transitions
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
        self.transition('mainmenu', True)
        self.screen.get_screen('mainmenu').ids.main_menu_label.text = "Exploring movies!"
        self.screen.get_screen('mainmenu').ids.art.source = "logo/art3.png"
        self.screen.get_screen('mainmenu').ids.art.size_hint = 0.6, 0.6

    def choice_songs(self):
        self.current_content_choice = "songs"
        self.transition('mainmenu', True)
        self.screen.get_screen('mainmenu').ids.main_menu_label.text = "Exploring songs!"
        self.screen.get_screen('mainmenu').ids.art.source = "logo/art1.png"
        self.screen.get_screen('mainmenu').ids.art.size_hint = 0.9, 0.9

    def choice_books(self):
        self.current_content_choice = "books"
        self.transition('mainmenu', True)
        self.screen.get_screen('mainmenu').ids.main_menu_label.text = "Exploring books!"
        self.screen.get_screen('mainmenu').ids.art.source = "logo/art2.png"
        self.screen.get_screen('mainmenu').ids.art.size_hint = 0.6, 0.6

    def show_mood_photo_choice(self):
        self.transition('moodphotochoice', True)
        if self.current_content_choice == "movies":
            self.screen.get_screen('moodphotochoice').ids.moodphotochoice_label.text = "Exploring movies!"
            self.screen.get_screen('moodphotochoice').ids.art_moodphotochoice.source = "logo/art3.png"
            self.screen.get_screen('moodphotochoice').ids.art_moodphotochoice.size_hint = 0.6, 0.6
        elif self.current_content_choice == "songs":
            self.screen.get_screen('moodphotochoice').ids.moodphotochoice_label.text = "Exploring songs!"
            self.screen.get_screen('moodphotochoice').ids.art_moodphotochoice.source = "logo/art1.png"
            self.screen.get_screen('moodphotochoice').ids.art_moodphotochoice.size_hint = 0.9, 0.9
        elif self.current_content_choice == "books":
            self.screen.get_screen('moodphotochoice').ids.moodphotochoice_label.text = "Exploring books!"
            self.screen.get_screen('moodphotochoice').ids.art_moodphotochoice.source = "logo/art2.png"
            self.screen.get_screen('moodphotochoice').ids.art_moodphotochoice.size_hint = 0.6, 0.6

    def return_content_dict(self):
        content_dict = dict()
        for i in range(1, 21):
            content_dict[i] = "Item " + str(i)
        return content_dict

    def show_content(self):
        self.transition('contentlist', True)
        content_dict = self.return_content_dict()
        for key, value in content_dict.items():
            item = OneLineListItem(text=value)
            self.screen.get_screen('contentlist').ids.list_view.add_widget(item)

    def on_start(self):
        Clock.schedule_once(self.download_and_transition, 2.5)

    def transition(self, to, forward):
        # takes the screen it needs to transition to and if its a forward transition
        if forward:
            self.screen.transition.direction = 'left'
            self.previousScreen.append(self.screen.current)
            self.screen.current = to
        else:
            self.screen.transition.direction = 'right'
            self.screen.current = self.previousScreen.pop()  # for going back it does not need a destination

    def handleFloatingActionButtonSpeedDial(self, instance):
        if instance.icon == "arrow-left":
            self.transition(self.previousScreen, False)
        elif instance.icon == "logout":
            self.transition('login_signup', True)


DemoUI().run()
