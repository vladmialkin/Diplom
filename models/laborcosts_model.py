from models.model import Model


class LaborcostsModel(Model):
    def __init__(self, redmine, database, user_model, issue, worker_model):
        super().__init__()
        self.redmine = redmine
        self.database = database
        self.user_model = user_model
        self.issue = issue
        self.worker_model = worker_model
        self.date.converting_date(year=self.worker_model.selected_date.split(" ")[1],
                                  month=self.worker_model.selected_date.split(" ")[0])

    def get_planed_labor_costs(self, worker_id):
        """функция получает плановые трудозатраты"""
        return self.database.get_editing_tree(user_id=worker_id, issue_id=self.issue.id,
                                              plan_month=self.worker_model.selected_date)

    def get_fact_labor_costs(self, worker_id):
        """функция получает плановые трудозатраты"""
        return self.redmine.get_fact_hours(issue_id=self.issue.id, user_id=worker_id,
                                           limit_date=self.date.limit_date)

    def create_planed_labor_cost(self, worker_id: int, month_plan: str, hours: float, spent_on):
        """функция создания новых плановых трудозатрат"""
        updated_on = self.date.get_current_time()
        self.database.insert_planed_labor_cost(user_id=worker_id, issue_id=self.issue.id, hours=hours,
                                               month_plan=month_plan,
                                               planned_on=spent_on, updated_on=updated_on)

    def create_fact_labor_cost(self, worker_id: int, hours: float, spent_on):
        """функция создания новых фактических трудозатрат"""
        self.redmine.create_time_entry(user_id=worker_id, issue_id=self.issue.id, hours=hours, spent_on=spent_on)

    def update_planed_labor_cost(self, id_labor_cost, hours, spent_on, month_plan):
        """функция изменения плановых трудозатрат"""
        custom_fields = self.issue.custom_fields.get(83).value
        if month_plan not in custom_fields:
            """если выбранного месяца нет в настраиваемых полях, то месяц добавляется"""
            self.database.update_month_in_custom_fields(issue_id=self.issue.id, month_plan=month_plan)
        self.database.update_planed_labor_cost(id_labor_cost=id_labor_cost, hours=hours, spent_on=spent_on,
                                               month_plan=month_plan)

    def update_fact_labor_cost(self, id_labor_cost: int, hours: float, spent_on):
        """функция изменения фактических трудозатрат"""
        self.redmine.update_time_entry(resource_id=id_labor_cost, hours=hours, spent_on=spent_on)

    def delete_planed_labor_cost(self, id_labor_cost: int):
        """функция удаления плановых трудозатрат"""
        self.database.delete_planed_labor_cost(id_labor_cost=id_labor_cost)

    def delete_fact_labor_cost(self, id_labor_cost: int):
        """функция удаления фактических трудозатрат"""
        self.redmine.delete_time_entry(id_labor_cost=id_labor_cost)
