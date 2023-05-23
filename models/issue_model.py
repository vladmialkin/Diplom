from models.model import Model


class IssueModel(Model):
    def __init__(self, redmine, database, user_model, issue, worker_model):
        super().__init__()
        self.redmine = redmine
        self.database = database
        self.user_model = user_model
        self.issue = issue
        self.worker_model = worker_model
        self.start_date = None
        self.due_date = None
        self.planned_hours = None
        self.fact_hours = None
        self.appointed = None
        self.months = None

        self.defolt_attributs = {'Проект: ': self.issue.project,
                                 'Тема задачи: ': self.issue.subject,
                                 'Трекер задачи: ': self.issue.tracker,
                                 'Статус задачи: ': self.issue.status,
                                 'Назначена: ': self.issue.assigned_to,
                                 "Дата начала: ": self.start_date,
                                 "Срок завершения: ": self.due_date,
                                 "Приоритет: ": self.issue.priority,
                                 "Владелец задачи: ": self.issue.author,
                                 "Плановые трудозатраты: ": self.planned_hours,
                                 "Фактические трудозатраты: ": self.fact_hours,
                                 }

        self.get_dates()
        self.get_hours()
        self.get_appointed()
        self.get_months()

    def get_hours(self):
        """функция находит трудозатраты задачи"""
        self.planned_hours = self.get_planned_hours()
        self.fact_hours = self.get_fact_hours()

    def get_dates(self):
        """функция находит даты начала и конца задачи"""
        self.start_date = self.get_date(self.issue, 'start_date', self.date.get_start_date_issue)
        self.due_date = self.get_date(self.issue, 'due_date', self.date.get_start_date_issue)

    def get_planned_hours(self):
        """функция получает плановые часы задачи"""
        return self.database.get_sum_estimated_hours(self.issue.id, self.user_model.user_id)

    def get_fact_hours(self):
        """функция получает фактические часы задачи"""
        fact_hours = 0
        self.date.converting_date(str(self.worker_model.selected_date.split(" ")[0]),
                                  int(self.worker_model.selected_date.split(" ")[1]))
        fact_hours_list = self.redmine.get_fact_hours(issue_id=self.issue.id, user_id=self.user_model.user_id,
                                                      limit_date=self.date.limit_date)
        for value in fact_hours_list:
            fact_hours += float(value.hours)
        return fact_hours

    @staticmethod
    def check_attr(obj: object, attr: str) -> bool:
        """функция проверят существование атрибута"""
        return hasattr(obj, attr)

    @staticmethod
    def get_attr(obj: object, attr: str):
        """функция получает значение атрибута объекта"""
        return getattr(obj, attr)

    def get_date(self, obj: object, attr: str, func):
        """функция проверяет существование атрибута и выводит результат даты"""
        if self.check_attr(obj, attr):
            value = self.get_attr(obj, attr)
            return func(value)
        else:
            value = ""
            return value

    def get_appointed(self):
        """функция находит пользователя, которому назначена задача"""
        value = self.issue.custom_fields.get(85).value
        if value is None:
            self.appointed = ''
        else:
            self.appointed = self.redmine.get_user_name(value)

    def get_months(self):
        """функция получает строку месяцев"""
        months = self.issue.custom_fields.get(83)
        string = str(months.value[0])
        if len(months.value) > 1:
            for month in months.value[1:]:
                string += f" {month}"
        self.months = string
