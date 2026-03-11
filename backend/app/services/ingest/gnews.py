from datetime import datetime
from typing import List
from .base import fetch_json
from app.core.config import settings
from app.schemas.source import RawItemIn

BASE = "https://gnews.io/api/v4/search"

async def fetch_gnews() -> List[RawItemIn]:
    if not settings.gnews_api_key:
        return []
    params = {
        "q": "(Military OR Defense OR \"Arms Race\")",
        "lang": "en",
        "max": 100,
        "token": settings.gnews_api_key,
        "sortby": "publishedAt",
    }
    data = await fetch_json(BASE, params)
    items = []
    for a in data.get("articles", []):
        items.append(
            RawItemIn(
                source="gnews",
                source_id=a.get("url"),
                title=a.get("title", ""),
                url=a.get("url"),
                published_at=datetime.fromisoformat(a.get("publishedAt")) if a.get("publishedAt") else None,
                content=a.get("description"),
                raw=a,
            )
        )
    return items
