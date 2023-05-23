from date import Date
from redmine_api import RedmineApi
from database import DataBase
from os.path import abspath
import pathlib


class Model:
    def __init__(self):
        self.date = Date()
        self.redmine = RedmineApi()
        self.database = DataBase()
        self.assets_path = pathlib.Path(abspath(__file__)[0:-16], 'assets')

    @staticmethod
    def insert_to_path(path, new_file):
        return pathlib.Path(path, new_file)
