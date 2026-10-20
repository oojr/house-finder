from typing import List
from pydantic import BaseModel, Field

class Listing(BaseModel):
    id: str
    source: str
    address: str
    city: str
    state: str
    zip: str
    price: float
    bedrooms: float
    bathrooms: float
    sqft: float
    latitude: float
    longitude: float
    listedDate: str
    status: str
    description: str

class ScoredListing(Listing):
    relevanceScore: float = Field(..., alias="relevanceScore")

    class Config:
        populate_by_name = True

class PaginatedResponse(BaseModel):
    results: List[ScoredListing]
    page: int
    pageSize: int = Field(..., alias="pageSize")
    totalResults: int = Field(..., alias="totalResults")
    totalPages: int = Field(..., alias="totalPages")

    class Config:
        populate_by_name = True
