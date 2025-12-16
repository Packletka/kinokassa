from pydantic import BaseModel


class Seat(BaseModel):
    row: int
    number: int
    is_occupied: bool = False
    is_selected: bool = False
