from pydantic import BaseModel
from typing import List

class UpdateStock(BaseModel):
  item_id: int
  new_stock: int

class UpdatedStockInfo(BaseModel):
  message: str
  updated_item_details: List[UpdateStock]

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