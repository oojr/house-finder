def test_get_listings_default(client):
    response = client.get("/api/listings")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "totalResults" in data
    assert "totalPages" in data
    assert data["pageSize"] == 4

def test_min_price_gt_max_price(client):
    response = client.get("/api/listings?min_price=500000&max_price=400000")
    assert response.status_code == 400
    assert "min_price cannot be greater than max_price" in response.json()["detail"]

def test_invalid_query_params_validation(client):
    response = client.get("/api/listings?page_size=0")
    assert response.status_code == 422

    response = client.get("/api/listings?page=0")
    assert response.status_code == 422

def test_unknown_city(client):
    response = client.get("/api/listings?city=Atlantis")
    assert response.status_code == 200
    data = response.json()
    assert data["results"] == []
    assert data["totalResults"] == 0
    assert data["totalPages"] == 0

def test_get_cities(client):
    response = client.get("/api/cities")
    assert response.status_code == 200
    cities = response.json()
    assert isinstance(cities, list)
    assert "Springfield" in cities
    assert "Fairfax" in cities
    assert cities == sorted(cities)
