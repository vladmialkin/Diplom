import flet
from views.view import View


class IssueView(View):
    def __init__(self, route):
        super().__init__(route=route)
        self.horizontal_alignment = "start"
        self.vertical_alignment = "start"
        self.scroll = True

        self.app_bar = flet.AppBar(title=flet.Text("Вернуться"))

        self.issue_info_frame = flet.Column()
        self.issue_edit_frame = flet.Row()

        self.frame_buttons = flet.Row()
        self.frame_issue = flet.Row()

        self.open_browser_issue_button = flet.ElevatedButton(text="Открыть в Redmine", width=180, height=50)
        self.edit_issue_button = flet.ElevatedButton(text="Редактировать", width=180, height=50)
        self.export_pdf_button = flet.ElevatedButton(text="PDF", width=180, height=50)

        self.frame_buttons.controls.append(self.open_browser_issue_button)
        self.frame_buttons.controls.append(self.edit_issue_button)
        self.frame_buttons.controls.append(self.export_pdf_button)

        self.defolt_attr_issue = flet.Column()
        self.specific_attr_issue = flet.Column()

        self.frame_issue.controls.append(self.defolt_attr_issue)
        self.frame_issue.controls.append(self.specific_attr_issue)

        self.append_widgets(self.issue_info_frame, [self.frame_buttons, self.frame_issue])

        self.issue_edit_frame = flet.Row(alignment="start")

        self.frame_edit = flet.Column(visible=False)

        self.project_row = flet.Row(controls=[flet.Text(value="Проект"), flet.Dropdown(width=500)])
        self.trecker_row = flet.Row(controls=[flet.Text(value="Трекер"), flet.Dropdown()])
        self.subject_row = flet.Row(controls=[flet.Text(value="Тема"), flet.TextField()])
        self.description_row = flet.Row(controls=[flet.Text(value="Описание"), flet.TextField()])
        self.status_row = flet.Row(controls=[flet.Text(value="Статус"), flet.Dropdown()])
        self.priority_row = flet.Row(controls=[flet.Text(value="Приоритет"), flet.Dropdown()])
        self.assigned_row = flet.Row(controls=[flet.Text(value="Назначена"), flet.Dropdown()])
        self.parent_issue = flet.Row(controls=[flet.Text(value="Родительская задача"), flet.TextField()])
        self.start_date = flet.Row(controls=[flet.Text(value="Дата начала"), flet.TextField()])
        self.due_date = flet.Row(controls=[flet.Text(value="Срок завершения"), flet.TextField()])

        self.save_button = flet.ElevatedButton(text="Сохранить", width=150, height=50)

        self.labor_costs_frame = flet.Column(controls=[flet.Text("Трудозатраты")], visible=False)

        self.date_row = flet.Row(controls=[flet.Text(value="Дата"), flet.TextField()])
        self.hours_row = flet.Row(controls=[flet.Text(value="Трудозатраты"), flet.TextField()])
        self.comment_row = flet.Row(controls=[flet.Text(value="Комментарий"), flet.TextField(width=500)])
        self.activity_row = flet.Row(controls=[flet.Text(value="Деятельность"), flet.Dropdown()])

        self.append_widgets(self.labor_costs_frame,
                            [self.date_row, self.hours_row, self.comment_row, self.activity_row])

        self.append_widgets(self.frame_edit,
                            [self.project_row, self.trecker_row, self.subject_row, self.description_row,
                             self.status_row, self.priority_row, self.assigned_row, self.parent_issue, self.start_date,
                             self.due_date, self.save_button])
        self.append_widgets(self.issue_edit_frame, [self.frame_edit, self.labor_costs_frame])

        self.append_widgets(self, [self.app_bar, self.issue_info_frame, self.issue_edit_frame])

    @staticmethod
    def create_text_row(width=None, head_text=None, text=None):
        """функция создает строку данных"""
        return flet.Row(wrap=True, width=width, vertical_alignment="start",
                        controls=[flet.Text(value=f"{head_text}", size=18, weight='bold'),
                                  flet.Text(value=text, size=18, overflow="visible")])
