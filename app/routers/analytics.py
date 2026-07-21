import math

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import RetailInventory
from app.schemas import ReorderRecommendationResponse, RetailInventoryResponse, StorePerformanceResponse, TopSellingProductResponse, WeatherImpactResponse
from app.services.analytics_service import get_low_stock, get_reorder_recommendations, get_store_performance, get_top_products, get_weather_impact

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)
@router.get(
    "/low-stock",
    response_model=list[RetailInventoryResponse]
)
def low_stock(db: Session = Depends(get_db)):
    return get_low_stock(db)


from sqlalchemy import func
from typing import Optional

@router.get(
    "/top-selling-products",
    response_model=list[TopSellingProductResponse]
)
def top_products(
    category: Optional[str] = None,
    store_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return get_top_products(db, category, store_id)


@router.get("/store-performance", response_model=list[StorePerformanceResponse])
def store_performance(
    db: Session = Depends(get_db)
):
    return get_store_performance(db)



@router.get("/weather-impact", response_model=list[WeatherImpactResponse])
def weather(
    db: Session = Depends(get_db)
):
    return get_weather_impact(db)


from sqlalchemy import and_
from decimal import Decimal
@router.get("/reorder-recommendations", response_model=list[ReorderRecommendationResponse])
def reorder(
    db: Session = Depends(get_db)
):
    return get_reorder_recommendations(db)