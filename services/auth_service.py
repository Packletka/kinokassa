import json
from pathlib import Path
from typing import Optional

from models.user import User


class AuthService:
    def __init__(self):
        self.users_path = Path("data/users.json")
        self.current_path = Path("data/current_user.json")

    def _load_users(self) -> list[User]:
        raw = json.loads(self.users_path.read_text(encoding="utf-8"))
        return [User.model_validate(u) for u in raw]

    def _save_users(self, users: list[User]) -> None:
        self.users_path.write_text(
            json.dumps([u.model_dump() for u in users], ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def get_current_user(self) -> Optional[User]:
        raw = self.current_path.read_text(encoding="utf-8").strip()
        if raw in ("", "null", "None"):
            return None
        data = json.loads(raw)
        if data is None:
            return None
        return User.model_validate(data)

    def set_current_user(self, user: Optional[User]) -> None:
        self.current_path.write_text(
            json.dumps(user.model_dump() if user else None, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def register(self, email: str, password: str) -> User:
        email = (email or "").strip().lower()
        password = (password or "").strip()

        if not email or not password:
            raise ValueError("Заполни email и пароль.")

        users = self._load_users()
        if any(u.email == email for u in users):
            raise ValueError("Пользователь с таким email уже существует.")

        next_id = (max([u.id for u in users]) + 1) if users else 1
        name = email.split("@")[0]  # простое имя по email
        user = User(id=next_id, email=email, password=password, name=name)

        users.append(user)
        self._save_users(users)
        self.set_current_user(user)
        return user

    def login(self, email: str, password: str) -> User:
        email = (email or "").strip().lower()
        password = (password or "").strip()

        users = self._load_users()
        for u in users:
            if u.email == email and u.password == password:
                self.set_current_user(u)
                return u
        raise ValueError("Неверный email или пароль.")

    def logout(self) -> None:
        self.set_current_user(None)
