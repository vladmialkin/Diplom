from models.model import Model
from working_hours import WorkingHours


class AdminModel(Model):
    def __init__(self, redmine, database, user_model):
        super().__init__()
        self.redmine = redmine
        self.database = database
        self.user_model = user_model

        self.working_hours = WorkingHours()
