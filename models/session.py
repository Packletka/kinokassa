from pydantic import BaseModel


class Session(BaseModel):
    id: int
    movie_id: int
    cinema_id: int
    date: str
    time: str
    price: int
