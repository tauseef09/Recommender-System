screens = """
ScreenManager:
    AppLoad:
    LoginSignup:
    Login:
    Signup:
    MainMenu:
    ContentChoice:
    ContentList:

<AppLoad>:
    name: 'appload'
    Image:
        source: 'logo/logo.png'
        size: self.texture_size
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
    MDProgressBar:
        id: progress_bar
        value: 0
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        size_hint: (0.75, 1)

<LoginSignup>:
    name: 'login_signup'
    Image:
        source: 'logo/logo.png'
        size: self.texture_size
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
    MDRectangleFlatButton:
        text: 'Login'
        pos_hint: {'center_x': 0.5, 'center_y': 0.35}
        theme_text_color: 'Custom'
        text_color: 38/255, 50/255, 56/255, 1
        on_release:
            app.transition('login', True)
    MDRectangleFlatButton:
        text: 'Signup'
        pos_hint: {'center_x': 0.5, 'center_y': 0.25}
        theme_text_color: 'Custom'
        text_color: 38/255, 50/255, 56/255, 1
        on_release:
            app.transition('signup', True)

<Login>:
    name: 'login'
    Image:
        source: 'logo/logo.png'
        size_hint: 0.5, 0.5
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
    MDTextField:
        id: login_username_textfield
        pos_hint: {'center_x': 0.5, 'center_y': 0.57}
        size_hint: (0.7, 0.1)
        hint_text: "Username"
        helper_text: "Required"
        helper_text_mode: 'on_error'
        required: True
    MDTextField:
        id: login_password_textfield
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint: (0.7, 0.1)
        hint_text: "Password"
        helper_text: "Required"
        helper_text_mode: 'on_error'
        required: True
        password: True
    MDRectangleFlatButton:
        text: "Login"
        pos_hint: {'center_x': 0.5, 'center_y': 0.25}
        on_release:
            app.transition('contentchoice', True)
        theme_text_color: 'Custom'
        text_color: 38/255, 50/255, 56/255, 1

<Signup>:
    name: 'signup'
    Image:
        source: 'logo/logo.png'
        size_hint: 0.5, 0.5
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
    MDTextField:
        id: signup_firstname_textfield
        pos_hint: {'center_x': 0.5, 'center_y': 0.76}
        size_hint: (0.7, 0.1)
        hint_text: "First Name"
        helper_text: "Required"
        helper_text_mode: 'on_error'
        required: True
    MDTextField:
        id: signup_lastname_textfield
        pos_hint: {'center_x': 0.5, 'center_y': 0.64}
        size_hint: (0.7, 0.1)
        hint_text: "Last Name"
        helper_text: "Required"
        helper_text_mode: 'on_error'
        required: True
    MDTextField:
        id: signup_username_textfield
        pos_hint: {'center_x': 0.5, 'center_y': 0.52}
        size_hint: (0.7, 0.1)
        hint_text: "Username"
        helper_text: "Required"
        helper_text_mode: 'on_error'
        required: True
    MDTextField:
        id: signup_password_textfield
        pos_hint: {'center_x': 0.5, 'center_y': 0.40}
        size_hint: (0.7, 0.1)
        hint_text: "Password"
        helper_text: "Required"
        helper_text_mode: 'on_error'
        required: True
        password: True
    MDRectangleFlatButton:
        text: "Signup"
        pos_hint: {'center_x': 0.5, 'center_y': 0.25}
        on_release:
            app.transition('contentchoice', True)
        theme_text_color: 'Custom'
        text_color: 38/255, 50/255, 56/255, 1

<ContentChoice>:
    name: 'contentchoice'
    MDLabel:
        text: "Welcome, Tauseef!"
        halign: 'center'
        pos_hint: {'center_y': 0.85}
        font_style: 'H4'
        theme_text_color: 'Custom'
        text_color: 38/255, 50/255, 56/255, 1
    MDLabel:
        text: "What are you in the mood for?"
        halign: 'center'
        pos_hint: {'center_y': 0.73}
        font_style: 'Subtitle1'
        theme_text_color: 'Custom'
        text_color: 153/255, 153/255, 153/255, 1
    MDRectangleFlatButton:
        text: "Movies"
        pos_hint: {'center_x': 0.5, 'center_y': 0.63}
        theme_text_color: 'Custom'
        text_color: 38/255, 50/255, 56/255, 1
        on_release: app.choice_movies()
    MDRectangleFlatButton:
        text: "Songs"
        pos_hint: {'center_x': 0.5, 'center_y': 0.53}
        theme_text_color: 'Custom'
        text_color: 38/255, 50/255, 56/255, 1
        on_release: app.choice_songs()
    MDRectangleFlatButton:
        text: "Books"
        pos_hint: {'center_x': 0.5, 'center_y': 0.43}
        theme_text_color: 'Custom'
        text_color: 38/255, 50/255, 56/255, 1
        on_release: app.choice_books()
    MDFloatingActionButtonSpeedDial:
        data: {'logout': 'Logout', 'arrow-left': 'Back',}
        callback: app.handleFloatingActionButtonSpeedDial
        rotation_root_button: True
        hint_animation: True
        label_text_color: [239/255, 239/255, 239/255, 1]
        bg_hint_color: [38/255, 50/255, 56/255, 1]
        bg_color_stack_button: [38/255, 50/255, 56/255, 1]
        bg_color_root_button: [38/255, 50/255, 56/255, 1]
        color_icon_root_button: [239/255, 239/255, 239/255, 1]
        color_icon_stack_button: [239/255, 239/255, 239/255, 1]

<MainMenu>:
    name: 'mainmenu'
    MDLabel:
        id: main_menu_label
        text: "Welcome, Tauseef!"
        halign: 'center'
        pos_hint: {'center_y': 0.85}
        font_style: 'H4'
        theme_text_color: 'Custom'
        text_color: 38/255, 50/255, 56/255, 1
    MDRectangleFlatButton:
        text: "Based on Ratings"
        pos_hint: {'center_x': 0.5, 'center_y': 0.63}
        theme_text_color: 'Custom'
        text_color: 38/255, 50/255, 56/255, 1
        on_release: app.show_content()
    MDRectangleFlatButton:
        text: "Based on Mood"
        pos_hint: {'center_x': 0.5, 'center_y': 0.53}
        theme_text_color: 'Custom'
        text_color: 38/255, 50/255, 56/255, 1
        on_release: app.show_content()
    MDRectangleFlatButton:
        text: "Search Content"
        pos_hint: {'center_x': 0.5, 'center_y': 0.43}
        theme_text_color: 'Custom'
        text_color: 38/255, 50/255, 56/255, 1
    Image:
        id: art
        source: 'logo/art1.png'
        size_hint: 0.6, 0.6
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
    MDFloatingActionButtonSpeedDial:
        data: {"logout":"Logout", "arrow-left":"Back"}
        callback: app.handleFloatingActionButtonSpeedDial
        rotation_root_button: True
        hint_animation: True
        label_text_color: [239/255, 239/255, 239/255, 1]
        bg_hint_color: [38/255, 50/255, 56/255, 1]
        bg_color_stack_button: [38/255, 50/255, 56/255, 1]
        bg_color_root_button: [38/255, 50/255, 56/255, 1]
        color_icon_root_button: [239/255, 239/255, 239/255, 1]
        color_icon_stack_button: [239/255, 239/255, 239/255, 1]

<ContentList>:
    name: 'contentlist'
    ScrollView:
        MDList:
            id: list_view
    MDFloatingActionButtonSpeedDial:
        data: {"logout":"Logout", "arrow-left":"Back"}
        callback: app.handleFloatingActionButtonSpeedDial
        rotation_root_button: True
        hint_animation: True
        label_text_color: [239/255, 239/255, 239/255, 1]
        bg_hint_color: [38/255, 50/255, 56/255, 1]
        bg_color_stack_button: [38/255, 50/255, 56/255, 1]
        bg_color_root_button: [38/255, 50/255, 56/255, 1]
        color_icon_root_button: [239/255, 239/255, 239/255, 1]
        color_icon_stack_button: [239/255, 239/255, 239/255, 1]
"""
