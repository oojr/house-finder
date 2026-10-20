import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from schemas import Listing
from scoring import parse_date

DEFAULT_DATA_FILE = Path(__file__).parent / "listings.json"
_data_file_override: Optional[Path] = None
_cache: Optional[List[Listing]] = None

def set_data_file(path: Optional[Path]) -> None:
    global _data_file_override, _cache
    _data_file_override = path
    _cache = None

def _read_valid_rows(path: Path) -> List[Listing]:
    if not path.exists():
        logging.warning(f"Data file not found: {path}")
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception as e:
        logging.warning(f"Failed to parse JSON from {path}: {e}")
        return []

    listings: List[Listing] = []
    for item in raw_data:
        try:
            if not isinstance(item, dict):
                continue
            # Validate required numeric fields exist and are numeric, skipping malformed rows instead of defaulting
            if "price" not in item or not isinstance(item["price"], (int, float)) or item["price"] < 0:
                continue
            if "bedrooms" not in item or not isinstance(item["bedrooms"], (int, float)) or item["bedrooms"] < 0:
                continue
            if "id" not in item or "address" not in item or "city" not in item:
                continue

            listing = Listing(**item)
            listings.append(listing)
        except Exception:
            continue
    return listings

def load_listings() -> List[Listing]:
    global _cache
    if _cache is None:
        path = _data_file_override if _data_file_override is not None else DEFAULT_DATA_FILE
        _cache = _read_valid_rows(path)
    return _cache

def newest_listed_date(listings: List[Listing]) -> Optional[datetime]:
    newest: Optional[datetime] = None
    for l in listings:
        dt = parse_date(l.listedDate)
        if dt:
            if newest is None or dt > newest:
                newest = dt
    return newest

def filter_listings(
    listings: List[Listing],
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_bedrooms: Optional[float] = None,
    city: Optional[str] = None,
    keyword: Optional[str] = None,
) -> List[Listing]:
    result = []
    for l in listings:
        if min_price is not None and l.price < min_price:
            continue
        if max_price is not None and l.price > max_price:
            continue
        if min_bedrooms is not None and l.bedrooms < min_bedrooms:
            continue
        if city and city.strip().lower() != "all" and city.strip() != "":
            if l.city.strip().lower() != city.strip().lower():
                continue
        if keyword and keyword.strip():
            kw = keyword.strip().lower()
            if kw not in l.description.lower():
                continue
        result.append(l)
    return result
