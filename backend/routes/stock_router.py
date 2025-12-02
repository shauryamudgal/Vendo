from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Integer, List

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
    items = List[Items]
    items.append(db.query(Items).filter(Items.user_id == user_id).all())
    count = len(items)
    return Stock(
      count = count,
      items = items
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
    low_stock_items = List[ItemStock]
    low_stock_items.append(db.query(Items).filter(Items.user_id == user_id).filter(Items.current_stock.cast(Integer) <= threshold).all())
    count = len(low_stock_items)
    return LowStockItems(
      threshold = threshold,
      count = count,
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
    item.current_stock = str(request.new_stock)

    db.commit()
    db.refresh(item)

    return UpdatedStockInfo(
      status = "Stock updated successfully",
      item_id = item.id,
      name = item.name,
      category = item.category,
      new_stock = int(item.current_stock)
    )
  
  except Exception as e:
    logger.error(f"Stock update was not successful {str(e)}")
    raise HTTPException(
      status_code = 500,
      detail = f"An error occured while updating the stock {str(e)}"
    )