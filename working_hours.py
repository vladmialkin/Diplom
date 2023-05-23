import json
from date import Date


class WorkingHours:
    def __init__(self):
        self.date = Date()

    def create_new_year(self, year):
        data = self.read_working_hours()
        if year in data.keys():
            return 0
        else:
            months = {}
            for index, month in enumerate(self.date.rus_months_list):
                month_dict = {month: float(0.0)}
                months.update(month_dict)
            new_year = {year: months}
            data.update(new_year)
            new_data = dict(sorted(data.items()))
            self.write_json(new_data)
            return 1

    @staticmethod
    def write_json(text: dict):
        with open('working_hours.json', 'w') as file:
            file.write(json.dumps(text, indent=2, ensure_ascii=False))

    def insert_working_hours(self, year: str, month: str, hours: int):
        data = self.read_working_hours()
        if year in data.keys():
            if month in data[year].keys():
                data[year].update({f"{month}": float(hours)})
            else:
                data[year].update({f"{month}": float(hours)})
        self.write_json(data)

    def read_working_hours(self):
        try:
            with open('working_hours.json', 'r') as file:
                return json.load(file)
        except:
            data = {}
            months = {}
            for index, month in enumerate(self.date.rus_months_list):
                month_dict = {month: float(0.0)}
                months.update(month_dict)
            new_year = {"2022": months}
            data.update(new_year)
            self.write_json(data)

    def get_hours(self, year, month):
        data = self.read_working_hours()
        if year in data.keys():
            return data[year][month]
        else:
            return None
