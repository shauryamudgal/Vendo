from datetime import datetime, timedelta
from decimal import Decimal
from .database import engine, Base, SessionLocal
from .models import User, Items, Sales, SalesItems 


def dt(days=0, h=9, m=0):
    return (datetime.utcnow() + timedelta(days=days)).replace(hour=h, minute=m, second=0, microsecond=0)


def seed():
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:

        users = [
            User(id=1, name="Ravi", fullname="Ravi Kumar", shop_name="Ravi Store", phone=9991112222, email=None),
            User(id=2, name="Amit", fullname="Amit Shah", shop_name="Amit Mart", phone=9991113333, email=None),
            User(id=3, name="Sita", fullname="Sita Devi", shop_name="Sita Kirana", phone=9991114444, email=None),
        ]
        for u in users:
            session.merge(u)


        default_items = [
            ("Parle G Biscuit", "Snacks", 40),
            ("Tata Salt 1kg", "Staples", 25),
            ("Sunflower Oil 1L", "Grocery", 15),
            ("Colgate Toothpaste", "Personal Care", 18),
            ("Maggi 2-Min Noodles", "Snacks", 30),
        ]

        for user in users:
            for (name, cat, stock) in default_items:
                session.add(Items(
                    name=name,
                    category=cat,
                    current_stock=str(stock),
                    user_id=user.id
                ))

        session.flush()

        def find_item(user_id, name):
            return session.query(Items).filter_by(user_id=user_id, name=name).first()

        custom_items = {
            1: [("Chips Packet", "Snacks", 20), ("Cold Drink", "Beverages", 10)],
            2: [("Bread", "Bakery", 15), ("Bananas", "Fruit", 25)],
            3: [("Samosa", "Food", 12), ("Lassi", "Beverages", 18)],
        }

        for uid, item_list in custom_items.items():
            for (name, cat, stock) in item_list:
                session.add(Items(
                    name=name,
                    category=cat,
                    current_stock=str(stock),
                    user_id=uid
                ))

        session.flush()

        def add_sale(user_id, dt_val, total, items_list):
            sale = Sales(user_id=user_id, created_at=dt_val, total_amount=Decimal(total))
            session.add(sale)
            session.flush()

            for (name, qty, price) in items_list:
                item = find_item(user_id, name)
                lt = Decimal(qty) * Decimal(price)
                session.add(SalesItems(
                    sales_id=sale.id,
                    item_id=item.id,
                    quantity=qty,
                    unit_price=Decimal(price),
                    line_total=lt
                ))

        add_sale(1, dt(-1, 10, 30), 120, [("Parle G Biscuit", 2, 10), ("Cold Drink", 1, 40)])
        add_sale(1, dt(0, 12, 15), 240, [("Maggi 2-Min Noodles", 3, 15), ("Chips Packet", 2, 20)])

        add_sale(2, dt(-1, 11, 45), 180, [("Tata Salt 1kg", 2, 50), ("Bread", 1, 40)])
        add_sale(2, dt(0, 14, 10), 300, [("Colgate Toothpaste", 2, 35), ("Bananas", 5, 10)])

        add_sale(3, dt(-1, 9, 20), 90, [("Samosa", 3, 15), ("Parle G Biscuit", 1, 10)])
        add_sale(3, dt(0, 17, 55), 150, [("Lassi", 2, 30), ("Sunflower Oil 1L", 1, 120)])

        session.commit()

        print("Sample data for 3 users inserted successfully!")


if __name__ == "__main__":
    seed()
