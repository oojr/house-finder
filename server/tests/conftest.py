import json
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from main import app
from listings import set_data_file

FIXTURE_DATA = [
    {
        "id": "T1",
        "source": "MLS_T",
        "address": "10 Test Rd",
        "city": "Springfield",
        "state": "VA",
        "zip": "22150",
        "price": 400000,
        "bedrooms": 3,
        "bathrooms": 2.0,
        "sqft": 1200,
        "latitude": 38.0,
        "longitude": -77.0,
        "listedDate": "2026-09-01",
        "status": "active",
        "description": "Charming pool and modern kitchen."
    },
    {
        "id": "T2",
        "source": "MLS_T",
        "address": "20 Test Ave",
        "city": "Fairfax",
        "state": "VA",
        "zip": "22030",
        "price": 500000,
        "bedrooms": 4,
        "bathrooms": 2.5,
        "sqft": 1800,
        "latitude": 38.1,
        "longitude": -77.1,
        "listedDate": "2026-08-15",
        "status": "active",
        "description": "Spacious yard near metro, no pets."
    },
    {
        "id": "T3",
        "source": "MLS_T",
        "address": "30 Test Blvd",
        "city": "Springfield",
        "state": "VA",
        "zip": "22150",
        "price": 450000,
        "bedrooms": 2,
        "bathrooms": 1.0,
        "sqft": 900,
        "latitude": 38.2,
        "longitude": -77.2,
        "listedDate": "2026-09-05",
        "status": "active",
        "description": "Cozy condo with pool."
    },
    {
        "id": "MALFORMED_1",
        "source": "MLS_T",
        "address": "Bad Row",
        "city": "Springfield",
        "state": "VA",
        "zip": "22150",
        "price": "not-a-number",
        "bedrooms": 3,
        "bathrooms": 1.0,
        "sqft": 900,
        "latitude": 38.2,
        "longitude": -77.2,
        "listedDate": "2026-09-05",
        "status": "active",
        "description": "Invalid price"
    }
]

@pytest.fixture(autouse=True)
def override_fixture_listings(tmp_path):
    f = tmp_path / "fixtures.json"
    f.write_text(json.dumps(FIXTURE_DATA), encoding="utf-8")
    set_data_file(f)
    yield
    set_data_file(None)

@pytest.fixture
def client():
    return TestClient(app)
