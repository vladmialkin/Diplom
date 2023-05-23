import flet
from views.view import View
from data_table import DataTable


class SupervisorView(View):
    def __init__(self, route):
        super().__init__(route)
        self.horizontal_alignment = "start"
        self.vertical_alignment = "start"
        self.scroll = True
        self.supervisor_mode = flet.Container(content=flet.Text(value="Режим руководителя", size=18), width=200,
                                              alignment=flet.alignment.center)

        self.worker_mode_item = flet.PopupMenuItem(text="Режим сотрудника")
        self.supervisor_mode_item = flet.PopupMenuItem(text="Режим руководителя")
        self.admin_mode_item = flet.PopupMenuItem(text="Режим администратора")

        self.menu_mode = flet.PopupMenuButton(
            items=[self.worker_mode_item, self.supervisor_mode_item, self.admin_mode_item])

        self.author_login = flet.Container(
            width=100,
            content=flet.Text(size=18, color=flet.colors.BLUE),
            alignment=flet.alignment.center)

        self.exit_bar = flet.AppBar(actions=[self.supervisor_mode,
                                             self.menu_mode,
                                             self.author_login], leading=flet.Text())

        self.frame_buttons = flet.Row()
        self.frame_table = flet.Column()

        self.months_dropdown = flet.Dropdown(width=150)
        self.year_dropdown = flet.Dropdown(width=150)
        self.sector_dropdown = flet.Dropdown(width=400)
        self.sector_name = flet.Text(size=18)

        self.plan_button = flet.ElevatedButton(text="План", width=150, height=50)
        self.report_button = flet.ElevatedButton(text="Отчет", width=150, height=50)
        self.settings_button = flet.ElevatedButton(text="Настройки",
                                                   width=150,
                                                   height=50, disabled=True)

        self.now_issues_row = flet.Row(controls=[flet.Text(size=20, weight="bold")])
        self.now_issues_row.alignment = "center"

        self.pdf_button = flet.ElevatedButton(text="Сохранить в pdf", width=150, height=50, visible=False)

        self.frame_progress_bar = flet.Row([flet.Column([flet.Text("Загрузка", style="headlineSmall"),
                                                         flet.ProgressBar(width=400, color="amber", bgcolor="#eeeeee")],
                                                        horizontal_alignment='center',
                                                        alignment='center')],
                                           visible=False, alignment='center')
        self.append_widgets(self.frame_buttons,
                            [self.months_dropdown, self.year_dropdown, self.plan_button, self.report_button,
                             self.settings_button])

        self.append_widgets(self, [self.exit_bar, self.frame_buttons, self.sector_dropdown, self.now_issues_row,
                                   self.frame_progress_bar, self.frame_table, self.pdf_button])

        self.content_color = flet.colors.BLUE

    def create_row_user_and_table(self):
        """функция создает две строки:
            - строка с данными пользователя;
            - строка с таблицей задач."""
        row = flet.Row()
        column = flet.Column()
        row.controls.append(column)
        row_user_data = self.create_row_user()
        table_issues_data = self.create_table_issues()
        column.controls.append(row_user_data)
        column.controls.append(table_issues_data)
        self.frame_table.controls.append(row)
        return row_user_data, table_issues_data

    @staticmethod
    def create_row_user():
        """функция создает строку с данными пользователя"""
        return flet.Container(content=flet.Row(controls=[flet.Text()]))

    @staticmethod
    def create_table_issues():
        """функция создает таблицу задач"""
        table = DataTable()
        table.visible = False
        table.create_columns(heads=table.issues_heads)
        return table

    @staticmethod
    def insert_text_to_user_row(row, name, planed_hours: float, fact_hours: float, hours: float):
        """функция добавляет текст в сроку с данными работника"""
        if planed_hours >= hours:
            planned_color = flet.colors.GREEN
        else:
            planned_color = flet.colors.RED

        if fact_hours >= hours:
            fact_color = flet.colors.GREEN
        else:
            fact_color = flet.colors.RED

        row.controls = [
            flet.Text(value=name, color=flet.colors.BLUE, size=20),
            flet.Text(value=f"План.:", size=20),
            flet.Text(value=f"{planed_hours}", color=planned_color, size=20),
            flet.Text(value=f"/ {hours}", size=20),
            flet.Text(value=f"Факт.:", size=20),
            flet.Text(value=f"{fact_hours}", color=fact_color, size=20),
            flet.Text(value=f"/ {hours}", size=20),
        ]