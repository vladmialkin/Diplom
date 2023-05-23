import flet
from views.view import View


class AuthView(View):
    def __init__(self, route):
        super().__init__(route=route)
        self.horizontal_alignment = "center"
        self.vertical_alignment = "center"

        self.frame_entry = flet.Column(alignment=flet.alignment.center)
        self.frame_buttons = flet.Column(alignment=flet.alignment.center, horizontal_alignment=flet.alignment.center)

        self.login_entry = flet.TextField(label="Логин", width=500)
        self.password_entry = flet.TextField(label="Пароль", width=500, password=True, can_reveal_password=True)

        self.auth_button = flet.ElevatedButton(text="Войти")  # on_click=self.auth_btn_click
        self.check_box = flet.Checkbox(label="Сохранить пароль", width=500)  # on_change=self.checkbox_changed

        self.append_widgets(self.frame_entry, [self.login_entry, self.password_entry])
        self.append_widgets(self.frame_buttons, [self.check_box, self.auth_button])
        self.append_widgets(self, [self.frame_entry, self.frame_buttons])
