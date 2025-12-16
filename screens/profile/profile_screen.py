from pathlib import Path
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.screen import MDScreen

from services.auth_service import AuthService

Builder.load_file(str(Path(__file__).with_name("profile_screen.kv")))


class ProfileScreen(MDScreen):
    back_target = StringProperty("home")
    is_logged_in = BooleanProperty(False)

    def on_pre_enter(self, *args):
        self.refresh()

    def go_back(self):
        self.manager.current = self.back_target

    def open_tickets(self):
        self.manager.current = "tickets"

    def refresh(self):
        user = AuthService().get_current_user()
        self.is_logged_in = bool(user)
        self.ids.msg_label.text = ""

        if user:
            self.ids.status_label.text = f"Вы вошли как: {user.name} ({user.email})"
        else:
            self.ids.status_label.text = "Вы не вошли"

    def do_login(self):
        try:
            AuthService().login(self.ids.email_field.text, self.ids.pass_field.text)
            self.refresh()
        except Exception as e:
            self.ids.msg_label.text = str(e)

    def do_register(self):
        try:
            AuthService().register(self.ids.email_field.text, self.ids.pass_field.text)
            self.refresh()
        except Exception as e:
            self.ids.msg_label.text = str(e)

    def do_logout(self):
        AuthService().logout()
        self.ids.email_field.text = ""
        self.ids.pass_field.text = ""
        self.refresh()
