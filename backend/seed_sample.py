from datetime import datetime, timedelta
from decimal import Decimal

from backend.database.db import SessionLocal, create_tables
from backend.models.models import User, Items, Sales, SalesItems


def dt(days=0, h=9, m=0):
    return (datetime.utcnow() + timedelta(days=days)).replace(
        hour=h, minute=m, second=0, microsecond=0
    )


def seed():

    create_tables()

    with SessionLocal() as db:

        users = [
            User(id=1, name="Ravi", fullname="Ravi Kumar", shop_name="Ravi Store", phone=9991112222, email=None),
            User(id=2, name="Amit", fullname="Amit Shah", shop_name="Amit Mart", phone=9991113333, email=None),
            User(id=3, name="Sita", fullname="Sita Devi", shop_name="Sita Kirana", phone=9991114444, email=None),
        ]

        for u in users:
            db.add(u)

        db.commit()

        default_items = [
            ("Parle G Biscuit", "Snacks", 40),
            ("Tata Salt 1kg", "Staples", 25),
            ("Sunflower Oil 1L", "Grocery", 15),
            ("Colgate Toothpaste", "Personal Care", 18),
            ("Maggi Noodles", "Snacks", 30),
        ]

        for u in users:
            for (name, cat, stock) in default_items:
                db.add(Items(
                    name=name,
                    category=cat,
                    current_stock=int(stock),
                    user_id=u.id
                ))

        db.commit()

        def find_item(user_id, name):
            return db.query(Items).filter_by(user_id=user_id, name=name).first()

        custom_items = {
            1: [("Chips Packet", "Snacks", 20), ("Cold Drink", "Beverages", 10)],
            2: [("Bread", "Bakery", 15), ("Bananas", "Fruit", 25)],
            3: [("Samosa", "Food", 12), ("Lassi", "Beverages", 18)],
        }

        for uid, items_list in custom_items.items():
            for (name, cat, stock) in items_list:
                db.add(Items(
                    name=name,
                    category=cat,
                    current_stock=int(stock),
                    user_id=uid
                ))

        db.commit()

        def add_sale(user_id, ts, total, line_items):
            sale = Sales(
                user_id=user_id,
                created_at=ts,
                total_amount=Decimal(total)
            )
            db.add(sale)
            db.commit()  

            for (item_name, qty, price) in line_items:
                item = find_item(user_id, item_name)
                lt = Decimal(qty) * Decimal(price)
                db.add(SalesItems(
                    sales_id=sale.id,
                    item_id=item.id,
                    quantity=qty,
                    unit_price=Decimal(price),
                    line_total=lt
                ))
            db.commit()

        add_sale(1, dt(-1, 10, 30), 120, [
            ("Parle G Biscuit", 2, 10),
            ("Cold Drink", 1, 40),
        ])
        add_sale(1, dt(0, 12, 15), 240, [
            ("Maggi Noodles", 3, 15),
            ("Chips Packet", 2, 20),
        ])

        add_sale(2, dt(-1, 11, 45), 180, [
            ("Tata Salt 1kg", 2, 50),
            ("Bread", 1, 40),
        ])
        add_sale(2, dt(0, 14, 10), 300, [
            ("Colgate Toothpaste", 2, 35),
            ("Bananas", 5, 10),
        ])

        add_sale(3, dt(-1, 9, 20), 90, [
            ("Samosa", 3, 15),
            ("Parle G Biscuit", 1, 10),
        ])
        add_sale(3, dt(0, 17, 55), 150, [
            ("Lassi", 2, 30),
            ("Sunflower Oil 1L", 1, 120),
        ])

        print("✔ Sample data created successfully for 3 users!")


if __name__ == "__main__":
    seed()
