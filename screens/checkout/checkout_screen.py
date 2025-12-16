from pathlib import Path
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivymd.uix.screen import MDScreen

from services.session_service import SessionService
from services.movie_service import MovieService
from services.order_service import OrderService
from services.auth_service import AuthService
from services.hall_service import HallService
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

Builder.load_file(str(Path(__file__).with_name("checkout_screen.kv")))


class CheckoutScreen(MDScreen):
    login_dialog = None

    session_id = NumericProperty(-1)
    seat_price = NumericProperty(0)
    seats = ListProperty([])  # [[row, seat], ...]

    movie_title = StringProperty("")
    cinema_line = StringProperty("")
    datetime_line = StringProperty("")
    seats_line = StringProperty("")
    total_line = StringProperty("")

    def on_pre_enter(self, *args):
        self.build_summary()

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
            text="Чтобы подтвердить покупку, нужно войти в профиль.",
            buttons=[
                MDFlatButton(text="Отмена", on_release=lambda x: self.login_dialog.dismiss()),
                MDFlatButton(text="Войти",
                             on_release=lambda x: (self.login_dialog.dismiss(), self._open_profile(back_target))),
            ],
        )
        self.login_dialog.open()

    def build_summary(self):
        ss = SessionService()
        ms = MovieService()

        session = ss.get_by_id(int(self.session_id))
        if not session:
            self.movie_title = "Сеанс не найден"
            return

        movie = ms.get_by_id(int(session.movie_id))
        title = movie.title if movie else "Фильм"

        cinema = ss.get_cinema_name(int(session.cinema_id))

        total = len(self.seats) * int(self.seat_price)
        seats_str = ", ".join([f"{r}-{s}" for r, s in self.seats]) if self.seats else "-"

        self.movie_title = title
        self.cinema_line = f"Кинотеатр: {cinema}"
        self.datetime_line = f"Дата/время: {session.date} • {session.time}"
        self.seats_line = f"Места (ряд-место): {seats_str}"
        self.total_line = f"Итого: {total} ₽"

    def confirm(self):
        from services.auth_service import AuthService
        auth = AuthService()
        user = auth.get_current_user()
        if not user:
            self.show_login_required_dialog(back_target="checkout")
            return

        ss = SessionService()
        ms = MovieService()
        os = OrderService()

        session = ss.get_by_id(int(self.session_id))
        if not session:
            self.manager.current = "home"
            return

        # ЗАНЯТЬ МЕСТА (до создания заказа!)
        self.ids.err_label.text = ""
        try:
            hs = HallService()
            hs.reserve_seats(int(self.session_id), [(r, s) for r, s in self.seats])
        except Exception as e:
            self.ids.err_label.text = str(e)
            return

        movie = ms.get_by_id(int(session.movie_id))
        cinema = ss.get_cinema_name(int(session.cinema_id))

        order = os.create_order(
            user_id=user.id,
            session_id=int(self.session_id),
            movie_title=(movie.title if movie else "Фильм"),
            cinema_name=cinema,
            date=session.date,
            time=session.time,
            seats=[list(x) for x in self.seats],
            seat_price=int(self.seat_price)
        )

        tickets = self.manager.get_screen("tickets")
        if hasattr(tickets, "refresh"):
            tickets.refresh()
        self.manager.current = "tickets"

    def go_back(self):
        self.manager.current = "hall"
