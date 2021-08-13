import sqlite3
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox


class Database:
    database_path = "todo.db"

    def start_connection(self):
        connection = sqlite3.connect(self.database_path)
        return connection


class ListItemWithCheckBox(OneLineAvatarIconListItem):
    """Custom list with an icon as the left widget"""
    icon = StringProperty("reminder")
    identifier = StringProperty("")


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

        self.add_to_list_view()
        self.ids.input.text = ""  # Deletes text from textbox after adding to record

    def add_to_list_view(self):
        """Add to list view"""
        self.ids.scroll_list.add_widget(
            ListItemWithCheckBox(text=f"{self.task}", icon="reminder"))

    def delete_record(self, identifier):
        """Delete record from the database"""
        connection = Database().start_connection()
        cursor = connection.cursor()
        cursor.execute("""
        DELETE FROM todo WHERE Task=?
        """, [identifier])
        connection.commit()
        connection.close()

        ## reload the whole list to update listview?
        ## on_start should also create a db if one doesn't exist



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
        result = cursor.fetchall()  # Stores the whole database into a variable; list of tuples
        connection.close()
        app = App.get_running_app()  # Return instance of the app
        for item in result:
            app.root.ids.scroll_list.add_widget(ListItemWithCheckBox(text=item[0]))


MainApp().run()
