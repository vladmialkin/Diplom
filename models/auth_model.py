from models.model import Model
from models.user_model import UserModel
import redminelib


class AuthModel(Model):
    def __init__(self):
        super().__init__()
        self.error_authorization = "Неверно введен логин/пароль"
        self.error_emptiness = "Поле логин/пароль не заполнено"
        self.user_model = None

    def authorization(self, login, password):
        if login == "" or password == "":
            return "Поле не может быть пустым"
        try:
            self.redmine.connecting(login, password)
            self.database.connecting()
            self.user_model = UserModel(redmine=self.redmine, database=self.database)
            return None
        except redminelib.exceptions.AuthError:
            return "Не верно введен логин/пароль"
        except Exception as e:
            return "Неизвестная ошибка"
