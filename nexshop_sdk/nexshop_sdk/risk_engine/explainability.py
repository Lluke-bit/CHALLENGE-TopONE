from __future__ import annotations
from typing import Dict, List

def top_reason_codes(contributions: Dict[str, float], top_k: int = 5) -> List[Dict[str, float]]:
    """
    Retorna top_k razões com maiores magnitudes (positivas e negativas).
    """
    items = sorted(contributions.items(), key=lambda kv: abs(kv[1]), reverse=True)
    return [
        {"code": name.upper(), "contribution": round(val, 4)}
        for name, val in items[:top_k]
    ]
