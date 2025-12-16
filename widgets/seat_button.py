from kivymd.uix.button import MDRaisedButton


class SeatButton(MDRaisedButton):
    def __init__(self, seat, on_toggle, **kwargs):
        super().__init__(**kwargs)
        self.seat = seat
        self.on_toggle = on_toggle

        self.text = str(seat.number)
        self.size_hint = (None, None)
        self.size = ("40dp", "40dp")

        self.update_color()

        if seat.is_occupied:
            self.disabled = True

        self.bind(on_release=self.toggle)

    def toggle(self, *_):
        if self.seat.is_occupied:
            return

        # сначала переключаем
        self.seat.is_selected = not self.seat.is_selected

        # спрашиваем у экрана: можно или нет
        ok = True
        if callable(self.on_toggle):
            ok = self.on_toggle(self.seat)

        if ok is False:
            # откат
            self.seat.is_selected = not self.seat.is_selected

        self.update_color()


    def update_color(self):
        if self.seat.is_occupied:
            self.md_bg_color = (0.6, 0.6, 0.6, 1)   # серый
        elif self.seat.is_selected:
            self.md_bg_color = (0.2, 0.6, 1, 1)    # синий
        else:
            self.md_bg_color = (0.9, 0.9, 0.9, 1)  # светлый
