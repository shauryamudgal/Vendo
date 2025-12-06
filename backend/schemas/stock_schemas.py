from pydantic import BaseModel
from typing import List, Optional

class UpdateStock(BaseModel):
  item_id: int
  new_stock: int

class UpdatedStockInfo(BaseModel):
  status: str
  item_id: int
  name: str
  category: Optional[str]
  new_stock: int

class ItemStock(BaseModel):
  id: int
  name: str
  category: str
  current_stock: int

class Stock(BaseModel):
  count: int
  items: List[ItemStock]

class LowStockItems(BaseModel):
  threshold: int
  count: int
  low_stock_items: List[ItemStock]