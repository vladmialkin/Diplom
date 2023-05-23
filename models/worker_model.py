from models.model import Model
from operator import itemgetter
from pdf import PdfFormat


class WorkerModel(Model):
    def __init__(self, redmine, database, user_model):
        super().__init__()
        self.redmine = redmine
        self.database = database
        self.user_model = user_model
        self.pdf = PdfFormat(path=self.assets_path)
        self.months_list = self.date.rus_months_list
        self.years_list = self.date.years
        self.now_day = self.date.now_day
        self.now_month = self.date.now_rus_month
        self.now_year = self.date.now_year
        self.now_date = f"{self.now_day}.{self.now_month}.{self.now_year}"
        self.selected_date = None
        self.values_issues = None
        self.sum_planned_hours = 0
        self.sum_fact_hours = 0
        self.state = None
        self.file_name = None

    def get_need_issues_planed(self) -> list:
        """функция возвращает задачи для плана месяца, относящиеся к выбранной пользователем дате"""
        return self.redmine.get_plan_issues(month_plan=self.selected_date, user_id=self.user_model.user_id)

    def get_need_issues_fact(self) -> list:
        """функция возвращает задачи для отчета, относящиеся к выбранной пользователем дате"""
        planed_issues = self.get_need_issues_planed()
        issues = []
        for issue in planed_issues:
            issues.append(issue)
        self.date.converting_date(str(self.selected_date.split(" ")[0]), int(self.selected_date.split(" ")[1]))
        user_time_entries = self.user_model.time_entries
        max_string = f"{self.date.limit_date['max_day']}/{self.date.limit_date['month_number']}/{self.date.limit_date['year']}"
        min_string = f"01/{self.date.limit_date['month_number']}/{self.date.limit_date['year']}"
        limit_max_date = self.date.convert_str_to_date(string=max_string, format="%d/%m/%Y").date()
        limit_min_date = self.date.convert_str_to_date(string=min_string, format="%d/%m/%Y").date()

        for time_entries in user_time_entries:
            if limit_min_date <= time_entries.spent_on <= limit_max_date:
                new_issue = self.redmine.get_issue(issue_id=time_entries.issue.id)
                issues.append(new_issue)
        issues_id = set([issue.id for issue in issues])
        new_issues = []
        for value_id in issues_id:
            for issue in issues:
                if value_id == issue.id:
                    new_issues.append(issue)
                    break
        return sorted(new_issues, key=itemgetter("id"), reverse=True)

    def get_need_values_issues(self, issues_list):
        """функция получает нужные значения для таблицы"""
        need_list = []
        value_issues_list = []
        self.date.converting_date(str(self.selected_date.split(" ")[0]), int(self.selected_date.split(" ")[1]))
        for issue in issues_list:
            fact_hours = 0
            planned_hours = self.database.get_planned_hours(issue_id=issue.id, user_id=self.user_model.user_id,
                                                            month_plan=self.selected_date)
            fact_hours_list = self.redmine.get_fact_hours(issue_id=issue.id, user_id=self.user_model.user_id,
                                                          limit_date=self.date.limit_date)
            if hasattr(issue, 'due_date'):
                due_date = issue.due_date
            else:
                due_date = ''
            for value in fact_hours_list:
                fact_hours += float(value.hours)
            need_dict = {"issue": issue, "values": [issue.id, issue.subject, issue.tracker,
                                                    planned_hours, fact_hours, due_date,
                                                    issue.custom_fields.get(83).value,
                                                    issue.custom_fields.get(91).value,
                                                    issue.custom_fields.get(7).value]}
            value_issues_list.append(need_dict.get("values"))
            need_list.append(need_dict)
        self.values_issues = value_issues_list
        return need_list

    def create_pdf(self, state: str, sum_func):
        """функция формирует PDF"""
        planned_hours, fact_hours = sum_func()
        self.file_name = self.pdf.worker_create_html(data=self.values_issues, state=state,
                                                     sector=self.user_model.sector,
                                                     user_name=self.user_model.user_name, now_date=self.now_date,
                                                     plan_costs=planned_hours, fact_costs=fact_hours,
                                                     plan_month=self.selected_date,
                                                     month_year=f"{self.date.now_rus_month} {self.date.now_year}",
                                                     norm_costs=1)
