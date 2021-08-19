import sqlite3
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox


class Database:
    database_path = "todo.db"

    def start_connection(self):
        """Returns connection object"""
        connection = sqlite3.connect(self.database_path)
        return connection

    def commit_close_connection(self, connection):
        """Commits and closes a pre-existing connection to database"""
        connection.commit()
        connection.close()

    def add_record(self, task):
        """Add task to to-do database"""
        connection = self.start_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO todo VALUES(?)', [task])
        self.commit_close_connection(connection)

    def delete_record(self, identifier):
        """Copies record to completed table, then deletes from todo table"""
        connection = self.start_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO completed (Task) SELECT Task from todo WHERE Task=?', [identifier])
        cursor.execute('DELETE FROM todo WHERE Task=?', [identifier])
        self.commit_close_connection(connection)

    def clear_completed_records(self):
        """Clears the 'completed' database"""
        connection = self.start_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM completed")
        self.commit_close_connection(connection)


class ListItemWithCheckBox(OneLineAvatarIconListItem, TouchBehavior):
    """List widget for to-do tasks"""
    icon = StringProperty("reminder")
    identifier = StringProperty("")  # identifies task in the database


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    """Custom right container."""


class CompletedList(OneLineAvatarIconListItem):
    """Custom list with an icon for completed tasks"""


class ToDoList(MDBoxLayout):

    def add_todo_list(self):
        """Adds widget to MDList"""
        self.task = self.ids.input.text  # Stores text from 'input' into variable
        if self.task != "":
            Database().add_record(self.task)
            self.ids.scroll_list.add_widget(
                ListItemWithCheckBox(text=f"{self.task}"))
            self.ids.input.text = ""  # Deletes text from textbox after adding to record
        else:
            return

    def remove_todo_list(self, identifier, widget):
        """Removes widget from MDList"""
        Database().delete_record(identifier)
        self.ids.scroll_list.remove_widget(widget)
        self.add_to_complete_list(identifier)

    def add_to_complete_list(self, completed_task):
        """Add widget to complete_list"""
        try:
            self.ids.complete_list.add_widget(
                CompletedList(text=f"[s][i]{completed_task}[/i][/s]", markup=True))
        except TypeError:  # Prevents crashing after completing the first item on start-up with empty completed list
            connection = Database().start_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT Task FROM completed WHERE Task = ?', [completed_task])
            completed_result = cursor.fetchall()
            connection.close()
            self.ids.complete_list.add_widget(CompletedList(text=f"[s][i]{completed_result[0][0]}[/i][/s]"))

    def clear_complete_list(self):
        """Deletes all records and widgets from complete db and complete_list"""
        Database().clear_completed_records()
        self.ids.complete_list.clear_widgets()


class MainApp(MDApp):

    def build(self):
        Builder.load_file("frontend.kv")
        return ToDoList()

    def on_start(self):
        """Loads the whole database as a list upon start"""
        connection = Database().start_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM todo')
        todo_result = cursor.fetchall()  # Stores the whole database into a variable; list of tuples
        cursor.execute('SELECT * FROM completed')
        completed_result = cursor.fetchall()
        connection.close()

        app = App.get_running_app()  # Return instance of the app
        for item in todo_result:
            app.root.ids.scroll_list.add_widget(ListItemWithCheckBox(text=item[0]))

        for item in completed_result:
            app.root.ids.complete_list.add_widget(CompletedList(text=f"[s][i]{item[0]}[/i][/s]"))


MainApp().run()
