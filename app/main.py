from fastapi import FastAPI

from app.routers import analytics, ai

app = FastAPI()

app.include_router(
    analytics.router
)

app.include_router(ai.router)