from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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
    items = []
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