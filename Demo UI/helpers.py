screens = """
ScreenManager:
    AppLoad:
    LoginSignup:
    Login:
    Signup:
    Menu:

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
        on_release:
            root.manager.transition.direction = 'left'
            root.manager.current = 'login'
    MDRectangleFlatButton:
        text: 'Signup'
        pos_hint: {'center_x': 0.5, 'center_y': 0.25}
        on_release:
            root.manager.transition.direction = 'left'
            root.manager.current = 'signup'

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
            root.manager.transition.direction = 'left'
            root.manager.current = 'menu'

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
            root.manager.transition.direction = 'left'
            root.manager.current = 'menu'

<Menu>:
    name: 'menu'
    MDLabel:
        text: 'Welcome, User!'
        halign: 'center'
        pos_hint:{'center_x': 0.5, 'center_y': 0.9}
        font_style: 'H4'
        theme_text_color: 'Secondary'
        font_size: '30sp'
    MDRectangleFlatButton:
        text: 'Suggestion'
        pos_hint: {'center_x': 0.5, 'center_y': 0.65}
    MDRectangleFlatButton:
        text: 'Mood'
        pos_hint: {'center_x': 0.5, 'center_y': 0.55}
    MDRectangleFlatButton:
        text: 'Search'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
    Image:
        source: 'logo/art6.jpg'
        size_hint: 0.6, 0.6
        pos_hint: {'center_x': 0.35, 'center_y': 0.18}
    MDFloatingActionButtonSpeedDial:
        root_button_anim: True
        data: {'logout': 'Logout', 'power': 'Quit',}
        callback: app.handleFloatingActionButton

"""
