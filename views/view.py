import flet


class View(flet.View):
    def __init__(self, route):
        super().__init__()
        self.route = route

    @staticmethod
    def append_widgets(widget, widgets: list):
        """функция добавляет виджеты в один"""
        if isinstance(widgets, list):
            for value in widgets:
                widget.controls.append(value)

    @staticmethod
    def insert_values_to_dropdown(values, need_value, dropdown):
        """фукнция добавления данных в выпадающий список"""
        for value in values:
            dropdown.options.append(flet.dropdown.Option(value))
            if value == str(need_value):
                dropdown.value = value
