from controllers.contoller import Controller
from views.issue_view import IssueView
from models.issue_model import IssueModel


class IssueController(Controller):
    def __init__(self, redmine, database, user_model, issue, worker_model):
        super().__init__()
        self.view = IssueView(route="issue")
        self.model = IssueModel(redmine=redmine, database=database, user_model=user_model, issue=issue,
                                worker_model=worker_model)
        self.insert_defolt_attr_issue()
        self.insert_specific_attr_issue()

    def insert_defolt_attr_issue(self):
        """функция выводит основные данные задачи"""
        defolt_array = self.model.defolt_attributs.items()
        for attr in defolt_array:
            widget_attr = self.view.create_text_row(width=500, head_text=attr[0], text=attr[1])
            self.view.defolt_attr_issue.controls.append(widget_attr)

    def insert_specific_attr_issue(self):
        """функция выводит специфические данные задачи"""
        for attr in self.model.issue.custom_fields:
            if attr.id == 85:
                attr.value = self.model.appointed
            if attr.id == 83:
                attr.value = self.model.months
            if attr.id == 7:
                break
            widget_attr = self.view.create_text_row(width=1000, head_text=attr.name, text=attr.value)
            self.view.specific_attr_issue.controls.append(widget_attr)

        widget_attr = self.view.create_text_row(width=1000, head_text="Описание:", text=self.model.issue.description)
        self.view.specific_attr_issue.controls.append(widget_attr)

        if self.model.issue.custom_fields.get(7) is not None:
            widget_attr = self.view.create_text_row(width=1000, head_text="Результат:",
                                                    text=self.model.issue.custom_fields.get(7).value)
            self.view.specific_attr_issue.controls.append(widget_attr)

