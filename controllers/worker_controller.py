from controllers.contoller import Controller
from views.worker_view import WorkerView
from models.worker_model import WorkerModel
from windows import ExitMenuDialog, ResultIssueDialog
from controllers.issue_controller import IssueController
from controllers.laborcosts_controller import LaborcostsController


class WorkerController(Controller):
    def __init__(self, redmine, database, user_model):
        super().__init__()
        self.view = WorkerView(route="worker")
        self.model = WorkerModel(redmine=redmine, database=database, user_model=user_model)

        self.view.supervisor_mode_item.on_click = self.supervisor_mode_click
        self.view.admin_mode_item.on_click = self.admin_mode_click

        self.view.plan_button.on_click = self.plan_btn_click
        self.view.report_button.on_click = self.report_btn_click
        self.view.pdf_button.on_click = self.create_pdf_click

        self.insert_date()

        self.view.author_login.content.value = self.model.user_model.user_login
        self.view.author_login.on_click = self.check_exit

    def supervisor_mode_click(self, event):
        """функция нажатия на кнопку перехода на страницу руководителя при наличии прав"""
        if self.model.user_model.supervisor_rights is True:
            self.mode_click("supervisor")

    def admin_mode_click(self, event):
        """функция нажатия на кнопку перехода на страницу администратора при наличии прав"""
        if self.model.user_model.supervisor_rights is True:
            self.mode_click("admin")

    def plan_btn_click(self, event):
        """функция нажатия на кнопку создания плана задач"""
        self.update_disabled_buttons()
        self.model.state = 0
        self.model.selected_date = f"{self.view.months_dropdown.value} {self.view.year_dropdown.value}"
        issues = self.model.get_need_issues_planed()
        issues = self.model.get_need_values_issues(issues)
        self.view.data_table.create_rows(issues_list=issues, worker_id=self.model.user_model.user_id,
                                         cell_click_funct=self.cell_on_click)
        self.update_disabled_buttons()

    def report_btn_click(self, event):
        """функция нажатия на кнопку создания отчета задач"""
        self.update_disabled_buttons()
        self.model.state = 1
        self.model.selected_date = f"{self.view.months_dropdown.value} {self.view.year_dropdown.value}"
        issues = self.model.get_need_issues_fact()
        issues = self.model.get_need_values_issues(issues)
        self.view.data_table.create_rows(issues_list=issues, worker_id=self.model.user_model.user_id,
                                         cell_click_funct=self.cell_on_click)
        self.update_disabled_buttons()

    def create_pdf_click(self, event):
        """функция нажатия на кнопку создания pdf"""
        if self.model.state == 0:
            state = "План"
        else:
            state = "Отчет"
        self.model.create_pdf(state=state, sum_func=self.view.data_table.get_sum_hours)
        self.view.page.launch_url(f"/assets/{self.model.file_name}", web_window_name='server')

    def check_exit(self, event):
        """функция нажатия на кнопку выхода для подтверждения выхода"""
        self.view.page.dialog = ExitMenuDialog()
        self.view.page.update()
        self.view.page.dialog.show_dialog()

    def insert_date(self):
        """функция добавляет список месяцев и годов в выпадающие списки"""
        self.view.insert_values_to_dropdown(self.model.months_list, self.model.now_month,
                                            self.view.months_dropdown)
        self.view.insert_values_to_dropdown(self.model.years_list, self.model.now_year, self.view.year_dropdown)

    def update_disabled_buttons(self):
        """функция изменят видимость кнопок"""
        if self.view.plan_button.disabled is True:
            self.view.data_table.visible = True
            self.view.plan_button.disabled = False
            self.view.report_button.disabled = False
            self.view.frame_progress_bar.visible = False
            self.view.pdf_button.visible = True
        else:
            self.view.data_table.visible = False
            self.view.pdf_button.visible = False
            self.view.frame_progress_bar.visible = True
            self.view.plan_button.disabled = True
            self.view.report_button.disabled = True
        self.view.update()

    def mode_click(self, route):
        """функция переходин на выбранную страницу"""
        views = self.view.page.views
        for view in views:
            if view.route == route:
                self.view.page.views.remove(view)
                self.view.page.views.append(view)
                self.view.page.go(view.route)
        self.view.page.update()

    def cell_on_click(self, event):
        """функция нажатия на ячейку таблицы"""
        column_count = event.control.data.get("column_count")
        issue = event.control.data.get("issue")
        if column_count == 0 or column_count == 1:
            """переход к странице информации о задаче"""
            self.issue_info_click(issue=issue)
        elif column_count == 3:
            """переход к странице плановых трудозатрат"""
            self.planned_labor_costs_click(issue=issue)
        elif column_count == 4:
            """переход к странице фактических трудозатрат"""
            self.fact_labor_costs_click(issue=issue)
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

    def planned_labor_costs_click(self, issue):
        """функция нажатия на кнопку перехода на страницу плановых трудозатрат задачи"""
        laborcosts_controller = LaborcostsController(redmine=self.model.redmine, database=self.model.database,
                                                     user_model=self.model.user_model,
                                                     issue=issue, worker_model=self.model, flag=0,
                                                     user=self.model.user_model.user_id)
        self.view.page.views.append(laborcosts_controller.view)
        self.view.page.go(laborcosts_controller.view.route)

    def fact_labor_costs_click(self, issue):
        """функция нажатия на кнопку перехода на страницу фактических трудозатрат задачи"""
        laborcosts_controller = LaborcostsController(redmine=self.model.redmine, database=self.model.database,
                                                     user_model=self.model.user_model,
                                                     issue=issue, worker_model=self.model, flag=1,
                                                     user=self.model.user_model.user_id)
        self.view.page.views.append(laborcosts_controller.view)
        self.view.page.go(laborcosts_controller.view.route)

    def result_click(self, issue):
        """функция нажатия на ячейку результата для вывода окна редактирования результата задачи"""
        self.view.page.dialog = ResultIssueDialog()
        self.view.page.update()
        self.view.page.dialog.show_dialog(issue=issue, database=self.model.database)