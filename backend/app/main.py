"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db, close_db
from app.api.routes import events, health, feedback, heatmap, auth, admin, raw_items
from app.api.v1 import api_router as v1_router
from app.services.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    await init_db()
    start_scheduler()
    yield
    await close_db()


app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
    description="Military Intelligence Dashboard API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Legacy routes (api/routes/)
app.include_router(health.router)
app.include_router(events.router)
app.include_router(feedback.router)
app.include_router(heatmap.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(raw_items.router)

# API v1 routes
app.include_router(v1_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    """Root endpoint with application info."""
    return {
        "name": settings.app_name,
        "version": "0.2.0",
        "environment": settings.environment,
        "docs": "/docs",
        "redoc": "/redoc",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
