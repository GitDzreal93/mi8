from datetime import datetime
from typing import List
from .base import fetch_json
from ...config import settings
from ...schemas import RawItemIn

BASE = "https://api.acleddata.com/acled/read"

async def fetch_acled() -> List[RawItemIn]:
    if not settings.acled_api_key:
        return []
    params = {
        "key": settings.acled_api_key,
        "limit": 100,
        "fields": "data_id,event_date,headline,location,latitude,longitude,notes,iso,url"
    }
    data = await fetch_json(BASE, params)
    records = data.get("data", [])
    items = []
    for r in records:
        items.append(
            RawItemIn(
                source="acled",
                source_id=str(r.get("data_id")),
                title=r.get("headline") or r.get("notes", ""),
                url=r.get("url"),
                published_at=datetime.fromisoformat(r.get("event_date")) if r.get("event_date") else None,
                content=r.get("notes"),
                raw=r,
            )
        )
    return items
