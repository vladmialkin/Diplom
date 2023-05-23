import flet
from views.view import View
from data_table import DataTable


class LaborcostsView(View):
    def __init__(self, route):
        super().__init__(route=route)
        self.horizontal_alignment = "center"
        self.vertical_alignment = "center"
        self.scroll = True

        self.app_bar = flet.AppBar(title=flet.Text("Вернуться"))

        self.info_column = flet.Column()
        self.info_frame = flet.Row(alignment='start', controls=[self.info_column])

        self.table = DataTable()
        self.table.height = 500
        self.entry_frame = flet.Row(alignment="center")
        self.buttons_frame = flet.Row(alignment="center")

        self.hours_entry = flet.TextField(label="Часы", width=150, keyboard_type="number")
        self.months_drop_box = flet.Dropdown(label="Месяц", width=150)
        self.years_drop_box = flet.Dropdown(label="Год", width=150)
        self.spent_on_entry = flet.TextField(label="Дата", width=150, keyboard_type="datetime")

        self.new_button = flet.ElevatedButton(text="Добавить часы", width=150, height=50)
        self.update_button = flet.ElevatedButton(text="Редактировать", width=150, height=50)
        self.delete_button = flet.ElevatedButton(text="Удалить", width=150, height=50)

        self.color = flet.colors.BLUE_50

        self.table.create_columns(heads=self.table.laborcosts_heads)

        self.append_widgets(self.buttons_frame,
                            [self.new_button, self.update_button, self.delete_button])

        self.append_widgets(self.entry_frame,
                            [self.hours_entry, self.months_drop_box, self.years_drop_box, self.spent_on_entry])

        self.append_widgets(self,
                            [self.app_bar, self.info_frame,
                             self.table, self.entry_frame, self.buttons_frame])

    @staticmethod
    def create_container(value, width=150, height=50):
        """функция создает контейнер с текстом"""
        return flet.Container(content=flet.Text(value=value, size=18, weight="bold"), alignment=flet.alignment.center,
                              width=width, height=height)

    def insert_months_drop_box(self, months):
        """функция добавления данных в выпадающий список"""
        for index, month in enumerate(months):
            self.months_drop_box.options.append(flet.dropdown.Option(month))

    def insert_years_drop_box(self, years):
        for index, year in enumerate(years):
            self.years_drop_box.options.append(flet.dropdown.Option(year))

    def insert_title(self, tracker, ids, subject, labor_costs):
        """функция добавляет заголовок с задачей"""
        self.info_column.controls = [flet.Text(f"{tracker} #{ids}", size=24, weight='bold'),
                                     flet.Text(f"{subject}", size=20, weight='bold'),
                                     flet.Text(f"{labor_costs}", size=20)]