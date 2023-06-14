from controllers.contoller import Controller
from models.auth_model import AuthModel
from views.auth_view import AuthView


class AuthController(Controller):
    def __init__(self, worker_controller, supervisor_controller, admin_controller):
        super().__init__()
        self.view = AuthView(route="auth")
        self.model = AuthModel()
        self.worker_controller = worker_controller
        self.supervisor_controller = supervisor_controller
        self.admin_controller = admin_controller

        self.view.auth_button.on_click = self.authorization

    def authorization(self, event):
        """функция авторизации аккаунта Redmine"""
        try:
            connect = self.model.authorization(login=self.view.login_entry.value,
                                               password=self.view.password_entry.value)
            if connect is None:
                self.worker_controller(redmine=self.model.redmine, database=self.model.database,
                                       user_model=self.model.user_model)
                self.supervisor_controller(redmine=self.model.redmine, database=self.model.database,
                                           user_model=self.model.user_model)
                self.admin_controller(redmine=self.model.redmine, database=self.model.database,
                                      user_model=self.model.user_model)
            else:
                self.view.login_entry.error_text = connect
                self.view.password_entry.error_text = connect
                self.view.update()
        except Exception as e:
            print(e)