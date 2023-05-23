import flet
from views.view import View
from data_table import DataTable


class WorkerView(View):
    def __init__(self, route):
        super().__init__(route)
        self.horizontal_alignment = "start"
        self.vertical_alignment = "start"
        self.worker_mode = flet.Container(content=flet.Text(value="Режим сотрудника", size=18), width=200,
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

        self.exit_bar = flet.AppBar(actions=[self.worker_mode,
                                             self.menu_mode,
                                             self.author_login], leading=flet.Text())

        self.frame_buttons = flet.Row()
        self.frame_sectors = flet.Column()
        self.frame_table = flet.Column()

        self.months_dropdown = flet.Dropdown(width=150)
        self.year_dropdown = flet.Dropdown(width=150)

        self.sector_name = flet.Text(size=18)

        self.plan_button = flet.ElevatedButton(text="План", width=150, height=50)
        self.report_button = flet.ElevatedButton(text="Отчет", width=150, height=50)
        self.settings_button = flet.ElevatedButton(text="Настройки",
                                                   width=150,
                                                   height=50, disabled=True)

        self.pdf_button = flet.ElevatedButton(text="Сохранить в pdf", width=150, height=50, visible=False)
        self.data_table = DataTable()
        self.data_table.visible = False

        self.frame_progress_bar = flet.Row(
            [flet.Column(
                [flet.Text("Загрузка", style="headlineSmall"),
                 flet.ProgressBar(width=400, color="amber", bgcolor="#eeeeee")],
                horizontal_alignment="center",
                alignment="center")],
            visible=False,
            alignment="center")

        self.append_widgets(self.frame_buttons,
                            [self.months_dropdown, self.year_dropdown, self.plan_button, self.report_button,
                             self.settings_button])
        self.append_widgets(self.frame_sectors, [self.sector_name])
        self.append_widgets(self.frame_table, [self.data_table, self.pdf_button])

        self.append_widgets(self, [self.exit_bar, self.frame_buttons, self.frame_sectors,
                                   self.frame_progress_bar,
                                   self.frame_table])

        self.content_color = flet.colors.BLUE

        self.data_table.create_columns(heads=self.data_table.issues_heads)