import json
from pathlib import Path
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from services.hall_service import HallService

from models.seat import Seat
from widgets.seat_button import SeatButton

Builder.load_file(str(Path(__file__).with_name("hall_screen.kv")))


class HallScreen(MDScreen):
    session_id = NumericProperty(-1)
    seat_price = 0

    def on_pre_enter(self, *args):
        self.load_hall()

    def load_hall(self):
        container = self.ids.hall_container
        container.clear_widgets()

        hs = HallService()
        layout = hs.get_layout()
        occupied_seats = hs.get_occupied(int(self.session_id))
        occupied_set = set(occupied_seats)

        self.seats = []

        for row in range(1, layout["rows"] + 1):
            row_layout = MDBoxLayout(orientation="horizontal", spacing="6dp", adaptive_height=True)
            row_layout.add_widget(MDLabel(text=f"Ряд {row}", size_hint_x=None, width="60dp"))

            for seat_num in range(1, layout["seats_per_row"] + 1):
                is_occupied = (row, seat_num) in occupied_set
                seat = Seat(row=row, number=seat_num, is_occupied=is_occupied)
                btn = SeatButton(seat, self.on_seat_toggle)
                row_layout.add_widget(btn)
                self.seats.append(seat)

            container.add_widget(row_layout)

        self.update_total()

    def on_seat_toggle(self, *_):
        self.update_total()

    def update_total(self):
        selected = [s for s in self.seats if s.is_selected]
        total = len(selected) * self.seat_price
        self.ids.total_label.text = f"Итого: {total} ₽"

    def proceed(self):
        selected = [(s.row, s.number) for s in self.seats if s.is_selected]
        if not selected:
            print("NO SEATS SELECTED")
            return

        checkout = self.manager.get_screen("checkout")
        checkout.session_id = int(self.session_id)
        checkout.seat_price = int(self.seat_price)
        checkout.seats = [list(x) for x in selected]
        self.manager.current = "checkout"

    def go_back(self):
        self.manager.current = "sessions"
