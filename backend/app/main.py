import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .db import init_db
from .api.routes import events, health, feedback, heatmap, auth, admin
from .services.scheduler import start_scheduler

app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(events.router)
app.include_router(feedback.router)
app.include_router(heatmap.router)
app.include_router(auth.router)
app.include_router(admin.router)


@app.on_event("startup")
async def startup_event():
    await init_db()
    start_scheduler()


@app.get("/")
async def root():
    return {"name": settings.app_name, "env": settings.environment}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
