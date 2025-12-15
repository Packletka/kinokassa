import json
from pathlib import Path
from typing import List, Optional

from models.movie import Movie


class MovieService:
    def __init__(self, data_path: str = "data/movies.json"):
        self.data_path = Path(data_path)

    def get_movies(self) -> List[Movie]:
        raw = json.loads(self.data_path.read_text(encoding="utf-8"))
        return [Movie.model_validate(item) for item in raw]

    def search(self, query: str) -> List[Movie]:
        movies = self.get_movies()
        q = (query or "").strip().lower()
        if not q:
            return movies
        return [m for m in movies if q in m.title.lower()]

    def filter_by_genre(self, genre: Optional[str]) -> List[Movie]:
        movies = self.get_movies()
        if not genre:
            return movies
        return [m for m in movies if genre in m.genres]

    def get_by_id(self, movie_id: int) -> Movie | None:
        for m in self.get_movies():
            if m.id == movie_id:
                return m
        return None
