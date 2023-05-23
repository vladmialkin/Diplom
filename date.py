import datetime as dt
import calendar


class Date:
    def __init__(self):
        self.rus_months_list = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
                                'Октябрь', 'Ноябрь', 'Декабрь']
        self.years = ['2020', '2021', '2022', '2023', '2024']

        self.now_date = dt.datetime.now()
        self.str_now_date = self.get_start_date_issue(self.now_date)
        self.now_day = self.now_date.day
        self.now_eng_month = self.now_date.month
        self.now_year = self.now_date.year
        self.now_rus_month = None
        self.limit_date = None

        self.get_now_rus_month()

    def get_now_rus_month(self):
        """функция находит текущий месяц"""
        for index, month in enumerate(self.rus_months_list):
            if self.now_eng_month == index + 1:
                self.now_rus_month = month

    def converting_date(self, month, year):
        """функция находит максимальное число месяца"""
        for index, value in enumerate(self.rus_months_list):
            if month == value:
                max_day = calendar.monthrange(int(year), index + 1)[1]
                month_index = index + 1
                if month_index < 10:
                    month_index = str(f"0{month_index}")
                self.limit_date = {"year": year, "month": month, "month_number": month_index, "max_day": max_day}

    @staticmethod
    def convert_str_to_date(string: str, format: str):
        """функция преобразует сроку в дату выбранного формата"""
        return dt.datetime.strptime(string, format)

    @staticmethod
    def get_start_date_issue(date: dt.datetime) -> str:
        """функция изменяет формат даты"""
        return date.strftime("%d.%m.%Y")

    @staticmethod
    def get_current_time():
        """функция выдает текущее время"""
        now_date = dt.datetime.now()
        now_date = now_date.strftime("%Y-%m-%d %H:%M:%S")
        return dt.datetime.strptime(now_date, "%Y-%m-%d %H:%M:%S")

    def get_date_for_month(self, month, year):
        """фукнция выводит числовую дату по полученному месяцу"""
        for index, value in enumerate(self.rus_months_list):
            if month == value:
                if index < 9:
                    ind = f"0{index + 1}"
                else:
                    ind = index + 1
                return f"{year}-{ind}-{self.now_day}"