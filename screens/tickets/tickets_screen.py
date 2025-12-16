from pathlib import Path
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

from services.order_service import OrderService

Builder.load_file("screens/tickets/tickets_screen.kv")


class TicketsScreen(MDScreen):
    def on_pre_enter(self, *args):
        self.refresh()

    def refresh(self):
        container = self.ids.tickets_container
        container.clear_widgets()

        orders = OrderService().list_orders()
        if not orders:
            container.add_widget(MDLabel(text="Пока нет купленных билетов", halign="center"))
            return

        for o in reversed(orders):
            card = MDCard(orientation="vertical", padding=12, spacing=6, radius=[16] * 4, size_hint_y=None)
            card.bind(minimum_height=card.setter("height"))

            card.add_widget(MDLabel(text=f"Заказ №{o.id}: {o.movie_title}", bold=True, adaptive_height=True))
            card.add_widget(MDLabel(text=f"{o.cinema_name}", theme_text_color="Secondary", adaptive_height=True))
            card.add_widget(MDLabel(text=f"{o.date} • {o.time}", theme_text_color="Secondary", adaptive_height=True))
            card.add_widget(
                MDLabel(text=f"Места: {', '.join([f'{i.row}-{i.seat}' for i in o.items])}", adaptive_height=True))
            card.add_widget(MDLabel(text=f"Итого: {o.total} ₽", bold=True, adaptive_height=True))
            card.add_widget(MDLabel(text=f"Создан: {o.created_at}", theme_text_color="Secondary", adaptive_height=True))

            container.add_widget(card)

    def go_back(self):
        self.manager.current = "home"
