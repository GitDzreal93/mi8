from datetime import datetime
from typing import List
from .base import fetch_json
from ...config import settings
from ...schemas import RawItemIn

BASE = "https://newsapi.org/v2/everything"

async def fetch_newsapi() -> List[RawItemIn]:
    if not settings.newsapi_api_key:
        return []
    params = {
        "q": "(military OR defense OR conflict)",
        "language": "en",
        "pageSize": 100,
        "sortBy": "publishedAt",
        "apiKey": settings.newsapi_api_key,
    }
    data = await fetch_json(BASE, params)
    items = []
    for a in data.get("articles", []):
        items.append(
            RawItemIn(
                source="newsapi",
                source_id=a.get("url"),
                title=a.get("title", ""),
                url=a.get("url"),
                published_at=datetime.fromisoformat(a.get("publishedAt")) if a.get("publishedAt") else None,
                content=a.get("description"),
                raw=a,
            )
        )
    return items
