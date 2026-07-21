import math
from sqlalchemy.orm import Session

from app.models import RetailInventory
from app.schemas import ReorderRecommendationResponse

def get_low_stock(
    db: Session,
    threshold: int = 60,
):
    return (
        db.query(RetailInventory)
        .filter(RetailInventory.inventory_level < threshold)
        .all()
    )

from sqlalchemy import func
from typing import Optional
def get_top_products(
    db: Session,
    category: Optional[str] = None,
    store_id: Optional[str] = None,
):
    query = (
        db.query(
            RetailInventory.product_id,
            RetailInventory.category,
            func.sum(RetailInventory.units_sold).label("total_sales")
        )
    )
    if category:
        query = query.filter(RetailInventory.category == category)

    if store_id:
        query = query.filter(RetailInventory.store_id == store_id)

    results = (
        query
        .group_by(
            RetailInventory.product_id,
            RetailInventory.category
        )
        .order_by(
            func.sum(RetailInventory.units_sold).desc()
        )
        .limit(5)
        .all()
    )

    return results


def get_store_performance(
    db: Session
):
    results = (
        db.query(
            RetailInventory.store_id,
            func.sum(
                RetailInventory.units_sold
            ).label("total_sales"),

            func.avg(
                RetailInventory.inventory_level
            ).label("avg_inventory"),

            func.avg(
                RetailInventory.demand_forecast
            ).label("avg_demand")

        )
        .group_by(
            RetailInventory.store_id
        )
        .order_by(
            func.sum(RetailInventory.units_sold).desc()
        )
        .all()
    )
    return results

def get_weather_impact(
    db: Session
):
    results = (
        db.query(
            RetailInventory.weather_condition,

            func.avg(
                RetailInventory.units_sold
            ).label("average_sales")
        )
        .group_by(
            RetailInventory.weather_condition
        )
        .all()
    )
    return results


from sqlalchemy import and_
from decimal import Decimal
def get_reorder_recommendations(
    db: Session
):
    candidates = (
        db.query(RetailInventory)
        .filter(
            RetailInventory.inventory_level <
            RetailInventory.demand_forecast
        )
        .all()
    )
    recommendations = []

    for item in candidates:

        shortage = item.demand_forecast - item.inventory_level
        sales_factor = Decimal(item.units_sold) * Decimal("0.2")
        recommended_qty = math.ceil(shortage + sales_factor)
        recommended_qty = max(
            recommended_qty,
            10
        )
        if shortage > 50 or item.holiday_promotion:
            priority = "High"
        elif shortage > 20:
            priority = "Medium"
        else:
            priority = "Low"

        reason = []

        if item.inventory_level < item.demand_forecast:
            reason.append(
                f"Inventory ({item.inventory_level}) is below forecast ({item.demand_forecast})."
            )

        if item.holiday_promotion:
            reason.append(
                "Holiday promotion is active."
            )

        if item.discount > 20:
            reason.append(
                f"Discount of {item.discount}% may increase demand."
            )
        
        reason_text = " ".join(reason)

        recommendations.append(
            ReorderRecommendationResponse(
                store_id=item.store_id,
                product_id=item.product_id,
                category=item.category,
                inventory_level=item.inventory_level,
                demand_forecast=float(item.demand_forecast),
                units_sold=item.units_sold,
                recommended_order_quantity=recommended_qty,
                priority=priority,
                reason=reason_text
            )
        )

    recommendations.sort(
        key=lambda x: x.recommended_order_quantity,
        reverse=True
    )

    return recommendations