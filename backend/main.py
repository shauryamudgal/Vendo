from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.routes.stock_router import router as stock_router
from backend.routes.sales_router import router as sales_router

from backend.database.db import create_tables

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Stock Management API",
    version="1.0.0",
    description="API for testing stock-related operations (CRUD, updates, low-stock detection)."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    logger.info("Creating database tables (if not exist)...")
    create_tables()
    logger.info("Startup complete.")

app.include_router(stock_router)
app.include_router(sales_router)

@app.get("/")
def root():
    return {
        "message": "Stock Management and Sales API is running.",
        "endpoints": ["/stock", "/stock/low", "/stock/update", "/sales", "/sales/add"]
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}
