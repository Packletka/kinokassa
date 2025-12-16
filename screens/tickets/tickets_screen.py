from pathlib import Path
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from services.auth_service import AuthService
from kivymd.uix.button import MDFlatButton
from services.hall_service import HallService
from kivymd.uix.dialog import MDDialog

from services.order_service import OrderService

Builder.load_file("screens/tickets/tickets_screen.kv")


class TicketsScreen(MDScreen):
    cancel_dialog = None

    def on_pre_enter(self, *args):
        self.refresh()

    def refresh(self):
        container = self.ids.tickets_container
        container.clear_widgets()

        user = AuthService().get_current_user()
        if not user:
            container.add_widget(MDLabel(text="Войдите в профиль, чтобы видеть свои билеты", halign="center"))
            return

        orders = OrderService().list_orders_by_user(user.id)
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

            if o.status == "paid":
                from kivymd.uix.button import MDRaisedButton
                btn = MDRaisedButton(
                    text="Вернуть билет",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    md_bg_color=(0.8, 0.1, 0.1, 1),  # красная кнопка
                    on_release=lambda x, order=o: self.confirm_cancel(order),
                )
                card.add_widget(btn)
            else:
                card.add_widget(MDLabel(text="Статус: отменён", theme_text_color="Secondary", adaptive_height=True))

            container.add_widget(card)

    def go_back(self):
        self.manager.current = "home"

    def cancel(self, order):
        user = AuthService().get_current_user()
        if not user:
            return

        # 1) отменяем заказ
        updated = OrderService().cancel_order(order.id, user.id)

        # 2) освобождаем места
        hs = HallService()
        seats = [(i.row, i.seat) for i in updated.items]
        hs.release_seats(updated.session_id, seats)

        # 3) обновляем список
        self.refresh()

    def confirm_cancel(self, order):
        if self.cancel_dialog:
            self.cancel_dialog.dismiss()
            self.cancel_dialog = None

        self.cancel_dialog = MDDialog(
            title="Вернуть билет?",
            text=(
                f"Фильм: {order.movie_title}\n"
                f"Дата: {order.date} {order.time}\n\n"
                "Места будут освобождены."
            ),
            buttons=[
                MDFlatButton(
                    text="Отмена",
                    on_release=lambda x: self.cancel_dialog.dismiss(),
                ),
                MDFlatButton(
                    text="Вернуть",
                    theme_text_color="Error",
                    on_release=lambda x: (
                        self.cancel_dialog.dismiss(),
                        self.cancel(order),
                    ),
                ),
            ],
        )
        self.cancel_dialog.open()
