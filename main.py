import sqlite3
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix import widget
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior, CircularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, IRightBody, OneLineListItem, OneLineIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox


class Database:
    database_path = "todo.db"

    def start_connection(self):
        """Returns connection object"""
        connection = sqlite3.connect(self.database_path)
        return connection


class CompletedList(OneLineAvatarIconListItem):
    """Custom list with an icon for completed tasks"""


class ListItemWithCheckBox(OneLineAvatarIconListItem, TouchBehavior):
    """Custom list with an icon as the left widget"""
    icon = StringProperty("reminder")
    identifier = StringProperty("")  # stores input text to be used to remove from database


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    """Custom right container."""


class ToDoList(MDBoxLayout):

    def add_record(self):
        """Adds a new record to the database if textbox is not empty"""
        self.task = self.ids.input.text  # Stores text from 'input' into variable
        if self.task != "":
            connection = Database().start_connection()
            cursor = connection.cursor()
            cursor.execute('INSERT INTO todo VALUES(?)', [self.task])
            connection.commit()
            connection.close()

            self.add_to_list_view()

            self.ids.input.text = ""  # Deletes text from textbox after adding to record
        else:
            return

    def add_to_list_view(self):
        """Add to list view"""
        self.ids.scroll_list.add_widget(
            ListItemWithCheckBox(text=f"{self.task}", icon="reminder"))

    def delete_record(self, identifier):
        """Delete record from the database"""

        connection = Database().start_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO completed (Task) SELECT Task from todo WHERE Task=?', [identifier])
        cursor.execute('DELETE FROM todo WHERE Task=?', [identifier])
        connection.commit()
        connection.close()

    def remove_from_list_view(self, widget):
        self.ids.scroll_list.remove_widget(widget)

    def add_to_complete_list(self, completed_task):
        self.ids.complete_list.add_widget(
            CompletedList(text=f"[s][i]{completed_task}[/i][/s]", markup=True))

    def clear_complete_list(self):
        connection = Database().start_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM completed")
        connection.commit()
        connection.close()

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
