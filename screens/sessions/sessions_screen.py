from pathlib import Path
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from services.auth_service import AuthService
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from services.auth_service import AuthService

from services.session_service import SessionService

Builder.load_file(str(Path(__file__).with_name("sessions_screen.kv")))


class SessionScreen(MDScreen):
    movie_id = NumericProperty(-1)

    login_dialog = None

    def _open_profile(self, back_target: str):
        profile = self.manager.get_screen("profile")
        profile.back_target = back_target
        self.manager.current = "profile"

    def show_login_required_dialog(self, back_target: str):
        if self.login_dialog:
            self.login_dialog.dismiss()
            self.login_dialog = None

        self.login_dialog = MDDialog(
            title="Нужен вход",
            text="Чтобы выбрать места и купить билет, нужно войти в профиль.",
            buttons=[
                MDFlatButton(text="Отмена", on_release=lambda x: self.login_dialog.dismiss()),
                MDFlatButton(text="Войти", on_release=lambda x: (self.login_dialog.dismiss(), self._open_profile(back_target))),
            ],
        )
        self.login_dialog.open()

    def on_pre_enter(self, *args):
        self.service = SessionService()
        self.load_sessions()

    def load_sessions(self):
        container = self.ids.sessions_container
        container.clear_widgets()

        sessions = self.service.get_sessions_for_movie(int(self.movie_id))

        if not sessions:
            container.add_widget(MDLabel(
                text="Нет доступных сеансов",
                halign="center"
            ))
            return

        for s in sessions:
            cinema = self.service.get_cinema_name(s.cinema_id)

            card = MDCard(
                orientation="vertical",
                padding=12,
                spacing=8,
                radius=[16, 16, 16, 16],
                size_hint_y=None
            )
            card.bind(minimum_height=card.setter("height"))

            card.add_widget(MDLabel(text=cinema, bold=True, adaptive_height=True))
            card.add_widget(MDLabel(
                text=f"{s.date} • {s.time} • {s.price} ₽",
                theme_text_color="Secondary",
                adaptive_height=True
            ))

            btn = MDRaisedButton(
                text="Выбрать",
                on_release=lambda x, session=s: self.select_session(session)
            )
            card.add_widget(btn)

            container.add_widget(card)

    def select_session(self, session):
        if not AuthService().get_current_user():
            self.show_login_required_dialog(back_target="sessions")
            return

        hall = self.manager.get_screen("hall")
        hall.session_id = session.id
        hall.seat_price = session.price
        self.manager.current = "hall"

    def go_back(self):
        self.manager.current = "movie"
