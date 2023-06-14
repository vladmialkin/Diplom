import mysql.connector


class DataBase:
    """класс взаимодействия с базой данных"""

    def __init__(self):
        self.database = None
        self.cursor = None
        self.db_host = '192.168.122.163'
        self.db_list = ['192.168.122.163']

    def connecting(self):
        """функция подключения к базе данных"""
        self.database = mysql.connector.connect(
            user='root',
            password='example',
            host=self.db_host,
            database='redmine',
            port='5217'
        )
        self.cursor = self.database.cursor()

    def get_sector(self, user_id: int):
        """функция находит сектор по id работника"""
        self.cursor.execute(f"SELECT value FROM custom_values WHERE custom_field_id=11 AND customized_id={user_id}")
        return self.cursor.fetchone()[0]

    def get_supervizor_rights(self, user_id: int):
        """функция проверяет работника на наличие прав руководителя по его id"""
        self.cursor.execute(f"SELECT name FROM `departments` WHERE head_id={user_id}")
        if self.cursor.fetchone() is None:
            return None
        else:
            return self.cursor.fetchone()[0]

    def get_planned_hours(self, issue_id: int, user_id: int, month_plan: str) -> float:
        """функция находит плановые трудозатраты задачи по ее id"""
        self.cursor.execute(f"SELECT month_hours FROM `planned_labor_costs` "
                            f"WHERE issue_id = {int(issue_id)} and user_id = {int(user_id)} and "
                            f"month_plan = '{month_plan}'")
        value = self.cursor.fetchall()
        if not value:
            value = 0
            return float(value)
        else:
            sum = 0
            for val in value:
                sum += val[0]
            return sum

    def get_sum_estimated_hours(self, issue_id, user_id):
        """функция возвращает сумму плановых трудозатрат"""
        self.cursor.execute(f"SELECT SUM(month_hours) FROM `planned_labor_costs` "
                            f"WHERE issue_id = {int(issue_id)} and user_id = {int(user_id)}")
        value = self.cursor.fetchone()
        if value[0] is None:
            value = 0
            return value
        else:
            return value[0]

    def get_editing_tree(self, user_id, issue_id, plan_month):
        """функция получает плановые трудозатраты"""
        self.cursor.execute(f"SELECT month_hours, month_plan, planned_on, id FROM planned_labor_costs "
                            f"WHERE "
                            f"user_id = {user_id} "
                            f"AND "
                            f"issue_id = {issue_id} "
                            f"AND "
                            f"month_plan = '{plan_month}'")
        return self.cursor.fetchall()

    def insert_planed_labor_cost(self, user_id, issue_id, hours, month_plan, planned_on, updated_on):
        """функция создает новые плановые трудозатраты"""
        self.cursor.execute(f"INSERT INTO `planned_labor_costs` "
                            f"SET "
                            f"user_id={user_id},"
                            f"issue_id={issue_id},"
                            f"month_plan='{month_plan}',"
                            f"month_hours={hours},"
                            f"planned_on='{planned_on}',"
                            f"created_on='{updated_on}',"
                            f"updated_on='{updated_on}'")
        self.database.commit()

    def update_planed_labor_cost(self, id_labor_cost, hours, spent_on, month_plan, updated_on):
        """функция изменяет плановые трудозатраты"""
        self.cursor.execute(f"UPDATE `planned_labor_costs` "
                            f"SET "
                            f"month_hours = '{hours}',"
                            f"month_plan = '{month_plan}',"
                            f"planned_on = '{spent_on}',"
                            f"updated_on = '{updated_on}'"
                            f"WHERE "
                            f"id = {id_labor_cost}")
        self.database.commit()

    def update_month_in_custom_fields(self, issue_id: int, month_plan: str):
        """функция добавляет месяц в план месяца задачи"""
        self.cursor.execute(
            f"INSERT INTO `custom_values` "
            f"SET "
            f"value = '{month_plan}',"
            f"custom_field_id = 83,"
            f"customized_id = {issue_id},"
            f"customized_type = 'Issue'")
        self.database.commit()

    def delete_planed_labor_cost(self, id_labor_cost: int):
        """функция удаляет плановые трудозатраты"""
        self.cursor.execute(f"DElETE FROM `planned_labor_costs` WHERE id={id_labor_cost}")
        self.database.commit()

    def update_result_issue(self, issue_id, value):
        """функция изменяет результат задачи"""
        self.cursor.execute(
            f"UPDATE `custom_values` "
            f"SET value = '{value}' "
            f"WHERE custom_field_id = 7 and "
            f"customized_id = {issue_id} and "
            f"customized_type = 'Issue'")
        self.database.commit()

    def get_sectors(self):
        """функция находит сектора"""
        self.cursor.execute(f"SELECT possible_values FROM custom_fields WHERE id=11")
        sectors = self.cursor.fetchall()
        values = []
        sectors = str(sectors[0]).split('\\n')
        sectors.remove(sectors[0])
        sectors.remove(sectors[-1])
        values.append([sector[2:] for sector in sectors])
        return values[0]

    def get_workers_from_sector(self, sector):
        """функция находит id сотрудников данного сектора"""
        self.cursor.execute(f"SELECT customized_id FROM custom_values WHERE value='{sector}' "
                            f"AND customized_type='Principal' AND custom_field_id=11")
        return self.cursor.fetchall()

    def check_user(self, worker_id):
        """функция проверяет на наличие уволеных сотрудников"""
        self.cursor.execute(f"SELECT status FROM users WHERE id={worker_id}")
        return self.cursor.fetchall()
