import sqlite3

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.modules import keybinding
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import OneLineIconListItem


class TextBox(MDBoxLayout):
    database_path = "todo.db"

    def add_record(self):
        """Adds a new record to the database"""

        task = self.ids.input.text  # Stores text input into variable

        self.connection = sqlite3.connect(self.database_path)
        self.connection.execute("""
            INSERT INTO todo VALUES(?)
            """, [task])
        self.connection.commit()
        self.connection.close()


class TaskList(MDBoxLayout):
    def add_task(self):
        pass

    def edit_task(self):
        pass

    def remove_task(self):
        pass


class Home(MDBoxLayout):
    pass


class MainApp(MDApp):
    def build(self):
        Builder.load_file("frontend.kv")
        return Home()


MainApp().run()
