from pathlib import Path
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.screen import MDScreen

from services.movie_service import MovieService

Builder.load_file(str(Path(__file__).with_name("movie_screen.kv")))


class MovieScreen(MDScreen):
    movie_id = NumericProperty(-1)

    title_text = StringProperty("")
    meta_text = StringProperty("")
    description_text = StringProperty("")

    def on_pre_enter(self, *args):
        self.load_movie()

    def load_movie(self):
        service = MovieService()
        movie = service.get_by_id(int(self.movie_id))

        if not movie:
            self.title_text = "Фильм не найден"
            self.meta_text = ""
            self.description_text = ""
            return

        self.title_text = movie.title
        self.meta_text = f"{movie.age_rating} • {movie.duration_min} мин • ⭐ {movie.rating} • {', '.join(movie.genres)}"
        self.description_text = movie.description

    def go_back(self):
        self.manager.current = "home"

    def choose_session(self):
        screen = self.manager.get_screen("sessions")
        screen.movie_id = self.movie_id
        self.manager.current = "sessions"
