from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AIQueryRequest, AIQueryResponse

from app.services.analytics_service import (
    get_reorder_recommendations,
    get_store_performance,
    get_weather_impact,
    get_top_products,
    get_low_stock,
)

from app.services.llm import ask_llm

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


def format_data(data):
    """Convert Pydantic models / SQLAlchemy objects into dictionaries."""
    formatted = []

    for item in data[:10]:

        if hasattr(item, "model_dump"):
            formatted.append(item.model_dump())

        elif hasattr(item, "__dict__"):
            d = item.__dict__.copy()
            d.pop("_sa_instance_state", None)
            formatted.append(d)

        else:
            formatted.append(str(item))

    return formatted


@router.post(
    "/ask",
    summary="AI Retail Operations Copilot",
    description="""
Ask natural language questions about inventory.

Examples:

- What should I restock today?
- Which store needs the most attention?
- Summarize inventory health.
- How is weather affecting sales?
"""
)
def ask(
    request: AIQueryRequest,
    db: Session = Depends(get_db)
):

    question = request.question.lower()

    # -----------------------------
    # 1. Restocking Questions
    # -----------------------------
    if "restock" in question or "reorder" in question:

        reorder = format_data(
            get_reorder_recommendations(db)
        )

        prompt = f"""
You are an AI Retail Operations Copilot.

User Question:
{request.question}

Reorder Recommendation Data:

{reorder}

Instructions:

- Summarize the highest priority products.
- Group recommendations by store.
- Explain WHY each product should be reordered.
- Mention business impact.
- Recommend concrete actions.
- Do NOT invent any numbers.
"""


    # -----------------------------
    # 2. Store Attention / Risks
    # -----------------------------
    elif (
        "attention" in question
        or "risk" in question
        or "which store" in question
    ):

        low_stock = format_data(
            get_low_stock(db)
        )

        reorder = format_data(
            get_reorder_recommendations(db)
        )

        performance = format_data(
            get_store_performance(db)
        )

        prompt = f"""
You are an AI Retail Operations Copilot.

User Question:

{request.question}

Backend Analytics

======================
LOW STOCK
======================

{low_stock}

======================
REORDER RECOMMENDATIONS
======================

{reorder}

======================
STORE PERFORMANCE
======================

{performance}

Instructions:

Determine which store requires the most attention.

Provide:

1. Executive Summary

2. Highest Risk Store

3. Reasons

4. Recommended Actions

Only use the supplied data.

Do NOT invent facts.
"""


    # -----------------------------
    # 3. Inventory Health Summary
    # -----------------------------
    elif (
        "summary" in question
        or "inventory health" in question
        or "overall" in question
    ):

        low_stock = format_data(
            get_low_stock(db)
        )

        performance = format_data(
            get_store_performance(db)
        )

        weather = format_data(
            get_weather_impact(db)
        )

        prompt = f"""
You are an AI Retail Operations Copilot.

User Question:

{request.question}

Backend Analytics

======================
LOW STOCK
======================

{low_stock}

======================
STORE PERFORMANCE
======================

{performance}

======================
WEATHER IMPACT
======================

{weather}

Instructions:

Generate an inventory health report.

Include:

- Executive Summary

- Overall Inventory Health

- Potential Risks

- Weather Impact

- Recommended Actions

Keep the response concise.

Do NOT invent numbers.
"""


    # -----------------------------
    # 4. Top Selling Products
    # -----------------------------
    elif (
        "top" in question
        or "best selling" in question
    ):

        top_products = format_data(
            get_top_products(db)
        )

        prompt = f"""
You are an AI Retail Operations Copilot.

User Question:

{request.question}

Top Selling Products

{top_products}

Explain:

- Which products perform best
- Possible reasons
- Business recommendations

Only use the supplied data.
"""


    # -----------------------------
    # 5. Weather
    # -----------------------------
    elif "weather" in question:

        weather = format_data(
            get_weather_impact(db)
        )

        prompt = f"""
You are an AI Retail Operations Copilot.

User Question:

{request.question}

Weather Analytics

{weather}

Explain the impact of weather on inventory and sales.

Suggest actions for managers.

Do not invent information.
"""


    # -----------------------------
    # 6. Low Stock
    # -----------------------------
    elif "low stock" in question:

        low_stock = format_data(
            get_low_stock(db)
        )

        prompt = f"""
User Question:

{request.question}

Low Stock Data

{low_stock}

Summarize the most critical inventory shortages.

Recommend actions.

Only use the supplied data.
"""


    # -----------------------------
    # Default
    # -----------------------------
    else:

        prompt = f"""
You are an AI Retail Operations Copilot.

The user asked:

{request.question}

The question does not match a supported analytics capability.

Politely explain that the current version supports:

- Restocking recommendations
- Store attention analysis
- Inventory health summaries
- Weather impact
- Top-selling products
"""

    answer = ask_llm(prompt)

    return AIQueryResponse(answer=answer)