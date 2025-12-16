import json
from datetime import datetime
from pathlib import Path
from typing import List

from models.order import Order, OrderItem


class OrderService:
    def __init__(self, path: str = "data/orders.json"):
        self.path = Path(path)

    def list_orders(self) -> List[Order]:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [Order.model_validate(o) for o in raw]

    def create_order(
        self,
        session_id: int,
        movie_title: str,
        cinema_name: str,
        date: str,
        time: str,
        seats: list[list[int]],   # [[row, seat], ...]
        seat_price: int
    ) -> Order:
        orders = self.list_orders()
        next_id = (max([o.id for o in orders]) + 1) if orders else 1

        items = [OrderItem(row=r, seat=s, price=seat_price) for r, s in seats]
        total = sum(i.price for i in items)

        order = Order(
            id=next_id,
            session_id=session_id,
            movie_title=movie_title,
            cinema_name=cinema_name,
            date=date,
            time=time,
            total=total,
            items=items,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        raw = [o.model_dump() for o in orders]
        raw.append(order.model_dump())
        self.path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")

        return order
