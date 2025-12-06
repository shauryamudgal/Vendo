from typing import Optional, List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, func
from datetime import datetime
from decimal import Decimal

from backend.database.db import Base

class User(Base):
  """
  Stores basic account information for each shopkeeper to link all stock, 
  sales, and summary data to the correct user.
  """

  __tablename__ = "user_account"

  id: Mapped[int] = mapped_column(Integer, primary_key = True)
  name: Mapped[str] = mapped_column(String(30))
  fullname: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
  shop_name: Mapped[str] = mapped_column(String(50))
  phone: Mapped[str] = mapped_column(String(20), nullable=True)
  email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

  items: Mapped[List["Items"]] = relationship(
    back_populates="user", cascade="all, delete-orphan"
  )  
  sales: Mapped[List["Sales"]] = relationship(
    back_populates="user", cascade="all, delete-orphan"
  )

  def __repr__(self) -> str:
    return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r}, shop_name={self.shop_name!r}, phone={self.phone!r}, email={self.email!r})"

class Items(Base):
  """
  Stores all the information about the items for each shopkeeper.
  """

  __tablename__ = "items"

  id: Mapped[int] = mapped_column(Integer, primary_key = True)
  name: Mapped[str] = mapped_column(String(50))
  category: Mapped[str] = mapped_column(String(50))
  current_stock: Mapped[int] = mapped_column(Integer, default = 0)
  user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_account.id"), nullable=False)

  user: Mapped["User"] = relationship(back_populates="items")
  sales_items: Mapped[List["SalesItems"]] = relationship(
    back_populates="items", cascade="all, delete-orphan"
  )

  def __repr__(self) -> str:
    return f"Items(id={self.id!r}, name={self.name!r}, category={self.category!r}, current_stock={self.current_stock!r})"

class Sales(Base):
  """
  Stores all the information about each sale happened with the timestamp
  of the sale.
  """

  __tablename__ = "sales"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_account.id"), nullable=False)
  total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
  created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default = func.now(),
  )
  updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), 
    server_default=func.now(), 
    onupdate=func.now()
  )

  user: Mapped["User"] = relationship(back_populates="sales")
  sales_items: Mapped[List["SalesItems"]] = relationship(
    "SalesItems", back_populates="sales", cascade="all, delete-orphan"
  )

  def __repr__(self) -> str:
    return f"Sales(id={self.id!r}, total_amount={self.total_amount!r}, created_at={self.created_at!r})"

class SalesItems(Base):
  """
  Stores about all the items sold in a particular sale that is made.
  """

  __tablename__ = "sales_items"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  quantity: Mapped[int] = mapped_column(Integer, nullable=False)
  unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
  line_total: Mapped[Decimal] = mapped_column(Numeric(10, 2))
  sales_id: Mapped[int] = mapped_column(ForeignKey("sales.id"))
  item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))

  sales: Mapped["Sales"] = relationship(back_populates="sales_items")
  items: Mapped["Items"] = relationship(back_populates="sales_items")

  def __repr__(self) -> str:
    return f"SalesItems(id={self.id!r}, quantity={self.quantity!r}, unit_price={self.unit_price!r}, line_total={self.line_total!r})"