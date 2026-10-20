import math
from typing import List, TypeVar

T = TypeVar("T")

def paginate(items: List[T], page: int, page_size: int) -> tuple[List[T], int, int]:
    total = len(items)
    if total == 0:
        return [], 0, 0
    total_pages = math.ceil(total / page_size)
    start = (page - 1) * page_size
    end = start + page_size
    slice_items = items[start:end]
    return slice_items, total, total_pages
