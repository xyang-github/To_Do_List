from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.modules import keybinding
from kivymd.app import MDApp




class MainApp(MDApp):
    def build(self):
        return Builder.load_file("frontend.kv")

    def new_task(self):
        print("hello world")





MainApp().run()