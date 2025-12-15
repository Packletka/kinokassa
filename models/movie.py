from pydantic import BaseModel, Field
from typing import List, Optional


class Movie(BaseModel):
    id: int
    title: str
    description: str
    genres: List[str] = Field(default_factory=list)
    age_rating: str = "0+"
    duration_min: int = 0
    rating: float = 0.0
    poster: Optional[str] = None  # путь к файлу в assets/posters или URL
