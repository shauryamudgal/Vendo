from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database.db import get_db
from backend.models.models import Items
from backend.schemas.stock_schemas import Stock, LowStockItems, UpdateStock, UpdatedStockInfo, ItemStock

import logging

router = APIRouter(prefix="/stock", tags=["Stock"])

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

@router.get('/', response_model=Stock)
def get_all_stock(user_id: int, db: Session = Depends(get_db)):
  try:
    items: List[Items] = db.query(Items).filter(Items.user_id == user_id).all()
    items_response: List[ItemStock] = [
      ItemStock(
        id = item.id,
        name = item.name,
        category = item.category,
        current_stock = item.current_stock
      )
      for item in items
    ]
    return Stock(
      count = len(items_response),
      items = items_response
    )
  
  except Exception as e:
    logger.error(f"Error while fetching stock {str(e)}")
    raise HTTPException(
      status_code = 500,
      detail = f"An error occured while fetching stock: {str(e)}"
    )
  
@router.get('/low', response_model=LowStockItems)
def get_low_stock(user_id: int, threshold: int, db: Session = Depends(get_db)):
  try:
    low_stock: List[Items] = db.query(Items).filter(Items.user_id == user_id).filter(Items.current_stock <= threshold).all()
    low_stock_items: List[ItemStock] = [
      ItemStock(
        id = item.id,
        name = item.name,
        category = item.category,
        current_stock = item.current_stock
      )
      for item in low_stock
    ]
    return LowStockItems(
      threshold = threshold,
      count = len(low_stock_items),
      low_stock_items = low_stock_items
    )
  
  except Exception as e:
    logger.error(f"Error while fetching low stock {str(e)}")
    raise HTTPException(
      status_code = 500,
      detail = f"An error occured while fetching low stock items {str(e)}"
    )

@router.patch('/update', response_model=UpdatedStockInfo)
def update_stock(request: UpdateStock, db: Session = Depends(get_db)):
  try:
    item = db.query(Items).filter(Items.id == request.item_id).first()
    if not item:
      raise HTTPException(status_code=404, detail="Item not found")
    
    item.current_stock = item.current_stock + request.new_stock

    db.commit()
    db.refresh(item)

    return UpdatedStockInfo(
      status="Stock updated successfully",
      item_id=item.id,
      name=item.name,
      category=item.category,
      new_stock = request.new_stock,
      current_stock=item.current_stock
    )
  
  except Exception as e:
    logger.error(f"Stock update was not successful {str(e)}")
    raise HTTPException(
      status_code = 500,
      detail = f"An error occured while updating the stock {str(e)}"
    )