import hashlib
from typing import Optional


def hash_record(title: str, source: str, published_at: Optional[str]) -> str:
    key = f"{source}|{published_at or ''}|{title}".encode("utf-8")
    return hashlib.sha256(key).hexdigest()


def is_near_duplicate(title: str, other_title: str, threshold: float = 0.9) -> bool:
    # simple Jaccard on words; placeholder until embeddings are enabled
    a = set(title.lower().split())
    b = set(other_title.lower().split())
    if not a or not b:
        return False
    score = len(a & b) / len(a | b)
    return score >= threshold
