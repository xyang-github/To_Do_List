import sqlite3

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox


class Database:
    database_path = "todo.db"

    def start_connection(self):
        connection = sqlite3.connect(self.database_path)
        return connection


class ListItemWithCheckBox(OneLineAvatarIconListItem):
    """Custom list with an icon as the left widget"""
    icon = StringProperty("reminder")


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    """Custom right container."""


class ToDoList(MDBoxLayout):

    def add_record(self):
        """Adds a new record to the database"""

        self.task = self.ids.input.text  # Stores text input into variable
        self.connection = Database().start_connection()
        self.connection.execute("""
            INSERT INTO todo VALUES(?)
            """, [self.task])
        self.connection.commit()
        self.connection.close()

        # Add to list view
        self.ids.scroll_list.add_widget(
            ListItemWithCheckBox(text=f"{self.task}", icon="reminder"))
        self.task = self.ids.input.text = ""  # Deletes text from textbox after adding to record


class MainApp(MDApp):
    def build(self):
        Builder.load_file("frontend.kv")
        return ToDoList()

    def on_start(self):
        """Loads the whole database as a list upon start"""
        connection = Database().start_connection()
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM todo
        """)
        result = cursor.fetchall()
        connection.close()
        app = App.get_running_app()
        for item in result:
            app.root.ids.scroll_list.add_widget(ListItemWithCheckBox(text=item[0]))


MainApp().run()
