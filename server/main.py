from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from schemas import ScoredListing, PaginatedResponse
from listings import load_listings, filter_listings, newest_listed_date
from scoring import score_listing
from pagination import paginate

app = FastAPI(title="HouseFinder API", description="API serving real estate property listings with relevance scoring and pagination")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "HouseFinder API is running"}

@app.get("/api/cities", response_model=List[str])
def get_cities():
    listings = load_listings()
    city_set = {l.city for l in listings if l.city}
    return sorted(list(city_set))

def _handle_listings_query(
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    min_bedrooms: Optional[float] = Query(None, ge=0, description="Minimum bedrooms"),
    city: Optional[str] = Query(None, description="Filter by city"),
    keyword: Optional[str] = Query(None, description="Search keyword in description"),
    target_budget: Optional[float] = Query(None, gt=0, description="Target budget"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(4, ge=1, le=50, description="Page size"),
):
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(status_code=400, detail="min_price cannot be greater than max_price")

    all_listings = load_listings()
    newest = newest_listed_date(all_listings)

    filtered = filter_listings(
        all_listings,
        min_price=min_price,
        max_price=max_price,
        min_bedrooms=min_bedrooms,
        city=city,
        keyword=keyword,
    )

    scored_items: List[ScoredListing] = []
    for l in filtered:
        score = score_listing(l, target_budget=target_budget, newest_date=newest)
        scored_dict = l.model_dump()
        scored_dict["relevanceScore"] = score
        scored_items.append(ScoredListing(**scored_dict))

    # Sort with deterministic tie-breaker: key=(-relevanceScore, id)
    scored_items.sort(key=lambda x: (-x.relevanceScore, x.id))

    slice_items, total_results, total_pages = paginate(scored_items, page, page_size)

    return PaginatedResponse(
        results=slice_items,
        page=page,
        pageSize=page_size,
        totalResults=total_results,
        totalPages=total_pages,
    )

@app.get("/api/listings", response_model=PaginatedResponse)
@app.get("/listings", response_model=PaginatedResponse)
def get_listings(
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    min_bedrooms: Optional[float] = Query(None, ge=0),
    city: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    target_budget: Optional[float] = Query(None, gt=0),
    page: int = Query(1, ge=1),
    page_size: int = Query(4, ge=1, le=50),
):
    return _handle_listings_query(
        min_price=min_price,
        max_price=max_price,
        min_bedrooms=min_bedrooms,
        city=city,
        keyword=keyword,
        target_budget=target_budget,
        page=page,
        page_size=page_size,
    )
