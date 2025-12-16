from pathlib import Path
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivymd.uix.screen import MDScreen

from services.session_service import SessionService
from services.movie_service import MovieService
from services.order_service import OrderService
from services.auth_service import AuthService

Builder.load_file(str(Path(__file__).with_name("checkout_screen.kv")))


class CheckoutScreen(MDScreen):
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
        auth = AuthService()
        user = auth.get_current_user()
        if not user:
            profile = self.manager.get_screen("profile")
            profile.back_target = "checkout"
            self.manager.current = "profile"
            return

        ss = SessionService()
        ms = MovieService()
        os = OrderService()

        session = ss.get_by_id(int(self.session_id))
        movie = ms.get_by_id(int(session.movie_id)) if session else None
        cinema = ss.get_cinema_name(int(session.cinema_id)) if session else "Кинотеатр"

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

        print(f"ORDER CREATED id={order.id}, total={order.total}")

        # Перейти в "Мои билеты" и обновить список
        tickets = self.manager.get_screen("tickets")
        if hasattr(tickets, "refresh"):
            tickets.refresh()
        self.manager.current = "tickets"

    def go_back(self):
        self.manager.current = "hall"
