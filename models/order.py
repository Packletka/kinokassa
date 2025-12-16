from pydantic import BaseModel, Field
from typing import List


class OrderItem(BaseModel):
    row: int
    seat: int
    price: int


class Order(BaseModel):
    id: int
    session_id: int
    movie_title: str
    cinema_name: str
    date: str
    time: str
    total: int
    items: List[OrderItem] = Field(default_factory=list)
    created_at: str
