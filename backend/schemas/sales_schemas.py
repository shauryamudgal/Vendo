from pydantic import BaseModel
from typing import List
from datetime import datetime

class SaleItemRequest(BaseModel):
  item_id: int
  quantity: int
  unit_price: float

class AddSaleRequest(BaseModel):
  user_id: int
  items: List[SaleItemRequest]
  created_at: datetime

class SaleItemResponse(BaseModel):
  item_id: int
  quantity: int
  unit_price: float
  line_total: float

class SaleResponse(BaseModel):
  sale_id: int
  user_id: int
  total_amount: float
  items: List[SaleItemResponse]

class SalesListResponse(BaseModel):
  count: int
  sales: List[SaleResponse]