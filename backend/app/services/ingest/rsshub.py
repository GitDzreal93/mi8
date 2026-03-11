from typing import List
from datetime import datetime
import httpx
from app.core.config import settings
from app.schemas.source import RawItemIn

ENDPOINTS = [
    "/dod/press",  # replace with real RSSHub paths
    "/mod/press-release",
]

async def fetch_rsshub() -> List[RawItemIn]:
    items: List[RawItemIn] = []
    async with httpx.AsyncClient(timeout=20) as client:
        for ep in ENDPOINTS:
            url = settings.rsshub_base.rstrip("/") + ep
            r = await client.get(url, params={"format": "json"})
            r.raise_for_status()
            feed = r.json()
            for entry in feed.get("items", []):
                items.append(
                    RawItemIn(
                        source="rsshub",
                        source_id=entry.get("id") or entry.get("link"),
                        title=entry.get("title", ""),
                        url=entry.get("link"),
                        published_at=datetime.fromisoformat(entry.get("pubDate")) if entry.get("pubDate") else None,
                        content=entry.get("description"),
                        raw=entry,
                    )
                )
    return items
