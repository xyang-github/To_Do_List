import sqlite3

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.modules import keybinding
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem

Builder.load_file("frontend.kv")

class Database(MDBoxLayout):
    database_path = "todo.db"

    def start_connection(self):
        """Returns connection to database"""
        connection = sqlite3.connect(self.database_path)
        return connection

    def commit_connection(self, connection):
        """Commit changes and closes connection to database"""
        self.connection.commit()
        self.connection.close()

    def add_record(self):
        """Adds a new record to the database"""
        task = self.ids.input.text  # Stores text input into variable
        self.connection = self.start_connection()
        self.connection.execute("""
        INSERT INTO todo VALUES(?)
        """, [task])
        self.commit_connection(self.connection)

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


class RootWidget(MDBoxLayout):
    pass


class MainApp(MDApp):
    def build(self):
        return RootWidget()


MainApp().run()
