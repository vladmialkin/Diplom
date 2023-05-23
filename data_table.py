import flet
import redminelib.resources


class DataTable(flet.DataTable):
    def __init__(self):
        super().__init__()
        self.column_count = 0
        self.horizontal_margin = 5.0
        self.show_bottom_border = True
        self.border = flet.border.all(1, color=flet.colors.BLACK)
        self.border_radius = 10
        self.vertical_lines = flet.border.BorderSide(0.5, "black")
        self.horizontal_lines = flet.border.BorderSide(0.5, "black")
        self.issues_heads = ['Номер', 'Тема', 'Трекер', 'План. труд-ты', 'Факт. труд-ты', 'Срок завершения',
                             'План месяца',
                             'Тип задачи', 'Результат задачи']
        self.laborcosts_heads = [
            'Часы',
            'План месяца',
            'Дата завершения'
        ]

    def create_columns(self, heads):
        """функция создания столбцов таблицы"""
        self.columns = []
        self.column_count = 0
        for value in heads:
            column = flet.DataColumn(flet.Text(value))
            self.columns.append(column)
            self.column_count += 1

    def create_rows(self, issues_list, worker_id, cell_click_funct):
        """функция создания строк столбцов"""
        self.rows = []
        for issue in issues_list:
            row = flet.DataRow()
            data_issue = issue.get("values")
            if isinstance(data_issue, list):
                row.cells = self.create_cells(data=data_issue, issue=issue.get("issue"), worker_id=worker_id,
                                              cell_on_click=cell_click_funct)
            self.rows.append(row)

    def create_cells(self, data: list, issue, worker_id: int, cell_on_click):
        """функция создания ячеек строки таблицы"""
        cells = []
        for index in range(self.column_count):
            cell_value = data[index]
            text_color = flet.colors.BLACK

            cell = flet.DataCell(content=flet.Text())
            cell.data = {"issue": issue,
                         "worker_id": worker_id,
                         "column_count": int(index)}

            if index == 0 or index == 1 or index == 3 or index == 4:
                cell.on_tap = cell_on_click
                text_color = flet.colors.BLUE

            if index == 6:
                months = ""
                for month in cell_value:
                    months += f" {month}"
                cell_value = months

            if index == 8:
                cell.on_tap = cell_on_click
                text_color = flet.colors.BLUE
                if cell_value == "":
                    cell_value = "Нет"

            if len(str(cell_value)) >= 60:
                cell_value = f'{cell_value[:30]}...'

            cell.content.value = cell_value
            cell.content.color = text_color
            cells.append(cell)
        return cells

    def get_sum_hours(self):
        """функция получает сумму плановых и сумму фактических трудозатрат задач пользователя"""
        sum_planned_hours = 0
        sum_fact_hours = 0
        for row in self.rows:
            for index, cell in enumerate(row.cells):
                if index == 3:
                    sum_planned_hours += float(cell.content.value)
                if index == 4:
                    sum_fact_hours += float(cell.content.value)
        return sum_planned_hours, sum_fact_hours

    def create_rows_for_planned_hours(self, data, cell_click_funct):
        """функция создает строку с ячейками данных таблицы"""
        self.rows = []
        for value in data:
            row = flet.DataRow()
            row.cells = self.create_cells_for_hours(data=value, cell_on_click=cell_click_funct)
            self.rows.append(row)

    def create_rows_for_fact_hours(self, data, selected_date, cell_click_funct):
        """функция создает строку с ячейками данных таблицы"""
        self.rows = []
        for labor_cost in data:
            row = flet.DataRow()
            args = [labor_cost.hours, selected_date, labor_cost.spent_on, labor_cost.id]
            row.cells = self.create_cells_for_hours(data=args, cell_on_click=cell_click_funct)
            self.rows.append(row)

    def create_cells_for_hours(self, data, cell_on_click):
        """функция создает ячейки с данными таблицы"""
        cells = []
        for value in data[:-1]:
            cell = flet.DataCell(content=flet.Text())
            cell.on_tap = cell_on_click
            cell.content.value = value
            cell.content.color = flet.colors.BLACK
            cell.data = data
            cells.append(cell)
        return cells
