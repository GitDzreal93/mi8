from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..db import SessionLocal
from ..config import settings
from .ingest.aggregator import run_ingest

scheduler = AsyncIOScheduler()


def start_scheduler():
    scheduler.add_job(job_wrapper, "interval", minutes=settings.poll_interval_minutes, id="ingest")
    scheduler.start()

async def job_wrapper():
    async with SessionLocal() as session:
        await run_ingest(session)

if __name__ == "__main__":
    import asyncio
    asyncio.run(job_wrapper())
