from controllers.contoller import Controller
from views.supervisor_view import SupervisorView
from models.supervisor_model import SupervisorModel
from windows import ExitMenuDialog, ResultIssueDialog
from controllers.issue_controller import IssueController
from controllers.laborcosts_controller import LaborcostsController
import threading


class SupervisorController(Controller):
    def __init__(self, redmine, database, user_model):
        super().__init__()
        self.view = SupervisorView(route="supervisor")
        self.model = SupervisorModel(redmine=redmine, database=database, user_model=user_model)

        self.view.worker_mode_item.on_click = self.worker_mode_click
        self.view.admin_mode_item.on_click = self.admin_mode_click

        self.view.plan_button.on_click = self.plan_btn_click
        self.view.report_button.on_click = self.report_btn_click
        self.view.pdf_button.on_click = self.create_pdf_click

        self.insert_date()

        self.view.author_login.content.value = self.model.user_model.user_login
        self.view.author_login.on_click = self.check_exit

    def worker_mode_click(self, event):
        """функция нажатия на кнопку перехода на страницу работника"""
        self.mode_click("worker")

    def admin_mode_click(self, event):
        """функция нажатия на кнопку перехода на страницу администратора при наличии прав"""
        if self.model.user_model.supervisor_rights is True:
            self.mode_click("admin")

    def mode_click(self, route):
        """функция переходин на выбранную страницу"""
        views = self.view.page.views
        for view in views:
            if view.route == route:
                self.view.page.views.remove(view)
                self.view.page.views.append(view)
                self.view.page.go(view.route)
        self.view.page.update()

    def plan_btn_click(self, event):
        """функция нажатия на кнопку создания плана задач"""
        self.update_disabled_buttons()
        self.view.now_issues_row.controls[0].value = "План"
        self.model.state = "План"
        self.view.frame_table.controls.clear()
        self.model.selected_date = f"{self.view.months_dropdown.value} {self.view.year_dropdown.value}"
        workers_list = self.model.get_workers_sector_list(self.view.sector_dropdown.value)
        self.model.workers = workers_list
        self.model.pdf.site = None
        self.model.pdf.supervizor_create_table(state=self.model.state, sector=self.view.sector_dropdown.value,
                                               plan_month=self.model.selected_date)
        need_hours = self.model.working_hours.get_hours(year=self.view.year_dropdown.value,
                                                        month=self.view.months_dropdown.value)
        for worker in workers_list:
            self.get_planed_issues(user_id=worker, need_hours=need_hours)
            self.model.pdf.create_new_row(data=self.model.values_issues, user_name=self.model.worker,
                                          now_date=self.model.date.str_now_date,
                                          plan_costs=self.model.sum_planned_hours,
                                          fact_costs=self.model.sum_fact_hours,
                                          norm_costs=need_hours,
                                          plan_month=self.model.selected_date)
        self.update_disabled_buttons()

    def report_btn_click(self, event):
        """функция нажатия на кнопку создания отчета задач"""
        self.update_disabled_buttons()
        self.view.now_issues_row.controls[0].value = "Отчет"
        self.model.state = "Отчет"
        self.view.frame_table.controls.clear()
        self.model.selected_date = f"{self.view.months_dropdown.value} {self.view.year_dropdown.value}"
        workers_list = self.model.get_workers_sector_list(self.view.sector_dropdown.value)
        self.model.workers = workers_list
        self.model.pdf.site = None
        self.model.pdf.supervizor_create_table(state=self.model.state, sector=self.view.sector_dropdown.value,
                                               plan_month=self.model.selected_date)
        need_hours = self.model.working_hours.get_hours(year=self.view.year_dropdown.value,
                                                        month=self.view.months_dropdown.value)

        for worker in workers_list:
            self.get_fact_issues(user_id=worker, need_hours=need_hours)
            self.model.pdf.create_new_row(data=self.model.values_issues, user_name=self.model.worker,
                                          now_date=self.model.date.str_now_date,
                                          plan_costs=self.model.sum_planned_hours,
                                          fact_costs=self.model.sum_fact_hours,
                                          norm_costs=need_hours,
                                          plan_month=self.model.selected_date)
        self.update_disabled_buttons()

    def insert_date(self):
        """функция добавляет список месяцев и годов в выпадающие списки"""
        self.view.insert_values_to_dropdown(self.model.months_list, self.model.now_month,
                                            self.view.months_dropdown)
        self.view.insert_values_to_dropdown(self.model.years_list, self.model.now_year, self.view.year_dropdown)
        self.view.insert_values_to_dropdown(self.model.sectors, self.model.user_model.sector, self.view.sector_dropdown)

    def check_exit(self, event):
        """функция нажатия на кнопку выхода для подтверждения выхода"""
        self.view.page.dialog = ExitMenuDialog()
        self.view.page.update()
        self.view.page.dialog.show_dialog()

    def cell_on_click(self, event):
        """функция нажатия на ячейку таблицы"""
        column_count = event.control.data.get("column_count")
        worker_id = event.control.data.get("worker_id")
        issue = event.control.data.get("issue")
        if column_count == 0 or column_count == 1:
            """переход к странице информации о задаче"""
            self.issue_info_click(issue=issue)
        elif column_count == 3:
            """переход к странице плановых трудозатрат"""
            self.planned_labor_costs_click(issue=issue, worker=worker_id)
        elif column_count == 4:
            """переход к странице фактических трудозатрат"""
            self.fact_labor_costs_click(issue=issue, worker=worker_id)
        elif column_count == 8:
            """переход в окно отображения результата задачи"""
            self.result_click(issue=issue)

    def issue_info_click(self, issue):
        """функция запуска страницы информации о задаче"""
        issue_controller = IssueController(redmine=self.model.redmine, database=self.model.database,
                                           user_model=self.model.user_model,
                                           issue=issue, worker_model=self.model)
        self.view.page.views.append(issue_controller.view)
        self.view.page.go(issue_controller.view.route)

    def planned_labor_costs_click(self, issue, worker):
        """функция нажатия на кнопку перехода на страницу плановых трудозатрат задачи"""
        laborcosts_controller = LaborcostsController(redmine=self.model.redmine, database=self.model.database,
                                                     user_model=self.model.user_model,
                                                     issue=issue, worker_model=self.model, flag=0, user=worker)
        self.view.page.views.append(laborcosts_controller.view)
        self.view.page.go(laborcosts_controller.view.route)

    def fact_labor_costs_click(self, issue, worker):
        """функция нажатия на кнопку перехода на страницу фактических трудозатрат задачи"""
        laborcosts_controller = LaborcostsController(redmine=self.model.redmine, database=self.model.database,
                                                     user_model=self.model.user_model,
                                                     issue=issue, worker_model=self.model, flag=1, user=worker)
        self.view.page.views.append(laborcosts_controller.view)
        self.view.page.go(laborcosts_controller.view.route)

    def result_click(self, issue):
        """функция нажатия на ячейку результата для вывода окна редактирования результата задачи"""
        self.view.page.dialog = ResultIssueDialog()
        self.view.page.update()
        self.view.page.dialog.show_dialog(issue=issue, database=self.model.database)

    def update_disabled_buttons(self):
        """функция изменят видимость кнопок"""
        if self.view.plan_button.disabled is True:
            self.view.frame_table.visible = True
            self.view.plan_button.disabled = False
            self.view.report_button.disabled = False
            self.view.frame_progress_bar.visible = False
            self.view.pdf_button.visible = True
        else:
            self.view.frame_table.visible = False
            self.view.pdf_button.visible = False
            self.view.frame_progress_bar.visible = True
            self.view.plan_button.disabled = True
            self.view.report_button.disabled = True
        self.view.update()

    def create_threads(self, quantity):
        """функция создает новые потоки"""
        for value in quantity:
            thread = threading.Thread(target=self.get_fact_issues, args=[value, self.model.working_hours.get_hours(
                year=self.view.year_dropdown.value, month=self.view.months_dropdown.value)])
            thread.start()
            thread.join()

    def get_planed_issues(self, user_id: int, need_hours: int):
        """функция ищет плановые задачи определенного пользователя"""
        user = self.model.get_user(user_id=user_id)
        issues = self.model.get_need_issues_planed(user=user_id)
        issues = self.model.get_need_values_issues(issues_list=issues, worker_id=user_id)
        user_row, table = self.view.create_row_user_and_table()
        user_row.content.data = {'table': table}
        user_row.on_click = self.user_on_click
        self.view.insert_text_to_user_row(row=user_row.content, name=f"{user.lastname} {user.firstname}",
                                          planed_hours=self.model.sum_planned_hours,
                                          fact_hours=self.model.sum_fact_hours, hours=need_hours)
        table.create_rows(issues_list=issues, worker_id=user_id, cell_click_funct=self.cell_on_click)

    def get_fact_issues(self, user_id: int, need_hours: int):
        """функция ищет фактические задачи определенного пользователя"""
        user = self.model.get_user(user_id=user_id)
        issues = self.model.get_need_issues_fact(user=user, user_id=user_id)
        issues = self.model.get_need_values_issues(issues_list=issues, worker_id=user_id)
        user_row, table = self.view.create_row_user_and_table()
        user_row.content.data = {'table': table}
        user_row.on_click = self.user_on_click
        self.view.insert_text_to_user_row(row=user_row.content, name=f"{user.lastname} {user.firstname}",
                                          planed_hours=self.model.sum_planned_hours,
                                          fact_hours=self.model.sum_fact_hours, hours=need_hours)
        table.create_rows(issues_list=issues, worker_id=user_id, cell_click_funct=self.cell_on_click)

    def user_on_click(self, event):
        """функция нажатия на поле с пользователем для тображения таблицы задач"""
        table = event.control.content.data.get("table")
        if table.visible is True:
            table.visible = False
        else:
            if self.model.last_table is not None:
                self.model.last_table.visible = False
            table.visible = True
        self.model.last_table = table
        self.view.page.update()

    def create_pdf_click(self, event):
        """функция создания pdf"""
        self.model.file_name = self.model.pdf.supervizor_create_pdf(sector=self.view.sector_dropdown.value,
                                                                    state=self.model.state,
                                                                    date=f"{self.view.months_dropdown.value} {self.view.year_dropdown.value}")
        self.view.page.launch_url(self.model.file_name)
