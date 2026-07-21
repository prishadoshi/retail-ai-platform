from sqlalchemy import Column, Integer, String, Date, Boolean, Numeric
from .database import Base

class RetailInventory(Base):
    __tablename__ = "retail_inventory"

    id = Column(Integer, primary_key=True, index=True)

    date = Column(Date)

    store_id = Column(String)

    product_id = Column(String)

    category = Column(String)

    region = Column(String)

    inventory_level = Column(Integer)

    units_sold = Column(Integer)

    units_ordered = Column(Integer)

    demand_forecast = Column(Numeric)

    price = Column(Numeric)

    discount = Column(Integer)

    weather_condition = Column(String)

    holiday_promotion = Column(Boolean)

    competitor_pricing = Column(Numeric)

    seasonality = Column(String)