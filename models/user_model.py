from models.model import Model


class UserModel(Model):
    def __init__(self, redmine, database):
        super().__init__()
        self.redmine = redmine
        self.database = database
        self.user = self.redmine.redmine.auth()
        self.user_id = self.user.id
        self.user_login = self.user.login
        self.user_name = self.user.__str__()
        self.issues = self.user.issues
        self.time_entries = self.user.time_entries
        self.groups = self.user.groups
        self.custom_fields = self.user.custom_fields
        self.sector = self.database.get_sector(user_id=self.user_id)
        self.admin_list = (540, 501, 177)

        self.supervisor_rights = False
        self.admin_rights = False

        self.check_rights()

    def check_rights(self):
        """функция проверки на наличие прав руководителя и администратора"""
        # if self.database.get_supervizor_rights(self.user_id) is not None:
        #     self.supervisor_rights = True
        if self.user_id in self.admin_list:
            self.admin_rights = True
            self.supervisor_rights = True
