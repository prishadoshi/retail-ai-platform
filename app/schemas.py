from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

class RetailInventoryBase(BaseModel):
    id: int
    date: date
    store_id: str
    product_id: str
    category: str
    region: str
    inventory_level: int
    units_sold: int
    units_ordered: int
    demand_forecast: float
    price: float
    discount: int
    weather_condition: str
    holiday_promotion: bool
    competitor_pricing: float
    seasonality: str


class RetailInventoryCreate(RetailInventoryBase):
    pass


# class RetailInventoryUpdate(RetailInventoryBase):
#     date: Optional[date] = None
#     store_id: Optional[str] = None
#     product_id: Optional[str] = None
#     category: Optional[str] = None
#     region: Optional[str] = None
#     inventory_level: Optional[int] = None
#     units_sold: Optional[int] = None
#     units_ordered: Optional[int] = None
#     demand_forecast: Optional[float] = None
#     price: Optional[float] = None
#     discount: Optional[int] = None
#     weather_condition: Optional[str] = None
#     holiday_promotion: Optional[bool] = None
#     competitor_pricing: Optional[float] = None
#     seasonality: Optional[str] = None


class RetailInventoryResponse(RetailInventoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TopSellingProductResponse(BaseModel):
    product_id: str
    category: str
    total_sales: int

class StorePerformanceResponse(BaseModel):
    store_id: str
    total_sales: int
    avg_inventory: float
    avg_demand: float

class WeatherImpactResponse(BaseModel):
    weather_condition: str
    average_sales: float

from pydantic import BaseModel

class ReorderRecommendationResponse(BaseModel):
    store_id: str
    product_id: str
    category: str

    inventory_level: int
    demand_forecast: float
    units_sold: int

    recommended_order_quantity: int

    priority: str

    reason: str


class AIQueryRequest(BaseModel):
    question: str


class AIQueryResponse(BaseModel):
    answer: str