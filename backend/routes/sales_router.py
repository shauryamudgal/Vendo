from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta, UTC

from backend.database.db import get_db
from backend.models.models import Sales, SalesItems, Items
from backend.schemas.sales_schemas import AddSaleRequest, SaleResponse, SalesListResponse

import logging

router = APIRouter(prefix="/sales", tags=["Sales"])

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

@router.get('/', response_model=SalesListResponse)
def get_all_sales(
  user_id: int,
  start_date: Optional[str] = Query(None, description = "YYYY-MM-DD"),
  end_date: Optional[str] = Query(None, description = "YYYY-MM-DD"),
  db: Session = Depends(get_db)
):
  try:
    query = db.query(Sales).filter(Sales.user_id == user_id)

    if start_date:
      start_dt = datetime.strptime(start_date, "%Y-%m-%d")
      query = query.filter(Sales.created_at >= start_dt)

    if end_date:
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        end_dt = end_dt + timedelta(days=1) - timedelta(seconds=1)
        query = query.filter(Sales.created_at <= end_dt)

    sales = query.order_by(Sales.created_at.desc()).all()

    response_sales = []
    for sale in sales:
       response_sales.append({
        "sale_id": sale.id,
        "user_id": sale.user_id,
        "total_amount": sale.total_amount,
        "created_at": sale.created_at,
        "items": [
            {
              "item_id": si.item_id,
              "quantity": si.quantity,
              "unit_price": si.unit_price,
              "line_total": si.line_total
            }
            for si in sale.sales_items
        ]
       })

    return{
       "count": len(response_sales),
       "sales": response_sales
    }
  
  except Exception as e:
    logger.error(f"Sales were not retrieved successfully {str(e)}")
    raise HTTPException(
      status_code = 500,
      detail = f"An error occured while retrieving the sales {str(e)}"
    )

  
@router.post('/add', response_model=SaleResponse)
def add_sale(request: AddSaleRequest, db: Session = Depends(get_db)):
  try:
    sale = Sales(
      user_id = request.user_id,
      total_amount = 0
    )

    db.add(sale)
    db.flush()

    total_amount = 0
    sale_items_response = []

    for item in request.items:
      db_item = db.query(Items).filter(Items.id==item.item_id).first()
      if not db_item:
        raise HTTPException(status_code=404, detail=f"Item {item.item_id} not found")

      if int(db_item.current_stock) < item.quantity:
        raise HTTPException(
          status_code=400,
          detail="Insufficient stock"
        )
      
      line_total = item.quantity * item.unit_price
      total_amount += line_total

      sale_item = SalesItems(
        sales_id = sale.id,
        item_id = item.item_id,
        quantity = item.quantity,
        unit_price = item.unit_price,
        line_total = line_total
      )

      db.add(sale_item)

      db_item.current_stock -= item.quantity

      sale_items_response.append({
        "item_id": item.item_id,
        "quantity": item.quantity,
        "unit_price": item.unit_price,
        "line_total": line_total
      })

    sale.total_amount = total_amount

    db.commit()
    db.refresh(sale)

    return{
    "sale_id": sale.id,
    "user_id": sale.user_id,
    "total_amount": sale.total_amount,
    "items": sale_items_response
    }
  
  except Exception as e:
    logger.error(f"Sale was not added successful {str(e)}")
    raise HTTPException(
      status_code = 500,
      detail = f"An error occured while adding the sale {str(e)}"
    )
      
    