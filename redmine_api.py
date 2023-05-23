import redminelib as rdm


class RedmineApi:
    """класс взаимодействия с API"""

    def __init__(self):
        self.__site = 'http://172.17.0.3:3000/'
        self.redmine = None

    def connecting(self, __login: str, __password: str):
        """подключение к Redmine"""
        self.redmine = rdm.Redmine(self.__site, username=__login, password=__password)

    def get_plan_issues(self, month_plan, user_id):
        """функция возвращает объект задач по плану за месяц назначенному пользователю"""
        return self.redmine.issue.filter(cf_85=f"{user_id}", cf_83=f"{month_plan}", cf_91="Плановая", status_id='*')

    def get_fact_hours(self, issue_id: int, user_id: int, limit_date):
        """функция находит фактические трудозатраты задачи по ее id"""
        spent_on = f'><{limit_date["year"]}-{limit_date["month_number"]}-01|{limit_date["year"]}-{limit_date["month_number"]}-{limit_date["max_day"]}'
        return self.redmine.time_entry.filter(issue_id=issue_id, user_id=user_id, spent_on=spent_on)

    def get_issue(self, issue_id: int):
        """функция возвращает объект задач"""
        return self.redmine.issue.get(issue_id)

    def create_time_entry(self, user_id: int, issue_id: int, hours: float, spent_on):
        """функция создает новые фактические трудозатраты от пользователя под id"""
        self.redmine.time_entry.create(user_id=user_id, issue_id=issue_id, hours=hours, spent_on=spent_on)

    def update_time_entry(self, resource_id: int, hours: float, spent_on):
        """функция изменяет фактические трудозатраты"""
        self.redmine.time_entry.update(resource_id=resource_id, hours=hours, spent_on=spent_on)

    def delete_time_entry(self, id_labor_cost: int):
        """функция удаляет фактические трудозатраты"""
        self.redmine.time_entry.delete(resource_id=id_labor_cost)

    def get_user(self, user_id: int):
        """функция возвращает пользователя по id"""
        return self.redmine.user.get(resource_id=user_id)

    def get_user_name(self, user_id: int):
        """функция назодит данные пользователя по id"""
        user = self.redmine.user.get(resource_id=user_id)
        name = f"{user.lastname} {user.firstname}"
        return name
