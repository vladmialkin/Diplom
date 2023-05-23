import flet
from views.view import View


class AdminView(View):
    def __init__(self, route):
        super().__init__(route)
        self.horizontal_alignment = "start"
        self.vertical_alignment = "start"

        self.admin_mode = flet.Container(content=flet.Text(value="Режим администратора", size=18), width=200,
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

        self.exit_bar = flet.AppBar(actions=[self.admin_mode,
                                             self.menu_mode,
                                             self.author_login], leading=flet.Text())

        self.insert_button = flet.TextButton(text="Добавить год", visible=False)

        self.tabs = flet.Tabs()

        self.db_tab = flet.Tab(text="База данных")

        self.db_frame = flet.Column()
        self.db_row = flet.Row()
        self.db_text = flet.Text(value="Сервер базы данных", size=18)
        self.dropdown_db = flet.Dropdown(width=150)

        self.db_tab.content = self.db_frame
        self.append_widgets(self.db_frame, [self.db_row])
        self.append_widgets(self.db_row, [self.db_text, self.dropdown_db])

        self.working_hours_tab = flet.Tab(text="Трудовые часы")

        self.working_hours_column = flet.Column()

        self.table = flet.Column()

        self.column = flet.Column()

        self.working_hours_button_row = flet.Row()
        self.update_working_hours_button = flet.TextButton(width=150, text="Изменить часы")
        self.insert_new_year_button = flet.TextButton(width=150, text="Добавить год")

        self.append_widgets(self.working_hours_button_row,
                            [self.update_working_hours_button, self.insert_new_year_button])

        self.update_working_hours_row = flet.Row(visible=False)
        self.year_dropdown = flet.Dropdown()
        self.month_dropdown = flet.Dropdown()
        self.hours_input = flet.TextField(width=100)
        self.button_save = flet.TextButton(width=100, text="Сохранить")
        self.button_cansel = flet.TextButton(width=100, text="Отмена")
        self.append_widgets(self.update_working_hours_row,
                            [self.year_dropdown, self.month_dropdown, self.hours_input, self.button_save,
                             self.button_cansel])

        self.new_year_row = flet.Row(controls=[flet.Text(value="Введите год")], visible=False)
        self.year_input = flet.TextField(width=150)
        self.button_year_save = flet.TextButton(width=100, text="Добавить")
        self.button_year_cansel = flet.TextButton(width=100, text="Отмена")
        self.append_widgets(self.new_year_row,
                            [self.year_input, self.button_year_save, self.button_year_cansel])

        self.append_widgets(self.column,
                            [self.working_hours_button_row, self.update_working_hours_row, self.new_year_row,
                             self.table])

        self.working_hours_tab.content = self.column
        self.tabs.tabs = [self.db_tab, self.working_hours_tab]
        self.append_widgets(self, [self.exit_bar, self.tabs, self.insert_button])

    @staticmethod
    def append_widgets(widget, widgets: list):
        """функция добавляет виджеты в один"""
        if isinstance(widgets, list):
            for value in widgets:
                widget.controls.append(value)

    def insert_months_drop_box(self, data):
        """фукнция добавления данных в выпадающий список"""
        for value in data:
            self.dropdown_db.options.append(flet.dropdown.Option(value))

    @staticmethod
    def insert_to_dropdown(dropdown, values):
        for value in values:
            dropdown.options.append(flet.dropdown.Option(value))

    @staticmethod
    def create_table_row(year, values):
        row = flet.Row()
        cell = flet.Row(controls=[flet.Text(value=year)], width=100, alignment="center")
        row.controls.append(cell)
        for value in values:
            cell = flet.Row(controls=[flet.Text(value=value)], width=100, alignment="center")
            row.controls.append(cell)
        return row

    @staticmethod
    def create_table_headlines(values):
        row = flet.Row()
        for value in values:
            cell = flet.Row(controls=[flet.Text(value=value)], width=100, alignment="center")
            row.controls.append(cell)
        return row

    def create_working_hours_table(self, headlines, values):
        headlines_columns = self.create_table_headlines(values=headlines)
        self.table.controls.append(headlines_columns)
        for value in values:
            row = self.create_table_row(year=value, values=values[value].values())
            self.table.controls.append(row)
