from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from helpers import screens
from kivy.core.window import Window
from recommender import download_yr_movies, download_yr_books, download_yr_songs
from recommender import upload_yr_movies, upload_yr_books, upload_yr_songs
from recommender import recommend_movies, recommend_books, recommend_songs, rate
from recommender import filter_content_movies, filter_content_books, filter_content_songs
from preload_model import preload_model
from take_photo import detect_mood, take_photo
from kivy.clock import Clock
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import numpy as np
import json
import threading
import time

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


class ItemPage(Screen):
    pass


class CameraPage(Screen):
    pass


class MoodChoice(Screen):
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
sm.add_widget(ItemPage(name='itempage'))
sm.add_widget(CameraPage(name='camerapage'))
sm.add_widget(MoodChoice(name='moodchoice'))


class DemoUI(MDApp):
    current_content_choice = ""
    first_name = ""
    last_name = ""
    username = ""
    password = ""
    user_id = -1
    content_dict_movies = dict()
    content_dict_books = dict()
    content_dict_songs = dict()
    current_item_id = -1
    current_item_rating = 0

    def build(self):
        self.screen = Builder.load_string(screens)
        self.previousScreen = list()  # to hold the screen transitions
        return self.screen

    def on_start(self):
        Clock.schedule_once(self.download_and_transition, 2.5)

    def on_stop(self):
        thread_movies = threading.Thread(target=upload_yr_movies, args=[self.y_movies, self.r_movies])
        thread_songs = threading.Thread(target=upload_yr_songs, args=[self.y_songs, self.r_songs])
        thread_books = threading.Thread(target=upload_yr_books, args=[self.y_books, self.r_books])

        thread_movies.start()
        thread_songs.start()
        thread_books.start()

        thread_movies.join()
        thread_songs.join()
        thread_books.join()

        # upload_yr_movies(self.y_movies, self.r_movies)
        # upload_yr_songs(self.y_songs, self.r_songs)
        # upload_yr_books(self.y_books, self.r_books)

    def download_and_transition(self, obj):
        self.model = preload_model()
        self.y_movies, self.r_movies = download_yr_movies()
        self.screen.get_screen('appload').ids.progress_bar.value = 33
        # print(self.y_movies.shape)
        # print(self.r_movies.shape)

        self.y_books, self.r_books = download_yr_books()
        self.screen.get_screen('appload').ids.progress_bar.value = 66
        # print(self.y_books.shape)
        # print(self.r_books.shape)

        self.y_songs, self.r_songs = download_yr_songs()
        self.screen.get_screen('appload').ids.progress_bar.value = 99
        # print(self.y_songs.shape)
        # print(self.r_songs.shape)

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

    def show_content(self):
        content_dict = dict()
        self.transition('contentlist', True)
        if self.current_content_choice == "movies":
            if len(self.content_dict_movies) == 0:
                self.content_dict_movies = recommend_movies(self.user_id, self.y_movies, self.r_movies)
                content_dict = self.content_dict_movies
            else:
                content_dict = self.content_dict_movies
        elif self.current_content_choice == "books":
            if len(self.content_dict_books) == 0:
                self.content_dict_books = recommend_books(self.user_id, self.y_books, self.r_books)
                content_dict = self.content_dict_books
            else:
                content_dict = self.content_dict_books
        else:
            if len(self.content_dict_songs) == 0:
                self.content_dict_songs = recommend_songs(self.user_id, self.y_songs, self.r_songs)
                content_dict = self.content_dict_songs
            else:
                content_dict = self.content_dict_songs

        i = 0
        self.screen.get_screen('contentlist').ids.list_view.clear_widgets()
        for key, value in content_dict.items():
            if i == 20:
                break
            i += 1
            item = OneLineListItem(text=value, on_release=self.show_item)
            item.id = str(key)
            self.screen.get_screen('contentlist').ids.list_view.add_widget(item)

    def show_item(self, obj):
        self.current_item_id = int(obj.id)
        self.screen.get_screen('itempage').ids.item.text = obj.text
        if self.current_content_choice == "movies":
            if self.y_movies[int(obj.id), self.user_id] != 0:
                self.screen.get_screen('itempage').ids.userrating.text = 'My rating: ' + str(self.y_movies[int(obj.id), self.user_id])
                self.change_rating_color(self.y_movies[int(obj.id), self.user_id])
            else:
                self.change_rating_color(0)
        elif self.current_content_choice == "books":
            if self.y_books[int(obj.id), self.user_id] != 0:
                self.screen.get_screen('itempage').ids.userrating.text = 'My rating: ' + str(self.y_books[int(obj.id), self.user_id])
                self.change_rating_color(self.y_books[int(obj.id), self.user_id])
            else:
                self.change_rating_color(0)
        else:
            if self.y_songs[int(obj.id), self.user_id] != 0:
                self.screen.get_screen('itempage').ids.userrating.text = 'My rating: ' + str(self.y_songs[int(obj.id), self.user_id])
                self.change_rating_color(self.y_songs[int(obj.id), self.user_id])
            else:
                self.change_rating_color(0)
        self.transition('itempage', True)

    def transition(self, to, forward):
        # takes the screen it needs to transition to and if its a forward transition
        if forward:
            self.screen.transition.direction = 'left'
            self.previousScreen.append(self.screen.current)
            self.screen.current = to
        else:
            self.current_item_id = -1
            self.current_item_rating = 0
            self.screen.transition.direction = 'right'
            self.screen.current = self.previousScreen.pop()  # for going back it does not need a destination

    def handleFloatingActionButtonSpeedDial(self, instance):
        if instance.icon == "arrow-left":
            self.transition(self.previousScreen, False)
        elif instance.icon == "logout":
            self.screen.get_screen('signup').ids.signup_firstname_textfield.text = ""
            self.screen.get_screen('signup').ids.signup_lastname_textfield.text = ""
            self.screen.get_screen('signup').ids.signup_username_textfield.text = ""
            self.screen.get_screen('signup').ids.signup_password_textfield.text = ""

            start = time.perf_counter()
            thread_movies = threading.Thread(target=upload_yr_movies, args=[self.y_movies, self.r_movies])
            thread_songs = threading.Thread(target=upload_yr_songs, args=[self.y_songs, self.r_songs])
            thread_books = threading.Thread(target=upload_yr_books, args=[self.y_books, self.r_books])

            thread_movies.start()
            thread_songs.start()
            thread_books.start()

            thread_movies.join()
            thread_songs.join()
            thread_books.join()

            # upload_yr_movies(self.y_movies, self.r_movies)
            # upload_yr_songs(self.y_songs, self.r_songs)
            # upload_yr_books(self.y_books, self.r_books)

            finish = time.perf_counter()
            print(f'Finished in {round(finish - start, 2)} second(s)')
            self.transition('login_signup', True)

    def signup(self):
        self.first_name = self.screen.get_screen('signup').ids.signup_firstname_textfield.text
        first_name_false = True

        self.last_name = self.screen.get_screen('signup').ids.signup_lastname_textfield.text
        last_name_false = True

        self.username = self.screen.get_screen('signup').ids.signup_username_textfield.text
        username_false = True

        self.password = self.screen.get_screen('signup').ids.signup_password_textfield.text
        password_false = True

        if self.first_name.split() == [] or self.last_name.split() == [] or self.username.split() == [] or self.password.split() == []:
            cancel_btn_dialogue = MDFlatButton(text="Retry", on_release=self.close_dialogue)
            self.dialogue = MDDialog(title="Invalid Info", text="Please enter valid information and password.",
                                     size_hint=(0.7, 0.2), buttons=[cancel_btn_dialogue])
            self.dialogue.open()
        else:
            if self.username_is_available():
                self.register_user()
                first_name_false = False
                last_name_false = False
                username_false = False
                password_false = False
            else:
                cancel_btn_dialogue = MDFlatButton(text="Retry", on_release=self.close_dialogue)
                self.dialogue = MDDialog(title="Username Unavailable",
                                         text="This username is taken. Please try another one.",
                                         size_hint=(0.7, 0.2), buttons=[cancel_btn_dialogue])
                self.dialogue.open()

        if first_name_false is False and last_name_false is False and username_false is False and password_false is False:
            self.screen.get_screen('contentchoice').ids.welcome_label.text = "Welcome, " + self.first_name + "!"
            self.transition('contentchoice', True)

    def close_dialogue(self, obj):
        self.dialogue.dismiss()

    def change_rating_color(self, rating_value):
        self.current_item_rating = rating_value
        if rating_value == 1:
            self.screen.get_screen('itempage').ids.star1.text_color = 77 / 255, 148 / 255, 255 / 255, 1
            self.screen.get_screen('itempage').ids.star2.text_color = 153 / 255, 153 / 255, 153 / 255, 1
            self.screen.get_screen('itempage').ids.star3.text_color = 153 / 255, 153 / 255, 153 / 255, 1
            self.screen.get_screen('itempage').ids.star4.text_color = 153 / 255, 153 / 255, 153 / 255, 1
            self.screen.get_screen('itempage').ids.star5.text_color = 153 / 255, 153 / 255, 153 / 255, 1
        elif rating_value == 2:
            self.screen.get_screen('itempage').ids.star1.text_color = 77 / 255, 148 / 255, 255 / 255, 1
            self.screen.get_screen('itempage').ids.star2.text_color = 77 / 255, 148 / 255, 255 / 255, 1
            self.screen.get_screen('itempage').ids.star3.text_color = 153 / 255, 153 / 255, 153 / 255, 1
            self.screen.get_screen('itempage').ids.star4.text_color = 153 / 255, 153 / 255, 153 / 255, 1
            self.screen.get_screen('itempage').ids.star5.text_color = 153 / 255, 153 / 255, 153 / 255, 1
        elif rating_value == 3:
            self.screen.get_screen('itempage').ids.star1.text_color = 77 / 255, 148 / 255, 255 / 255, 1
            self.screen.get_screen('itempage').ids.star2.text_color = 77 / 255, 148 / 255, 255 / 255, 1
            self.screen.get_screen('itempage').ids.star3.text_color = 77 / 255, 148 / 255, 255 / 255, 1
            self.screen.get_screen('itempage').ids.star4.text_color = 153 / 255, 153 / 255, 153 / 255, 1
            self.screen.get_screen('itempage').ids.star5.text_color = 153 / 255, 153 / 255, 153 / 255, 1
        elif rating_value == 4:
            self.screen.get_screen('itempage').ids.star1.text_color = 77 / 255, 148 / 255, 255 / 255, 1
            self.screen.get_screen('itempage').ids.star2.text_color = 77 / 255, 148 / 255, 255 / 255, 1
            self.screen.get_screen('itempage').ids.star3.text_color = 77 / 255, 148 / 255, 255 / 255, 1
            self.screen.get_screen('itempage').ids.star4.text_color = 77 / 255, 148 / 255, 255 / 255, 1
            self.screen.get_screen('itempage').ids.star5.text_color = 153 / 255, 153 / 255, 153 / 255, 1
        elif rating_value == 5:
            self.screen.get_screen('itempage').ids.star1.text_color = 77 / 255, 148 / 255, 255 / 255, 1
            self.screen.get_screen('itempage').ids.star2.text_color = 77 / 255, 148 / 255, 255 / 255, 1
            self.screen.get_screen('itempage').ids.star3.text_color = 77 / 255, 148 / 255, 255 / 255, 1
            self.screen.get_screen('itempage').ids.star4.text_color = 77 / 255, 148 / 255, 255 / 255, 1
            self.screen.get_screen('itempage').ids.star5.text_color = 77 / 255, 148 / 255, 255 / 255, 1
        else:
            self.screen.get_screen('itempage').ids.star1.text_color = 153 / 255, 153 / 255, 153 / 255, 1
            self.screen.get_screen('itempage').ids.star2.text_color = 153 / 255, 153 / 255, 153 / 255, 1
            self.screen.get_screen('itempage').ids.star3.text_color = 153 / 255, 153 / 255, 153 / 255, 1
            self.screen.get_screen('itempage').ids.star4.text_color = 153 / 255, 153 / 255, 153 / 255, 1
            self.screen.get_screen('itempage').ids.star5.text_color = 153 / 255, 153 / 255, 153 / 255, 1

    def username_is_available(self):
        available = True
        with open('users.json') as json_file:
            data = json.load(json_file)

        for item in data['users']:
            if self.username == item['username']:
                available = False

        return available

    def add_user_vectors(self):
        my_ratings_movies = np.zeros((self.y_movies.shape[0], 1), dtype=float)
        # generating user r vector from the user ratings (movies)
        my_r_movies = (my_ratings_movies != 0) * 1
        # adding new user y vector to y rating matrix (movies)
        self.y_movies = np.hstack((self.y_movies, my_ratings_movies))
        # adding new user r vector to original r matrix (movies)
        self.r_movies = np.hstack((self.r_movies, my_r_movies))

        my_ratings_songs = np.zeros((self.y_songs.shape[0], 1), dtype=float)
        # generating user r vector from the user ratings (songs)
        my_r_songs = (my_ratings_songs != 0) * 1
        # adding new user y vector to y rating matrix (songs)
        self.y_songs = np.hstack((self.y_songs, my_ratings_songs))
        # adding new user r vector to original r matrix (songs)
        self.r_songs = np.hstack((self.r_songs, my_r_songs))

        my_ratings_books = np.zeros((self.y_books.shape[0], 1), dtype=float)
        # generating user r vector from the user ratings (books)
        my_r_books = (my_ratings_books != 0) * 1
        # adding new user y vector to y rating matrix (books)
        self.y_books = np.hstack((self.y_books, my_ratings_books))
        # adding new user r vector to original r matrix (books)
        self.r_books = np.hstack((self.r_books, my_r_books))

    def register_user(self):
        self.user_id = self.y_movies.shape[1]
        self.add_user_vectors()
        with open('users.json') as json_file:
            data = json.load(json_file)

        temp = data['users']
        y = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "password": self.password,
            "user_id": self.user_id
        }
        temp.append(y)

        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)

    def login(self):
        self.username = self.screen.get_screen('login').ids.login_username_textfield.text
        username_false = True

        self.password = self.screen.get_screen('login').ids.login_password_textfield.text
        password_false = True

        if self.username.split() == [] or self.password.split() == []:
            cancel_btn_dialogue = MDFlatButton(text="Retry", on_release=self.close_dialogue)
            self.dialogue = MDDialog(title="Invalid Info", text="Please enter valid username and password.",
                                     size_hint=(0.7, 0.2), buttons=[cancel_btn_dialogue])
            self.dialogue.open()
        else:
            if self.verify_user():
                self.fetch_user_info()
                username_false = False
                password_false = False
            else:
                cancel_btn_dialogue = MDFlatButton(text="Retry", on_release=self.close_dialogue)
                self.dialogue = MDDialog(title="Login Failed", text="Username and Password do not match.",
                                         size_hint=(0.7, 0.2), buttons=[cancel_btn_dialogue])
                self.dialogue.open()

        if username_false is False and password_false is False:
            self.screen.get_screen('contentchoice').ids.welcome_label.text = "Welcome, " + self.first_name + "!"
            self.transition('contentchoice', True)

    def verify_user(self):
        verified = False
        with open('users.json') as json_file:
            data = json.load(json_file)

        for item in data['users']:
            if self.username == item['username'] and self.password == item['password']:
                verified = True
                break
        return verified

    def fetch_user_info(self):
        with open('users.json') as json_file:
            data = json.load(json_file)
        for item in data['users']:
            if self.username == item['username'] and self.password == item['password']:
                self.first_name = item['first_name']
                self.last_name = item['last_name']
                self.user_id = item['user_id']

    def save_rating_changes(self):
        if self.current_item_id != -1 and self.current_item_rating != 0:
            if self.current_content_choice == "movies":
                self.y_movies, self.r_movies = rate(self.current_item_id, self.user_id, self.y_movies, self.r_movies,
                                                    self.current_item_rating)
            elif self.current_content_choice == "books":
                self.y_books, self.r_books = rate(self.current_item_id, self.user_id, self.y_books, self.r_books,
                                                  self.current_item_rating)
            else:
                self.y_songs, self.r_songs = rate(self.current_item_id, self.user_id, self.y_songs, self.r_songs,
                                                  self.current_item_rating)

    def get_mood(self):
        if take_photo():
            mood = detect_mood("data/capture.png", self.model)
            if mood != "No faces detected":
                self.mood_filter(mood)
            else:
                cancel_btn_dialogue = MDFlatButton(text="Retry", on_release=self.close_dialogue)
                self.dialogue = MDDialog(title="No Faces Detected", text="Please check if there is sufficient light.",
                                         size_hint=(0.7, 0.2), buttons=[cancel_btn_dialogue])
                self.dialogue.open()

    def mood_filter(self, mood):
        content_dict = dict()
        self.transition('contentlist', True)
        if self.current_content_choice == "movies":
            if len(self.content_dict_movies) == 0:
                self.content_dict_movies = recommend_movies(self.user_id, self.y_movies, self.r_movies)
                content_dict = self.content_dict_movies
                content_dict = filter_content_movies(mood, content_dict)
            else:
                content_dict = self.content_dict_movies
                content_dict = filter_content_movies(mood, content_dict)
        elif self.current_content_choice == "books":
            if len(self.content_dict_books) == 0:
                self.content_dict_books = recommend_books(self.user_id, self.y_books, self.r_books)
                content_dict = self.content_dict_books
                content_dict = filter_content_books(mood, content_dict)
            else:
                content_dict = self.content_dict_books
                content_dict = filter_content_books(mood, content_dict)
        else:
            if len(self.content_dict_songs) == 0:
                self.content_dict_songs = recommend_songs(self.user_id, self.y_songs, self.r_songs)
                content_dict = self.content_dict_songs
                content_dict = filter_content_songs(mood, content_dict)
            else:
                content_dict = self.content_dict_songs
                content_dict = filter_content_songs(mood, content_dict)

        i = 0
        self.screen.get_screen('contentlist').ids.list_view.clear_widgets()
        for key, value in content_dict.items():
            if i == 20:
                break
            i += 1
            item = OneLineListItem(text=value, on_release=self.show_item)
            item.id = str(key)
            self.screen.get_screen('contentlist').ids.list_view.add_widget(item)


DemoUI().run()
