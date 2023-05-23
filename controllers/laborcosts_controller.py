from controllers.contoller import Controller
from views.laborcosts_view import LaborcostsView
from models.laborcosts_model import LaborcostsModel
from windows import DeletePlannedHoursDialog


class LaborcostsController(Controller):
    def __init__(self, redmine, database, user_model, issue, worker_model, flag, user):
        super().__init__()
        self.view = LaborcostsView(route="labor_costs")
        self.model = LaborcostsModel(redmine=redmine, database=database, user_model=user_model, issue=issue,
                                     worker_model=worker_model)
        self.flag = flag
        self.user = user

        self.need_time_entries_values = None
        self.view.new_button.on_click = self.create_btn_on_click
        self.view.update_button.on_click = self.update_btn_on_click
        self.view.delete_button.on_click = self.delete_btn_on_click
        self.view.months_drop_box.on_change = self.month_drop_box_on_change
        self.view.years_drop_box.on_change = self.year_drop_box_on_change

        self.insert_month_box()
        self.insert_year_box()
        self.create_labor_costs()

    def insert_month_box(self):
        """функция заполняет выпадающий список месяцев"""
        self.view.insert_months_drop_box(months=self.model.date.rus_months_list)

    def insert_year_box(self):
        """функция заполняет выпадающий список года"""
        self.view.insert_years_drop_box(years=self.model.date.years)

    def create_labor_costs(self):
        """функция создает плановые или фактические трудозатраты"""
        if self.flag == 0:
            self.create_planned_labor_costs()
            text = "Плановые трудозатраты"
        else:
            self.create_fact_labor_costs()
            text = "Фактические трудозатраты"
        issue = self.model.issue
        self.view.insert_title(tracker=issue.tracker, ids=issue.id, subject=issue.subject, labor_costs=text)

    def create_planned_labor_costs(self):
        """функция создания таблицы плоновых трудозатрат"""
        data = self.model.get_planed_labor_costs(worker_id=self.user)
        text = f"Плановые традозатраты #{self.model.issue.id} {self.model.issue}"
        self.view.info_frame.controls[0].value = text
        self.view.table.create_columns(heads=self.view.table.laborcosts_heads)
        self.view.table.create_rows_for_planned_hours(data=data, cell_click_funct=self.cell_on_click)

    def create_fact_labor_costs(self):
        """функция создания таблицы плоновых трудозатрат"""
        data = self.model.get_fact_labor_costs(worker_id=self.user)
        text = f"Фактические традозатраты #{self.model.issue.id} {self.model.issue}"
        self.view.info_frame.controls[0].value = text
        self.view.table.create_columns(heads=self.view.table.laborcosts_heads)
        self.view.table.create_rows_for_fact_hours(data=data, selected_date=self.model.worker_model.selected_date,
                                                   cell_click_funct=self.cell_on_click)

    def cell_on_click(self, event):
        """функция нажатия на ячейку таблицы"""
        values = event.control.data
        self.view.hours_entry.value = values[0]
        self.view.hours_entry.data = values
        self.view.spent_on_entry.value = values[2]
        self.view.spent_on_entry.data = values
        self.view.months_drop_box.value = values[1].split(" ")[0]
        self.view.months_drop_box.data = values
        self.view.years_drop_box.value = values[1].split(" ")[1]
        self.view.years_drop_box.data = values
        self.need_time_entries_values = values
        self.view.update()

    def create_btn_on_click(self, event):
        """функция нажатия на кнопку создания новых трудозатрат"""
        if self.flag == 0:
            self.model.create_planed_labor_cost(worker_id=self.user,
                                                month_plan=f'{self.view.months_drop_box.value} {self.view.years_drop_box.value}',
                                                hours=self.view.hours_entry.value,
                                                spent_on=self.view.spent_on_entry.value)
        else:
            self.model.create_fact_labor_cost(worker_id=self.user,
                                              hours=self.view.hours_entry.value,
                                              spent_on=self.view.spent_on_entry.value)
        self.upload_btn_on_click()

    def update_btn_on_click(self, event):
        if self.need_time_entries_values is None:
            return
        if self.flag == 0:
            self.model.update_planed_labor_cost(id_labor_cost=self.need_time_entries_values[3],
                                                hours=self.view.hours_entry.value,
                                                spent_on=self.view.spent_on_entry.value,
                                                month_plan=f'{self.view.months_drop_box.value} {self.view.years_drop_box.value}')
        else:
            self.model.update_fact_labor_cost(id_labor_cost=self.need_time_entries_values[3],
                                              hours=self.view.hours_entry.value,
                                              spent_on=self.view.spent_on_entry.value)
        self.upload_btn_on_click()

    def delete_btn_on_click(self, event):
        if self.need_time_entries_values is None:
            return
        if self.flag == 0:
            if len(self.view.table.rows) == 1:
                self.view.page.dialog = DeletePlannedHoursDialog()
                self.view.page.update()
                self.view.page.dialog.show_dialog(database=self.model.database, issue_id=self.model.issue.id,
                                                  month=self.model.worker_model.selected_date)
            self.model.delete_planed_labor_cost(self.need_time_entries_values[3])
        else:
            self.model.delete_fact_labor_cost(self.need_time_entries_values[3])
        self.upload_btn_on_click()

    def upload_btn_on_click(self):
        if self.flag == 0:
            self.create_planned_labor_costs()
        else:
            self.create_fact_labor_costs()
        self.view.update()

    def update_spent_on(self, month, year):
        """Функция обновляет дату"""
        date = self.model.date.get_date_for_month(month=month, year=year)
        self.view.spent_on_entry.value = date

    def month_drop_box_on_change(self, event):
        """функция добавления текущего года в выпадающий список годов трудозатрат"""
        if self.view.years_drop_box.value is None:
            year = self.model.date.now_date.year
            self.view.years_drop_box.value = year
        self.update_spent_on(month=self.view.months_drop_box.value, year=self.view.years_drop_box.value)
        self.view.update()

    def year_drop_box_on_change(self, event):
        """функция добавления текущего месяца в выпадающий список месяцев трудозатрат"""
        if self.view.months_drop_box.value is None:
            month = self.model.date.rus_months_list[self.model.date.now_eng_month - 1]
            self.view.months_drop_box.value = month
        self.update_spent_on(month=self.view.months_drop_box.value, year=self.view.years_drop_box.value)
        self.view.update()
