from typing import List
from datetime import datetime, timedelta
from .base import fetch_json
from app.schemas.source import RawItemIn

BASE = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"  # placeholder, FIRMS has multiple formats

async def fetch_firms() -> List[RawItemIn]:
    # Placeholder: user must set actual endpoint & token
    # Return empty to avoid 403 without token
    return []
