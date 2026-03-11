import asyncio
import json
from datetime import date, datetime
from typing import Dict, Any
import httpx
from ..config import settings

_head = {"Authorization": f"Bearer {settings.deepseek_api_key}"}
_lock = asyncio.Lock()
_last_call = 0.0
_daily_day = None
_daily_requests = 0
_daily_tokens = 0

async def _rate_limit():
    global _last_call
    min_interval = 1.0 / max(settings.deepseek_rate_limit_qps, 0.001)
    async with _lock:
        now = asyncio.get_event_loop().time()
        wait = (_last_call + min_interval) - now
        if wait > 0:
            await asyncio.sleep(wait)
        _last_call = asyncio.get_event_loop().time()


def _reset_daily_if_needed():
    global _daily_day, _daily_requests, _daily_tokens
    today = date.today()
    if _daily_day != today:
        _daily_day = today
        _daily_requests = 0
        _daily_tokens = 0


def _can_call():
    _reset_daily_if_needed()
    if settings.deepseek_daily_request_cap and _daily_requests >= settings.deepseek_daily_request_cap:
        return False
    if settings.deepseek_daily_token_cap and _daily_tokens >= settings.deepseek_daily_token_cap:
        return False
    return True


async def call_deepseek(prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
    """Call DeepSeek and coerce JSON output. Returns parsed JSON dict."""
    global _daily_requests, _daily_tokens

    if not settings.deepseek_api_key or not _can_call():
        raise RuntimeError("DeepSeek quota reached or API key missing")

    await _rate_limit()

    payload = {
        "model": settings.deepseek_model,
        "messages": [
            {"role": "system", "content": "You are an analyst. Output JSON only."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": settings.deepseek_max_tokens,
    }

    # Some providers support response_format/json_schema; keep optional
    payload["response_format"] = {"type": "json_object", "schema": schema}

    async with httpx.AsyncClient(base_url=settings.deepseek_base_url, timeout=settings.deepseek_timeout_seconds) as client:
        resp = await client.post("/v1/chat/completions", headers=_head, json=payload)
        if resp.status_code == 400:
            # retry without response_format for compatibility
            payload.pop("response_format", None)
            resp = await client.post("/v1/chat/completions", headers=_head, json=payload)
        resp.raise_for_status()
        data = resp.json()

    _daily_requests += 1
    usage = data.get("usage") or {}
    _daily_tokens += int(usage.get("total_tokens", 0))

    content = data["choices"][0]["message"]["content"]
    return json.loads(content)
