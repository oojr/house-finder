from datetime import datetime
from typing import List, Optional, Tuple
from schemas import Listing, ScoredListing

BUDGET_WEIGHT = 0.7
RECENCY_WEIGHT = 0.3
RECENCY_WINDOW_DAYS = 90

def parse_date(date_str: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(date_str.strip()[:10])
    except Exception:
        return None

def budget_score(price: float, target: float) -> float:
    if target <= 0:
        return 0.0
    return max(0.0, 1.0 - abs(price - target) / target)

def recency_score(listing_date: str, newest_date: Optional[datetime]) -> float:
    if not newest_date:
        return 0.0
    dt = parse_date(listing_date)
    if not dt:
        return 0.0
    age_days = (newest_date - dt).days
    if age_days < 0:
        age_days = 0
    return max(0.0, 1.0 - age_days / RECENCY_WINDOW_DAYS)

def score_listing(
    listing: Listing,
    target_budget: Optional[float],
    newest_date: Optional[datetime]
) -> float:
    b_score = budget_score(listing.price, target_budget) if target_budget is not None else 0.0
    r_score = recency_score(listing.listedDate, newest_date)

    if target_budget is not None:
        raw = BUDGET_WEIGHT * b_score + RECENCY_WEIGHT * r_score
    else:
        raw = r_score

    return round(raw * 100, 1)
