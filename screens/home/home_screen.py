from pathlib import Path
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

from services.movie_service import MovieService
from widgets.movie_card import MovieCard

Builder.load_file(str(Path(__file__).with_name("home_screen.kv")))


class HomeScreen(MDScreen):
    def on_pre_enter(self, *args):
        # on_pre_enter гарантированно вызовется, когда ids уже готовы
        if getattr(self, "_loaded", False):
            return
        self._loaded = True

        self.service = MovieService()
        self.load_movies()

    def load_movies(self, query: str = ""):
        container = self.ids.movies_container
        container.clear_widgets()

        movies = self.service.search(query)
        for m in movies:
            container.add_widget(MovieCard(movie=m, on_open=self.open_movie))

    def on_search_live(self, text: str):
        self.load_movies(text)

    def open_movie(self, movie):
        movie_screen = self.manager.get_screen("movie")
        movie_screen.movie_id = movie.id
        self.manager.current = "movie"

    def open_profile(self):
        profile = self.manager.get_screen("profile")
        profile.back_target = "home"
        self.manager.current = "profile"
