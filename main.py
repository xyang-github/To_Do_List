import sqlite3
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
    database_path = "todo.db"

    def add_record(self):
        """Adds a new record to the database"""

        self.task = self.ids.input.text  # Stores text input into variable
        self.connection = Database().start_connection()
        self.connection.execute("""
            INSERT INTO todo VALUES(?)
            """, [self.task])
        self.connection.commit()
        self.connection.close()

        self.ids.scroll_list.add_widget(
            ListItemWithCheckBox(text=f"{self.task}", icon="reminder"))
        self.task = self.ids.input.text = ""  # Deletes text from textbox after adding to record


class MainApp(MDApp):
    def build(self):
        Builder.load_file("frontend.kv")
        return ToDoList()

    def on_start(self):
        """Need to load the whole database as a list upon start"""
        connection = Database().start_connection()
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM todo
        """)
        result = cursor.fetchall()
        connection.close()
        print(result)  # Work still needs to be done


MainApp().run()
