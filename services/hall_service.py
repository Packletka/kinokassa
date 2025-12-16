import json
from pathlib import Path
from typing import List, Tuple


class HallService:
    def __init__(self):
        self.layout_path = Path("data/hall_layouts.json")
        self.occupied_path = Path("data/occupied_seats.json")

    def get_layout(self) -> dict:
        return json.loads(self.layout_path.read_text(encoding="utf-8"))["default"]

    def get_occupied(self, session_id: int) -> List[Tuple[int, int]]:
        raw = json.loads(self.occupied_path.read_text(encoding="utf-8"))
        items = raw.get(str(session_id), [])
        return [(r, s) for r, s in items]

    def reserve_seats(self, session_id: int, seats: List[Tuple[int, int]]) -> None:
        """
        Атомарно для нашего уровня: читаем occupied, проверяем конфликты,
        дописываем новые места, сохраняем обратно.
        """
        raw = json.loads(self.occupied_path.read_text(encoding="utf-8"))
        key = str(session_id)

        occupied = set((r, s) for r, s in raw.get(key, []))
        requested = set(seats)

        conflicts = requested & occupied
        if conflicts:
            # отдаём понятную ошибку
            conflicts_str = ", ".join([f"{r}-{s}" for r, s in sorted(conflicts)])
            raise ValueError(f"Эти места уже заняты: {conflicts_str}")

        new_occupied = sorted(list(occupied | requested))
        raw[key] = [[r, s] for r, s in new_occupied]

        self.occupied_path.write_text(
            json.dumps(raw, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def release_seats(self, session_id: int, seats: List[Tuple[int, int]]) -> None:
        raw = json.loads(self.occupied_path.read_text(encoding="utf-8"))
        key = str(session_id)

        occupied = set((r, s) for r, s in raw.get(key, []))
        to_release = set(seats)

        new_occupied = sorted(list(occupied - to_release))
        raw[key] = [[r, s] for r, s in new_occupied]

        self.occupied_path.write_text(
            json.dumps(raw, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
