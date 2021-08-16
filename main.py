import sqlite3
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix import widget
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox


class Database:
    database_path = "todo.db"

    def start_connection(self):
        """Returns connection object"""
        connection = sqlite3.connect(self.database_path)
        return connection


class ListItemWithCheckBox(OneLineAvatarIconListItem, TouchBehavior):
    """Custom list with an icon as the left widget"""
    dialog = None
    icon = StringProperty("reminder")
    identifier = StringProperty("")  # stores input text to be used to remove from database


# Somehow the double tap creates two dialog boxes instead of one
    def on_double_tap(self, *args):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Options:",
                size_hint=(0.4, 0.3),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        text_color=self.theme_cls.primary_color,
                        on_press=lambda _: self.close_dialog()
                    ),
                    MDFlatButton(
                        text="DELETE", text_color=self.theme_cls.primary_color
                    ),
                    MDFlatButton(
                        text="EDIT", text_color=self.theme_cls.primary_color
                    )
                ],
            )
        self.dialog.open()

    def close_dialog(self):
        self.dialog.dismiss()


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
        cursor.execute('DELETE FROM todo WHERE Task=?', [identifier])
        connection.commit()
        connection.close()

    def remove_from_list_view(self, widget):
        self.ids.scroll_list.remove_widget(widget)


class MainApp(MDApp):

    def build(self):
        Builder.load_file("frontend.kv")
        return ToDoList()

    def on_start(self):
        """Loads the whole database as a list upon start"""
        connection = Database().start_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM todo')
        result = cursor.fetchall()  # Stores the whole database into a variable; list of tuples
        connection.close()

        app = App.get_running_app()  # Return instance of the app
        for item in result:
            app.root.ids.scroll_list.add_widget(ListItemWithCheckBox(text=item[0]))


MainApp().run()
