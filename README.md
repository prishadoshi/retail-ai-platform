# AI Retail Inventory Intelligence Platform

An AI-powered backend platform for retail inventory analytics and decision support.

## Features

- Inventory analytics
- Low-stock detection
- Reorder recommendations
- Store performance analysis
- Weather impact analysis
- Top-selling products
- AI Retail Copilot (Groq LLM)
- Dockerized FastAPI application

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Docker
- Groq LLM

## APIs

### Analytics

- GET /analytics/low-stock
- GET /analytics/top-selling-products
- GET /analytics/store-performance
- GET /analytics/weather-impact
- GET /analytics/reorder-recommendations

### AI

- POST /ai/ask

Example questions:

- What should I restock today?
- Which store needs the most attention?
- Summarize inventory health.
- How is weather affecting sales?

## Running

```bash
docker compose up --build
```


