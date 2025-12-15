from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton

from models.movie import Movie


class MovieCard(MDCard):
    def __init__(self, movie: Movie, on_open=None, **kwargs):
        super().__init__(**kwargs)
        self.movie = movie
        self.on_open = on_open

        self.orientation = "vertical"
        self.padding = 12
        self.spacing = 8
        self.radius = [16, 16, 16, 16]
        self.elevation = 2

        # ВАЖНО: чтобы карточка имела высоту по содержимому
        self.size_hint_y = None
        self.bind(minimum_height=self.setter("height"))

        header = MDBoxLayout(orientation="horizontal", adaptive_height=True)
        header.add_widget(MDLabel(text=movie.title, bold=True, adaptive_height=True))
        header.add_widget(MDIconButton(icon="chevron-right", on_release=self._open))
        self.add_widget(header)

        self.add_widget(MDLabel(
            text=f"Жанры: {', '.join(movie.genres)}",
            theme_text_color="Secondary",
            adaptive_height=True
        ))

        self.add_widget(MDLabel(
            text=f"{movie.age_rating} • {movie.duration_min} мин • ⭐ {movie.rating}",
            theme_text_color="Secondary",
            adaptive_height=True
        ))

        desc = movie.description
        if len(desc) > 140:
            desc = desc[:140].rstrip() + "…"

        self.add_widget(MDLabel(
            text=desc,
            theme_text_color="Secondary",
            adaptive_height=True
        ))

    def _open(self, *_):
        if callable(self.on_open):
            self.on_open(self.movie)
