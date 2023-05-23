from controllers.contoller import Controller
from views.admin_view import AdminView
from models.admin_model import AdminModel
from windows import ExitMenuDialog, WorkingHoursDialog


class AdminController(Controller):
    def __init__(self, redmine, database, user_model):
        super().__init__()
        self.view = AdminView(route="admin")
        self.model = AdminModel(redmine=redmine, database=database, user_model=user_model)

        self.view.dropdown_db.value = self.model.database.db_host

        self.view.worker_mode_item.on_click = self.worker_mode_click
        self.view.supervisor_mode_item.on_click = self.supervisor_mode_click
        self.view.button_save.on_click = self.save_new_working_hours
        self.view.button_cansel.on_click = self.cansel_new_working_hours
        self.view.update_working_hours_button.on_click = self.update_working_hours_on_click

        self.view.insert_new_year_button.on_click = self.insert_new_year
        self.view.button_year_cansel.on_click = self.cansel_new_year
        self.view.button_year_save.on_click = self.save_new_year
        self.view.button_cansel.on_click = self.cansel_new_working_hours

        self.view.dropdown_db.on_change = self.change_db_click
        self.view.insert_months_drop_box(self.model.database.db_list)

        self.insert_table()
        self.insert_dropdowns()

        self.view.author_login.content.value = self.model.user_model.user_login
        self.view.author_login.on_click = self.check_exit

    def change_db_click(self, event):
        """функция изменяет БД на выбранную из выпадающего списка"""
        new_db_host = self.view.dropdown_db.value
        self.model.database.db_host = new_db_host
        self.model.database.connection()
        self.model.database.check_table()

    def worker_mode_click(self, event):
        """функция переходит в view работника при нажатии кнопки"""
        self.mode_click("worker")

    def supervisor_mode_click(self, event):
        """функция переходит в view руководителя при нажатии кнопки"""
        self.mode_click("supervisor")

    def mode_click(self, route):
        """функция переходин на выбранную страницу"""
        views = self.view.page.views
        for view in views:
            if view.route == route:
                self.view.page.views.remove(view)
                self.view.page.views.append(view)
                self.view.page.go(view.route)
        self.view.page.update()

    def check_exit(self, event):
        """функция выхода из аккаунта"""
        self.view.page.dialog = ExitMenuDialog()
        self.view.page.update()
        self.view.page.dialog.show_dialog()

    def insert_table(self):
        """функция заполняет таблицу данными"""
        table = self.view.table
        headlines = self.model.date.rus_months_list.copy()
        headlines.insert(0, 'Год')
        working_hours = self.model.working_hours.read_working_hours()
        self.view.create_working_hours_table(headlines=headlines, values=working_hours)

    def insert_dropdowns(self):
        self.view.year_dropdown.options.clear()
        self.view.month_dropdown.options.clear()
        years = self.model.working_hours.read_working_hours().keys()
        self.view.insert_to_dropdown(dropdown=self.view.year_dropdown, values=years)
        self.view.year_dropdown.value = self.view.year_dropdown.options[0].key
        self.view.insert_to_dropdown(dropdown=self.view.month_dropdown, values=self.model.date.rus_months_list)
        self.view.month_dropdown.value = self.view.month_dropdown.options[0].key
        self.view.hours_input.value = 0.0

    def cell_on_click(self, event):
        self.view.page.dialog = WorkingHoursDialog()
        self.view.page.update()
        self.view.page.dialog.show_dialog(self.model.working_hours)

    def cansel_new_working_hours(self, event):
        self.view.update_working_hours_row.visible = False
        self.view.page.update()

    def save_new_working_hours(self, event):
        year = self.view.year_dropdown.value
        month = self.view.month_dropdown.value
        hours = self.view.hours_input.value
        self.model.working_hours.insert_working_hours(year=year, month=month, hours=hours)
        self.view.table.controls.clear()
        self.insert_table()
        self.view.update_working_hours_row.visible = False
        self.view.page.update()

    def update_working_hours_on_click(self, event):
        self.view.update_working_hours_row.visible = True
        self.view.page.update()

    def insert_new_year(self, event):
        self.view.new_year_row.visible = True
        self.view.page.update()

    def save_new_year(self, event):
        year = self.view.year_input.value
        if year is not None:
            fl = self.model.working_hours.create_new_year(year=year)
            if fl == 1:
                self.view.table.controls.clear()
                self.insert_table()
                self.insert_dropdowns()
                self.view.new_year_row.visible = False
            else:
                self.view.year_input.error_text = "Год уже существует"
        else:
            self.view.year_input.error_text = "Год не указан"
        self.view.page.update()

    def cansel_new_year(self, event):
        self.view.new_year_row.visible = False
        self.view.page.update()
