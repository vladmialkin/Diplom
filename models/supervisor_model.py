from models.model import Model
from operator import itemgetter
from pdf import PdfFormat
from working_hours import WorkingHours


class SupervisorModel(Model):
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
        self.sectors = self.database.get_sectors()
        self.sum_planned_hours = 0
        self.sum_fact_hours = 0
        self.state = None
        self.working_hours = WorkingHours()
        self.last_table = None
        self.workers = None
        self.worker = None
        self.file_name = None

    def get_need_issues_planed(self, user) -> list:
        """функция возвращает задачи для плана месяца, относящиеся к выбранной пользователем дате"""
        return self.redmine.get_plan_issues(month_plan=self.selected_date, user_id=user)

    def get_user(self, user_id: int):
        self.worker = self.redmine.get_user(user_id=user_id)
        return self.worker

    def get_workers_sector_list(self, sector):
        """функция возвращает список работников выбранного сектора"""
        workers = self.database.get_workers_from_sector(sector)
        workers_list = []
        for worker_id in workers:
            worker_status = self.database.check_user(*worker_id)
            if worker_status:
                if worker_status[0][0] != 3:
                    workers_list.append(*worker_id)
        return sorted(workers_list)

    def get_need_values_issues(self, issues_list, worker_id):
        """функция получает нужные значения для таблицы"""
        need_list = []
        value_issues_list = []
        self.date.converting_date(str(self.selected_date.split(" ")[0]), int(self.selected_date.split(" ")[1]))
        sum_planned_hours = 0
        sum_fact_hours = 0
        for issue in issues_list:
            fact_hours = 0
            planned_hours = self.database.get_planned_hours(issue_id=issue.id, user_id=worker_id,
                                                            month_plan=self.selected_date)
            fact_hours_list = self.redmine.get_fact_hours(issue_id=issue.id, user_id=worker_id,
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
            sum_planned_hours += planned_hours
            sum_fact_hours += fact_hours
        self.values_issues = value_issues_list
        self.sum_planned_hours = sum_planned_hours
        self.sum_fact_hours = sum_fact_hours
        return need_list

    def get_need_issues_fact(self, user, user_id) -> list:
        """функция возвращает задачи для отчета, относящиеся к выбранной пользователем дате"""
        planed_issues = self.get_need_issues_planed(user=user_id)
        issues = []
        for issue in planed_issues:
            issues.append(issue)
        self.date.converting_date(str(self.selected_date.split(" ")[0]), int(self.selected_date.split(" ")[1]))
        user_time_entries = user.time_entries
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
