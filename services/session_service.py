import json
from pathlib import Path
from typing import List

from models.session import Session


class SessionService:
    def __init__(self):
        self.sessions_path = Path("data/sessions.json")
        self.cinemas_path = Path("data/cinemas.json")

    def get_sessions_for_movie(self, movie_id: int) -> List[Session]:
        raw = json.loads(self.sessions_path.read_text(encoding="utf-8"))
        sessions = [Session.model_validate(s) for s in raw]
        return [s for s in sessions if s.movie_id == movie_id]

    def get_cinema_name(self, cinema_id: int) -> str:
        cinemas = json.loads(self.cinemas_path.read_text(encoding="utf-8"))
        for c in cinemas:
            if c["id"] == cinema_id:
                return c["name"]
        return "Кинотеатр"
