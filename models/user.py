from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    password: str  # учебный проект: храним как есть (позже можно хэш)
    name: str
