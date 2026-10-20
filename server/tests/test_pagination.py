from pagination import paginate

def test_pagination_basic():
    items = list(range(10))
    slice_items, total, total_pages = paginate(items, page=1, page_size=4)
    assert slice_items == [0, 1, 2, 3]
    assert total == 10
    assert total_pages == 3

    slice_items2, _, _ = paginate(items, page=3, page_size=4)
    assert slice_items2 == [8, 9]

def test_pagination_beyond_end():
    items = list(range(5))
    slice_items, total, total_pages = paginate(items, page=10, page_size=4)
    assert slice_items == []
    assert total == 5
    assert total_pages == 2

def test_pagination_zero_items():
    slice_items, total, total_pages = paginate([], page=1, page_size=4)
    assert slice_items == []
    assert total == 0
    assert total_pages == 0
