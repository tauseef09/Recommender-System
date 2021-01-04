from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from helpers import screens
from kivy.core.window import Window
from recommender import download_y_movies, download_y_books, download_y_songs
from recommender import upload_y_movies, upload_y_books, upload_y_songs
from recommender import create_movies_dict, create_songs_dict, create_books_dict
from recommender import recommend, rate
from recommender import filter_content_movies, filter_content_books, filter_content_songs
from preload_model import preload_model
from take_photo import detect_mood, take_photo
from kivy.clock import Clock
from kivy.clock import mainthread
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import numpy as np
import json
import threading
import time
import pandas as pd

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


class Search(Screen):
    pass


class LoadingPage(Screen):
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
sm.add_widget(Search(name='search'))
sm.add_widget(LoadingPage(name='loadingpage'))


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
    movie_dict = dict()
    song_dict = dict()
    book_dict = dict()
    current_item_id = -1
    current_item_rating = 0

    def build(self):
        self.screen = Builder.load_string(screens)
        self.previousScreen = list()  # to hold the screen transitions
        return self.screen

    def on_start(self):
        Clock.schedule_once(self.download_and_transition, 2.5)

    def on_stop(self):
        upload_y_movies(self.y_movies)
        upload_y_songs(self.y_songs)
        upload_y_books(self.y_books)

    def download_and_transition(self, obj):
        """ Downloads all the required data and proceeds to the login/signup screen.

        """
        self.y_movies = download_y_movies()
        self.movie_dict = create_movies_dict()
        self.movie_names = pd.read_csv('data/movie_ids.csv')
        self.screen.get_screen('appload').ids.progress_bar.value = 33

        self.model = preload_model()

        self.y_books = download_y_books()
        self.book_dict = create_books_dict()
        self.book_names = pd.read_csv('data/book_ids.csv')
        self.screen.get_screen('appload').ids.progress_bar.value = 66

        self.y_songs = download_y_songs()
        self.song_dict = create_songs_dict()
        self.song_names = pd.read_csv('data/song_ids.csv')
        self.screen.get_screen('appload').ids.progress_bar.value = 99

        self.screen.current = 'login_signup'

    def choice_movies(self):
        """ Sets up the UI elements of the 'mainmenu' page for content choice: movies.

        """
        self.current_content_choice = "movies"
        self.transition('mainmenu', True)
        self.screen.get_screen('mainmenu').ids.main_menu_label.text = "Exploring movies!"
        self.screen.get_screen('mainmenu').ids.art.source = "logo/art3.png"
        self.screen.get_screen('mainmenu').ids.art.size_hint = 0.6, 0.6

    def choice_songs(self):
        """ Sets up the UI elements of the 'mainmenu' page for content choice: songs.

        """
        self.current_content_choice = "songs"
        self.transition('mainmenu', True)
        self.screen.get_screen('mainmenu').ids.main_menu_label.text = "Exploring songs!"
        self.screen.get_screen('mainmenu').ids.art.source = "logo/art1.png"
        self.screen.get_screen('mainmenu').ids.art.size_hint = 0.8, 0.8

    def choice_books(self):
        """ Sets up the UI elements of the 'mainmenu' page for content choice: books.

        """
        self.current_content_choice = "books"
        self.transition('mainmenu', True)
        self.screen.get_screen('mainmenu').ids.main_menu_label.text = "Exploring books!"
        self.screen.get_screen('mainmenu').ids.art.source = "logo/art2.png"
        self.screen.get_screen('mainmenu').ids.art.size_hint = 0.6, 0.6

    def show_mood_photo_choice(self):
        """ Transitions to and sets up the UI elements of the 'moodphotochoice' page depending
            on the content the user has currently selected.

        """
        self.transition('moodphotochoice', True)
        if self.current_content_choice == "movies":
            self.screen.get_screen('moodphotochoice').ids.moodphotochoice_label.text = "Exploring movies!"
            self.screen.get_screen('moodphotochoice').ids.art_moodphotochoice.source = "logo/art3.png"
            self.screen.get_screen('moodphotochoice').ids.art_moodphotochoice.size_hint = 0.6, 0.6
        elif self.current_content_choice == "songs":
            self.screen.get_screen('moodphotochoice').ids.moodphotochoice_label.text = "Exploring songs!"
            self.screen.get_screen('moodphotochoice').ids.art_moodphotochoice.source = "logo/art1.png"
            self.screen.get_screen('moodphotochoice').ids.art_moodphotochoice.size_hint = 0.8, 0.8
        elif self.current_content_choice == "books":
            self.screen.get_screen('moodphotochoice').ids.moodphotochoice_label.text = "Exploring books!"
            self.screen.get_screen('moodphotochoice').ids.art_moodphotochoice.source = "logo/art2.png"
            self.screen.get_screen('moodphotochoice').ids.art_moodphotochoice.size_hint = 0.6, 0.6

    def recommend_thread_starter(self):
        """ Starts the thread for the show_content() function.

        """
        threading.Thread(target=self.show_content).start()

    def show_content(self):
        """ Prepares the content list for the user depending on their current choice of content.
            Adds the list of items to the OneLineListItem for display in the 'contentlist' page.
            Transitions to the 'contentlist' page.

        """
        content_dict = dict()
        self.screen.transition.duration = 0
        self.transition('loadingpage', True)
        if self.current_content_choice == "movies":
            if len(self.content_dict_movies) == 0:
                self.content_dict_movies = recommend(self.y_movies_df, self.merged_movies, self.moviemat, self.movie_dict,
                                                    self.movies_rated, self.movies_liked, self.filt_good_movies_rating_count, self.filt_movies_rating_count)
                content_dict = self.content_dict_movies
            else:
                content_dict = self.content_dict_movies
        elif self.current_content_choice == "books":
            if len(self.content_dict_books) == 0:
                self.content_dict_books = recommend(self.y_books_df, self.merged_books, self.bookmat, self.book_dict,
                                                    self.books_rated, self.books_liked, self.filt_good_books_rating_count, self.filt_books_rating_count)
                content_dict = self.content_dict_books
            else:
                content_dict = self.content_dict_books
        else:
            if len(self.content_dict_songs) == 0:
                self.content_dict_songs = recommend(self.y_songs_df, self.merged_songs, self.songmat, self.song_dict,
                                                    self.songs_rated, self.songs_liked, self.filt_good_songs_rating_count, self.filt_songs_rating_count)
                content_dict = self.content_dict_songs
            else:
                content_dict = self.content_dict_songs

        self.make_list_ui(content_dict)

        self.transition('contentlist', True)

    # @mainthread runs this function in the main thread since all UI elements must be updated in the main thread.
    @mainthread
    def make_list_ui(self, content_dict):
        """ Creates the UI elements of the list of items. UI elements must be updated in the
            main thread.

        Parameters:
        content_dict (dictionary): Dctionary containing the suggestions for a user.

        """
        i = 0
        self.screen.get_screen('contentlist').ids.list_view.clear_widgets()
        for key, value in content_dict.items():
            if i == 24:
                break
            i += 1
            item = OneLineListItem(text=value, on_release=self.show_item)
            item.id = str(key)
            self.screen.get_screen('contentlist').ids.list_view.add_widget(item)

    def show_item(self, obj):
        """ Transitions to and prepares the UI elements of the 'itempage' for the item
            that has been selected from the list.

        Parameters:
        obj (object): Object of the list item that has been selected.

        """
        self.current_item_id = int(obj.id)
        self.screen.get_screen('itempage').ids.item.text = obj.text
        self.screen.get_screen('itempage').ids.userrating.text = 'My rating: Unrated'
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
        """ Enables the transition to a different page.

        Parameters:
        to (str): Name of the page where the app will transition to.
        forward (bool): True if the direction of transition is forward.

        """
        # takes the screen it needs to transition to and if its a forward transition
        if forward:
            self.screen.transition.direction = 'left'
            self.screen.transition.duration = .3
            if to == 'loadingpage':
                self.screen.transition.duration = 0
            if self.screen.current != 'loadingpage':
                self.previousScreen.append(self.screen.current)
            self.screen.current = to
        else:
            self.current_item_id = -1
            self.current_item_rating = 0
            self.screen.get_screen('search').ids.search_field.text = ""
            self.screen.transition.direction = 'right'
            self.screen.transition.duration = .3
            # for going back it does not need a destination
            self.screen.current = self.previousScreen.pop()

    def action_button_thread_starter(self, instance):
        """ Thread starter for the handleFloatingActionButtonSpeedDial() function.

        Parameters:
        instance (obj): Object of the button that has been selected in the speed dial action button.

        """
        if instance.icon == "arrow-left":
            threading.Thread(target=self.handleFloatingActionButtonSpeedDial, args=["arrow-left"]).start()
        elif instance.icon == "logout":
            threading.Thread(target=self.handleFloatingActionButtonSpeedDial, args=["logout"]).start()

    def handleFloatingActionButtonSpeedDial(self, icon_name):
        """ Handles the functions of the back button.
            Stores necessary user information during logout.

        Parameters:
        icon_name (str): Name of the icon of the button that has been pressed in the floating action
                         button.

        """
        if icon_name == "arrow-left":
            self.transition(self.previousScreen, False)
        elif icon_name == "logout":
            self.screen.transition.duration = 0
            self.transition('loadingpage', True)

            # Flushing the UI elements of the signup page.
            self.screen.get_screen('signup').ids.signup_firstname_textfield.text = ""
            self.screen.get_screen('signup').ids.signup_lastname_textfield.text = ""
            self.screen.get_screen('signup').ids.signup_username_textfield.text = ""
            self.screen.get_screen('signup').ids.signup_password_textfield.text = ""

            # Flushing the dictionaries of each content.
            self.content_dict_movies.clear()
            self.content_dict_books.clear()
            self.content_dict_songs.clear()

            # Uploading updated (possibly) versions of the y matrices.
            upload_y_movies(self.y_movies)
            upload_y_songs(self.y_songs)
            upload_y_books(self.y_books)

            self.transition('login_signup', True)

    def signup_thread_starter(self):
        """ Thread starter for the signup function.

        """
        threading.Thread(target=self.signup).start()

    # @mainthread runs this function in the main thread since all UI elements must be updated in the main thread.
    @mainthread
    def dialogue_box_error_ui(self, title, text, button_text):
        """ Creates and opens the dialogue box on the screen.

        Parameters:
        title (str): The title of the dialogue box.
        text (str): The text of the dialogue box.
        button_text (str): Text of the button of the dialogue box.

        """

        cancel_btn_dialogue = MDFlatButton(text=button_text, on_release=self.close_dialogue)
        self.dialogue = MDDialog(title=title, text=text,
                                size_hint=(0.7, 0.2), buttons=[cancel_btn_dialogue])
        self.dialogue.open()

    def signup(self):
        """ Signs the user up after verifications and prepares dataframes necessary for recommendation.
            Transitions to the 'contentchoice' page after all verifications are made.

        """
        self.first_name = self.screen.get_screen('signup').ids.signup_firstname_textfield.text
        first_name_false = True

        self.last_name = self.screen.get_screen('signup').ids.signup_lastname_textfield.text
        last_name_false = True

        self.username = self.screen.get_screen('signup').ids.signup_username_textfield.text
        username_false = True

        self.password = self.screen.get_screen('signup').ids.signup_password_textfield.text
        password_false = True

        if self.first_name.split() == [] or self.last_name.split() == [] or self.username.split() == [] or self.password.split() == []:
            self.dialogue_box_error_ui("Invalid Info", "Please enter valid information and password.", "Retry")
        else:
            if self.username_is_available():
                self.register_user()
                self.screen.transition.duration = 0
                self.transition('loadingpage', True)
                self.y_movies_df = pd.DataFrame(self.y_movies)
                self.y_movies_df = self.y_movies_df.T.stack().reset_index()
                self.y_movies_df.columns = ['user_id','id','rating']
                # casting dtypes for merging
                self.movie_names = self.movie_names.astype({'id': 'int'})
                self.y_movies_df = self.y_movies_df.astype({'id': 'int'})
                # merging 2 dataframes
                self.merged_movies = pd.merge(self.y_movies_df,self.movie_names,on='id')
                # creating moviemat
                self.moviemat = self.merged_movies.pivot_table(index='user_id',columns='name',values='rating')

                self.y_books_df = pd.DataFrame(self.y_books)
                self.y_books_df = self.y_books_df.T.stack().reset_index()
                self.y_books_df.columns = ['user_id','id','rating']
                # casting dtypes for merging
                self.book_names = self.book_names.astype({'id': 'int'})
                self.y_books_df = self.y_books_df.astype({'id': 'int'})
                # merging 2 dataframes
                self.merged_books = pd.merge(self.y_books_df,self.book_names,on='id')
                # creating moviemat
                self.bookmat = self.merged_books.pivot_table(index='user_id',columns='name',values='rating')

                self.y_songs_df = pd.DataFrame(self.y_songs)
                self.y_songs_df = self.y_songs_df.T.stack().reset_index()
                self.y_songs_df.columns = ['user_id','id','rating']
                # casting dtypes for merging
                self.song_names = self.song_names.astype({'id': 'int'})
                self.y_songs_df = self.y_songs_df.astype({'id': 'int'})
                # merging 2 dataframes
                self.merged_songs = pd.merge(self.y_songs_df,self.song_names,on='id')
                # creating moviemat
                self.songmat = self.merged_songs.pivot_table(index='user_id',columns='name',values='rating')

                self.filt_movies_rating_count = ((self.merged_movies['user_id'] == self.user_id) & (self.merged_movies['rating'] > 0.0))
                self.movies_rated = len(self.merged_movies[self.filt_movies_rating_count].index)
                self.filt_good_movies_rating_count = ((self.merged_movies['user_id'] == self.user_id) & (self.merged_movies['rating'] >= 3.0))
                self.movies_liked = len(self.merged_movies[self.filt_good_movies_rating_count].index)

                self.filt_books_rating_count = ((self.merged_books['user_id'] == self.user_id) & (self.merged_books['rating'] > 0.0))
                self.books_rated = len(self.merged_books[self.filt_books_rating_count].index)
                self.filt_good_books_rating_count = ((self.merged_books['user_id'] == self.user_id) & (self.merged_books['rating'] >= 3.0))
                self.books_liked = len(self.merged_books[self.filt_good_books_rating_count].index)

                self.filt_songs_rating_count = ((self.merged_songs['user_id'] == self.user_id) & (self.merged_songs['rating'] > 0.0))
                self.songs_rated = len(self.merged_songs[self.filt_songs_rating_count].index)
                self.filt_good_songs_rating_count = ((self.merged_songs['user_id'] == self.user_id) & (self.merged_songs['rating'] >= 3.0))
                self.songs_liked = len(self.merged_songs[self.filt_good_songs_rating_count].index)

                first_name_false = False
                last_name_false = False
                username_false = False
                password_false = False
            else:
                self.dialogue_box_error_ui("Username Unavailable", "This username is taken. Please try another one.", "Retry")

        if first_name_false is False and last_name_false is False and username_false is False and password_false is False:
            self.screen.get_screen('contentchoice').ids.welcome_label.text = "Welcome, " + self.first_name + "!"
            self.transition('contentchoice', True)

    def close_dialogue(self, obj):
        """ Closes the dialogue box.

        Parameters:
        obj (object): Object of the button that was pressed in the dialogue box.

        """
        self.dialogue.dismiss()

    def change_rating_color(self, rating_value):
        """ Changes the color of the icon buttons based on the rating of the user.

        Parameters:
        rating_value (int): The rating that was given to a certain item by the user.

        """
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
        """ Checks whether an username is available during the user registration process.

        Returns:
        available (bool): True if username is available.

        """
        available = True
        with open('users.json') as json_file:
            data = json.load(json_file)

        for item in data['users']:
            if self.username == item['username']:
                available = False

        return available

    def add_user_vectors(self):
        """ Adds a new vector to the y matrix for the newly registered user.

        """
        my_ratings_movies = np.zeros((self.y_movies.shape[0], 1), dtype=float)
        # adding new user y vector to y rating matrix (movies)
        self.y_movies = np.hstack((self.y_movies, my_ratings_movies))

        my_ratings_songs = np.zeros((self.y_songs.shape[0], 1), dtype=float)
        # adding new user y vector to y rating matrix (songs)
        self.y_songs = np.hstack((self.y_songs, my_ratings_songs))

        my_ratings_books = np.zeros((self.y_books.shape[0], 1), dtype=float)
        # adding new user y vector to y rating matrix (books)
        self.y_books = np.hstack((self.y_books, my_ratings_books))

    def register_user(self):
        """ Generates the new user ID and stores their info in the data store.

        """
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

    def login_thread_starter(self):
        """ Starts the thread for the login function.

        """
        threading.Thread(target=self.login).start()

    def login(self):
        """ Logs the user in and calculates necessary dataframes needed for recommendation.
            Transitions to the 'contentchoice' page after all verifications are made.

        """
        self.username = self.screen.get_screen('login').ids.login_username_textfield.text
        username_false = True

        self.password = self.screen.get_screen('login').ids.login_password_textfield.text
        password_false = True

        if self.username.split() == [] or self.password.split() == []:
            self.dialogue_box_error_ui("Invalid Info", "Please enter valid information and password.", "Retry")

        else:
            if self.verify_user():
                self.fetch_user_info()
                self.screen.transition.duration = 0
                self.transition('loadingpage', True)

                self.y_movies_df = pd.DataFrame(self.y_movies)
                self.y_movies_df = self.y_movies_df.T.stack().reset_index()
                self.y_movies_df.columns = ['user_id','id','rating']
                # casting dtypes for merging
                self.movie_names = self.movie_names.astype({'id': 'int'})
                self.y_movies_df = self.y_movies_df.astype({'id': 'int'})
                # merging 2 dataframes
                self.merged_movies = pd.merge(self.y_movies_df,self.movie_names,on='id')
                # creating moviemat
                self.moviemat = self.merged_movies.pivot_table(index='user_id',columns='name',values='rating')

                self.y_books_df = pd.DataFrame(self.y_books)
                self.y_books_df = self.y_books_df.T.stack().reset_index()
                self.y_books_df.columns = ['user_id','id','rating']
                # casting dtypes for merging
                self.book_names = self.book_names.astype({'id': 'int'})
                self.y_books_df = self.y_books_df.astype({'id': 'int'})
                # merging 2 dataframes
                self.merged_books = pd.merge(self.y_books_df,self.book_names,on='id')
                # creating moviemat
                self.bookmat = self.merged_books.pivot_table(index='user_id',columns='name',values='rating')

                self.y_songs_df = pd.DataFrame(self.y_songs)
                self.y_songs_df = self.y_songs_df.T.stack().reset_index()
                self.y_songs_df.columns = ['user_id','id','rating']
                # casting dtypes for merging
                self.song_names = self.song_names.astype({'id': 'int'})
                self.y_songs_df = self.y_songs_df.astype({'id': 'int'})
                # merging 2 dataframes
                self.merged_songs = pd.merge(self.y_songs_df,self.song_names,on='id')
                # creating moviemat
                self.songmat = self.merged_songs.pivot_table(index='user_id',columns='name',values='rating')

                self.filt_movies_rating_count = ((self.merged_movies['user_id'] == self.user_id) & (self.merged_movies['rating'] > 0.0))
                self.movies_rated = len(self.merged_movies[self.filt_movies_rating_count].index)
                self.filt_good_movies_rating_count = ((self.merged_movies['user_id'] == self.user_id) & (self.merged_movies['rating'] >= 3.0))
                self.movies_liked = len(self.merged_movies[self.filt_good_movies_rating_count].index)

                self.filt_books_rating_count = ((self.merged_books['user_id'] == self.user_id) & (self.merged_books['rating'] > 0.0))
                self.books_rated = len(self.merged_books[self.filt_books_rating_count].index)
                self.filt_good_books_rating_count = ((self.merged_books['user_id'] == self.user_id) & (self.merged_books['rating'] >= 3.0))
                self.books_liked = len(self.merged_books[self.filt_good_books_rating_count].index)

                self.filt_songs_rating_count = ((self.merged_songs['user_id'] == self.user_id) & (self.merged_songs['rating'] > 0.0))
                self.songs_rated = len(self.merged_songs[self.filt_songs_rating_count].index)
                self.filt_good_songs_rating_count = ((self.merged_songs['user_id'] == self.user_id) & (self.merged_songs['rating'] >= 3.0))
                self.songs_liked = len(self.merged_songs[self.filt_good_songs_rating_count].index)

                username_false = False
                password_false = False
            else:
                self.dialogue_box_error_ui("Login Failed", "Username and Password do not match.", "Retry")

        if username_false is False and password_false is False:
            self.screen.get_screen('contentchoice').ids.welcome_label.text = "Welcome, " + self.first_name + "!"
            self.transition('contentchoice', True)

    def verify_user(self):
        """ Verifies user credentials while logging in.

        """
        verified = False
        with open('users.json') as json_file:
            data = json.load(json_file)

        for item in data['users']:
            if self.username == item['username'] and self.password == item['password']:
                verified = True
                break
        return verified

    def fetch_user_info(self):
        """ Fetches user information from the data store after login is successful.

        """
        with open('users.json') as json_file:
            data = json.load(json_file)
        for item in data['users']:
            if self.username == item['username'] and self.password == item['password']:
                self.first_name = item['first_name']
                self.last_name = item['last_name']
                self.user_id = item['user_id']

    def save_rating_changes(self):
        """ Saves the changes after user has given a rating to a certain item.

        """
        if self.current_item_id != -1 and self.current_item_rating != 0:
            if self.current_content_choice == "movies":
                self.y_movies = rate(self.current_item_id, self.user_id, self.y_movies,
                                                    self.current_item_rating)
            elif self.current_content_choice == "books":
                self.y_books = rate(self.current_item_id, self.user_id, self.y_books,
                                                  self.current_item_rating)
            else:
                self.y_songs = rate(self.current_item_id, self.user_id, self.y_songs,
                                                  self.current_item_rating)

    def camera_thread_starter(self):
        """ Starts the thread for the get_mood() function.

        """
        threading.Thread(target=self.get_mood).start()

    # @mainthread runs this function in the main thread since all UI elements must be updated in the main thread.
    @mainthread
    def create_dialogue_box_mood(self, mood):
        """ Creates and opens the dialogue box to notify the detected mood of the user.

        Parameters:
        mood (str): Detected mood.

        """
        cancel_btn_dialogue = MDFlatButton(text="Ok!", on_release=self.close_dialogue)
        self.dialogue = MDDialog(title="Mood Detected: " + mood, text="Enjoy exploring " + mood + " " + self.current_content_choice + "!",
                                size_hint=(0.7, 0.2), buttons=[cancel_btn_dialogue])
        self.dialogue.open()

    # @mainthread runs this function in the main thread since all UI elements must be updated in the main thread.
    @mainthread
    def create_dialogue_box_noFace(self):
        """ Creates opens the dialogue box to notify the user that no face was detected.

        """
        cancel_btn_dialogue = MDFlatButton(text="Retry", on_release=self.close_dialogue)
        self.dialogue = MDDialog(title="No Faces Detected", text="Please check if there is sufficient light.",
                                size_hint=(0.7, 0.2), buttons=[cancel_btn_dialogue])
        self.dialogue.open()

    def get_mood(self):
        """ Opens the camera and predicts the mood of the user from their image.

        """
        self.screen.transition.duration = 0
        self.transition('loadingpage', True)
        if take_photo():
            mood = detect_mood("data/capture.png", self.model)
            if mood != "No faces detected":
                self.mood_filter(mood)
            else:
                self.create_dialogue_box_noFace()
                self.transition('camerapage', True)

    def mood_filter_thread_starter(self, mood):
        """ Starts the thread for the mood_filter() function.

        """
        threading.Thread(target=self.mood_filter, args=[mood]).start()

    def mood_filter(self, mood):
        """ Filters content according to the mood of the user.
            Transitions to the 'contentlist' page to display the filtered content.

        Parameters:
        mood (str): Name of the mood of the user.

        """
        self.create_dialogue_box_mood(mood)
        content_dict = dict()
        self.screen.transition.duration = 0
        self.transition('loadingpage', True)
        if self.current_content_choice == "movies":
            if len(self.content_dict_movies) == 0:
                self.content_dict_movies = recommend(self.y_movies_df, self.merged_movies, self.moviemat, self.movie_dict,
                                                    self.movies_rated, self.movies_liked, self.filt_good_movies_rating_count, self.filt_movies_rating_count)
                content_dict = self.content_dict_movies
                content_dict = filter_content_movies(mood, content_dict)
            else:
                content_dict = self.content_dict_movies
                content_dict = filter_content_movies(mood, content_dict)
        elif self.current_content_choice == "books":
            if len(self.content_dict_books) == 0:
                self.content_dict_books = recommend(self.y_books_df, self.merged_books, self.bookmat, self.book_dict,
                                                    self.books_rated, self.books_liked, self.filt_good_books_rating_count, self.filt_books_rating_count)
                content_dict = self.content_dict_books
                content_dict = filter_content_books(mood, content_dict)
            else:
                content_dict = self.content_dict_books
                content_dict = filter_content_books(mood, content_dict)
        else:
            if len(self.content_dict_songs) == 0:
                self.content_dict_songs = recommend(self.y_songs_df, self.merged_songs, self.songmat, self.song_dict,
                                                    self.songs_rated, self.songs_liked, self.filt_good_songs_rating_count, self.filt_songs_rating_count)
                content_dict = self.content_dict_songs
                content_dict = filter_content_songs(mood, content_dict)
            else:
                content_dict = self.content_dict_songs
                content_dict = filter_content_songs(mood, content_dict)

        self.make_list_ui(content_dict)

        self.transition('contentlist', True)

    def search_item(self, searching):
        """ Allows the user to search for any item.

        Parameters:
        searching (bool): True if the user is searching for something.

        """
        if self.current_content_choice == "movies":
            demo_dict = self.movie_dict
        elif self.current_content_choice == "songs":
            demo_dict = self.song_dict
        else:
            demo_dict = self.book_dict

        self.screen.get_screen('search').ids.search_list_view.clear_widgets()
        search_key = ""
        search_key = self.screen.get_screen('search').ids.search_field.text
        i = 0
        for key, value in demo_dict.items():
            if searching and search_key != "":
                if search_key in key and i <= 20:
                    i += 1
                    item = OneLineListItem(text=key, on_release=self.show_item)
                    item.id = str(value)
                    self.screen.get_screen('search').ids.search_list_view.add_widget(item)


DemoUI().run()
