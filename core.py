import flet

from controllers.auth_controller import AuthController
from controllers.worker_controller import WorkerController
from controllers.supervisor_controller import SupervisorController
from controllers.admin_controller import AdminController
from redmine_api import RedmineApi
from database import DataBase


class Core:
    def __init__(self, page):
        self.page = page
        self.page.window_width = 1920
        self.page.window_height = 1080
        self.page.title = "Redmine Helper"
        self.page.window_center()
        self.page.on_route_change = self.on_route_change
        self.page.on_keyboard_event = self.keyboard_event
        self.page.on_view_pop = self.exit

        self.auth_controller = None
        self.worker_controller = None
        self.supervisor_controller = None
        self.admin_controller = None

        self.redmine = RedmineApi()
        self.database = DataBase()
        self.user_model = None
        self.auth()
        self.page.update()

    def keyboard_event(self, event):
        """функция работает при нажатии горячей клавиши"""
        if self.page.route == "auth" and event.key == 'Enter':
            self.auth_controller.authorization(None)

    def exit(self, view):
        """функция возвращает пользователя в окно авторизации"""
        """
        Код подразумевает , что при создании окна запускаются все view и при возврате 
        к /osn... view другие view не будут удалятся.
        """
        list_views = self.page.views
        if view.view.route == "supervisor" or view.view.route == "worker":
            for view in list_views:
                print(view.route)
                if view.view.route == "auth":
                    top_view = view
                    list_views.clear()
                    list_views.append(top_view)
                    self.page.go(top_view.route)
        else:
            last_view = list_views[-2]
            list_views.remove(last_view)
            list_views.append(last_view)
            self.page.go(last_view.route)
        view.view.page.update()

    def on_route_change(self, event):
        """функция вызывается при изменении адреса окна"""
        pass

    def add_new_view(self, view: list):
        """функция добавления новой страницы в список"""
        self.page.views.append(view)

    def auth(self):
        """авторизация в аккаунте Redmine и БД"""
        self.auth_controller = AuthController(worker_controller=self.worker, supervisor_controller=self.supervisor,
                                              admin_controller=self.admin)
        self.add_new_view(self.auth_controller.view)
        self.page.go(self.auth_controller.view.route)

    def worker(self, redmine, database, user_model):
        """функция запуска страницы для работника"""

        self.worker_controller = WorkerController(redmine=redmine, database=database,
                                                  user_model=user_model)
        self.add_new_view(self.worker_controller.view)
        self.page.go(self.worker_controller.view.route)

    def supervisor(self, redmine, database, user_model):
        """функция запуска страницы для руководителя"""
        self.supervisor_controller = SupervisorController(redmine=redmine, database=database,
                                                          user_model=user_model)
        self.add_new_view(self.supervisor_controller.view)

    def admin(self, redmine, database, user_model):
        """функция запуска страницы для руководителя"""
        self.admin_controller = AdminController(redmine=redmine, database=database,
                                                user_model=user_model)
        self.add_new_view(self.admin_controller.view)
