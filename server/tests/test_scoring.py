from scoring import score_listing, parse_date
from schemas import Listing
from datetime import datetime

def sample_listing(id="1", price=400000, listedDate="2026-09-01"):
    return Listing(
        id=id,
        source="MLS",
        address="1 St",
        city="City",
        state="VA",
        zip="22150",
        price=price,
        bedrooms=3,
        bathrooms=2.0,
        sqft=1000,
        latitude=38.0,
        longitude=-77.0,
        listedDate=listedDate,
        status="active",
        description="desc"
    )

def test_scoring_exact_budget_and_recency():
    newest = datetime(2026, 9, 5)
    l1 = sample_listing(id="A", price=450000, listedDate="2026-09-05")
    l2 = sample_listing(id="B", price=460000, listedDate="2026-09-05")
    score1 = score_listing(l1, target_budget=450000, newest_date=newest)
    score2 = score_listing(l2, target_budget=450000, newest_date=newest)
    assert score1 > score2
    assert 0 <= score1 <= 100
    assert 0 <= score2 <= 100

def test_scoring_fallback_no_target_budget():
    newest = datetime(2026, 9, 5)
    l1 = sample_listing(id="A", price=450000, listedDate="2026-09-05")
    l2 = sample_listing(id="B", price=450000, listedDate="2026-08-06") # 30 days old
    score1 = score_listing(l1, target_budget=None, newest_date=newest)
    score2 = score_listing(l2, target_budget=None, newest_date=newest)
    assert score1 > score2

def test_scoring_invalid_date():
    newest = datetime(2026, 9, 5)
    l1 = sample_listing(id="A", price=450000, listedDate="bad-date")
    score = score_listing(l1, target_budget=450000, newest_date=newest)
    assert score >= 0
    assert not str(score).__contains__("nan")

def test_scoring_determinism():
    newest = datetime(2026, 9, 5)
    l = sample_listing()
    s1 = score_listing(l, target_budget=400000, newest_date=newest)
    s2 = score_listing(l, target_budget=400000, newest_date=newest)
    assert s1 == s2
