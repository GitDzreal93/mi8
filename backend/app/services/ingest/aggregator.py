import asyncio
from datetime import datetime
from typing import List, Callable
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import RawItemIn
from ...models import RawItem, Event, Alert
from ...config import settings
from ..deepseek import call_deepseek
from ..dedup import hash_record
from ..quota import can_fetch_source, increment_source_usage
from ..source_health import update_source_status
from ..alerts import alert_service
from .gnews import fetch_gnews
from .newsapi import fetch_newsapi
from .acled import fetch_acled
from .rsshub import fetch_rsshub

FetchFn = Callable[[], asyncio.Future]

SOURCES = {
    "gnews": fetch_gnews,
    "newsapi": fetch_newsapi,
    "acled": fetch_acled,
    "rsshub": fetch_rsshub,
}

async def run_ingest(session: AsyncSession):
    tasks = []
    for name, fn in SOURCES.items():
        if await can_fetch_source(session, name):
            tasks.append(_fetch_with_status(session, name, fn))
        else:
            await update_source_status(session, name, "skipped", "quota limit")

    results = await asyncio.gather(*tasks, return_exceptions=True)
    all_items: List[RawItemIn] = []
    for r in results:
        if isinstance(r, Exception):
            continue
        all_items.extend(r)

    for item in all_items:
        hash_key = hash_record(item.title, item.source, item.published_at.isoformat() if item.published_at else None)
        exists = await session.scalar(select(RawItem).where(RawItem.hash_key == hash_key))
        if exists:
            continue
        raw = RawItem(
            source=item.source,
            source_id=item.source_id,
            title=item.title,
            url=item.url,
            published_at=item.published_at,
            content=item.content,
            raw=item.raw,
            hash_key=hash_key,
        )
        session.add(raw)
        await session.flush()

        event_payload = await to_event(item, hash_key)
        if isinstance(event_payload.get("event_time"), str):
            try:
                event_payload["event_time"] = datetime.fromisoformat(event_payload["event_time"])
            except Exception:
                event_payload["event_time"] = item.published_at
        event = Event(**event_payload, raw_id=raw.id)
        session.add(event)
        await session.flush()

        # Check if alert should be sent
        importance = event_payload.get("importance", 0)
        if importance >= settings.alert_min_importance:
            await _create_alert(session, event, event_payload)

    await session.commit()


async def _create_alert(session: AsyncSession, event: Event, event_payload: dict):
    """Create an alert record and attempt to send notifications."""
    alert = Alert(
        event_id=event.id,
        channel="email",
        payload={"importance": event.importance, "event_type": event.event_type}
    )
    session.add(alert)

    try:
        event_data = {
            "title": event.title,
            "importance": event.importance,
            "event_type": event.event_type,
            "summary_en": event.summary_en,
            "summary_zh": event.summary_zh,
            "location_lat": event.location_lat,
            "location_lng": event.location_lng,
            "event_time": event.event_time.isoformat() if event.event_time else None,
            "actors": event.actors,
            "equipment": event.equipment,
        }
        success = await alert_service.send_event_alert(event_data)
        if success:
            alert.sent = True
    except Exception as e:
        print(f"Failed to send alert: {e}")


async def _fetch_with_status(session: AsyncSession, name: str, fn: FetchFn):
    try:
        items = await fn()
        await increment_source_usage(session, name, 1)
        await update_source_status(session, name, "ok", f"items={len(items)}")
        return items
    except Exception as e:
        await update_source_status(session, name, "error", str(e))
        return []


async def to_event(item: RawItemIn, hash_key: str):
    schema = {
        "type": "object",
        "properties": {
            "event_type": {"type": "string"},
            "importance": {"type": "integer"},
            "location_lat": {"type": "number"},
            "location_lng": {"type": "number"},
            "geo_precision": {"type": "string"},
            "actors": {"type": "array", "items": {"type": "string"}},
            "equipment": {"type": "array", "items": {"type": "string"}},
            "casualties": {"type": "object"},
            "tags": {"type": "array", "items": {"type": "string"}},
            "summary_en": {"type": "string"},
            "summary_zh": {"type": "string"},
            "event_time": {"type": "string"},
            "confidence": {"type": "number"}
        },
        "required": ["event_type", "importance"],
    }

    prompt = (
        "根据以下新闻，提取军事事件关键信息，返回 JSON。字段: "
        "event_type, importance(1-5), location_lat, location_lng, geo_precision, actors, equipment, casualties, tags, summary_en, summary_zh, event_time(ISO8601), confidence(0-1).\n"
        f"Title: {item.title}\nContent: {item.content}"
    )
    try:
        parsed = await call_deepseek(prompt, schema)
    except Exception:
        parsed = {
            "event_type": "unknown",
            "importance": 1,
            "location_lat": None,
            "location_lng": None,
            "geo_precision": None,
            "actors": [],
            "equipment": [],
            "casualties": None,
            "tags": [],
            "summary_en": item.content or item.title,
            "summary_zh": item.content or item.title,
            "event_time": item.published_at.isoformat() if item.published_at else None,
            "confidence": 0.3,
        }
    parsed["source"] = item.source
    parsed["title"] = item.title
    parsed["canonical_event_id"] = hash_key
    return parsed
