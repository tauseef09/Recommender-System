screens = """
ScreenManager:
    AppLoad:
    LoginSignup:
    Login:
    Signup:

<AppLoad>:
    name: 'appload'
    Image: 
        source: 'logo.png'
        size: self.texture_size
    MDProgressBar:
        id: progress_bar
        value: 0
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        size_hint: (0.75, 1) 
        
<LoginSignup>:
    name: 'login_signup'
    Image:
        source: 'logo.png'
        size: self.texture_size
    MDRectangleFlatButton:
        text: 'Login'
        pos_hint: {'center_x': 0.5, 'center_y': 0.35}
        on_release:
            root.manager.current = 'login'
    MDRectangleFlatButton:
        text: 'Signup'
        pos_hint: {'center_x': 0.5, 'center_y': 0.25}
        on_release:
            root.manager.current = 'signup'
        
<Login>:
    name: 'login'
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
        
<Signup>:
    name: 'signup'
    MDTextField:
        id: signup_firstname_textfield
        pos_hint: {'center_x': 0.5, 'center_y': 0.76}
        size_hint: (0.7, 0.1)
        hint_text: "First Name"
        helper_text: "Required"
        helper_text_mode: 'on_error'
        required: True
    MDTextField:
        id: login_lastname_textfield
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
        
"""