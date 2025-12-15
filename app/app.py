from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from app.router import setup_routes
from app.theme import setup_theme


class KinoKassaApp(MDApp):
    def build(self):
        setup_theme(self)

        self.sm = ScreenManager()
        setup_routes(self.sm)

        return self.sm
