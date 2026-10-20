from listings import load_listings, filter_listings

def test_filter_min_max_price():
    listings = load_listings()
    res = filter_listings(listings, min_price=420000, max_price=520000)
    assert len(res) == 2
    assert {l.id for l in res} == {"T2", "T3"}

def test_filter_min_bedrooms():
    listings = load_listings()
    res = filter_listings(listings, min_bedrooms=4)
    assert len(res) == 1
    assert res[0].id == "T2"

def test_filter_city_case_insensitive():
    listings = load_listings()
    res = filter_listings(listings, city="springfield")
    assert len(res) == 2
    assert {l.id for l in res} == {"T1", "T3"}

def test_filter_keyword_case_insensitive():
    listings = load_listings()
    res = filter_listings(listings, keyword="POOL")
    assert len(res) == 2
    assert {l.id for l in res} == {"T1", "T3"}

def test_filter_no_matches():
    listings = load_listings()
    res = filter_listings(listings, city="Atlantis")
    assert len(res) == 0
