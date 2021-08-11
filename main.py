from kivy.app import App
from kivy.lang import Builder
from kivymd.app import MDApp




class MainApp(MDApp):
    def build(self):
        return Builder.load_file("frontend.kv")



MainApp().run()