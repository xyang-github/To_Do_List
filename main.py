import sqlite3

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.modules import keybinding
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.list import OneLineIconListItem


class Database:
    database_path = "todo.db"

    def start_connection(self):
        """Returns connection to database"""
        connection = sqlite3.connect(self.database_path)
        return connection

    def add_record(self):
        pass

    def edit_record(self):
        pass

    def remove_record(self):
        pass


class ToDoList(TouchBehavior, OneLineIconListItem):
    def add_task(self):
        pass

    def edit_task(self):
        pass

    def remove_task(self):
        pass


class MainApp(MDApp):
    def build(self):
        return Builder.load_file("frontend.kv")

    def new_task(self):
        print("hello world")


MainApp().run()
