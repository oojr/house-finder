# HouseFinder App - Refactored

HouseFinder is a full-stack real estate listing and discovery application with backend-driven filtering, relevance scoring, and pagination.

## Project Structure

- `server/`: Python + FastAPI backend (modular structure with schemas, scoring, pagination, listings, and pytest suite).
- `client/`: React + TypeScript + Vite frontend (thin client communicating with FastAPI via proxy).

---

## Getting Started

### 1. Backend (`server/`)

```bash
cd server
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

To run tests:

```bash
cd server
python3 -m pytest
```

### 2. Frontend (`client/`)

```bash
cd client
npm install
npm run dev
```

---

## Scoring Approach & Weights

- **Formula**: `relevanceScore = round((BUDGET_WEIGHT * budget_score + RECENCY_WEIGHT * recency_score) * 100, 1)`
- **Weights**: 70% (`BUDGET_WEIGHT = 0.7`) for budget proximity, 30% (`RECENCY_WEIGHT = 0.3`) for recency.
- **Recency Window**: 90 days (`RECENCY_WINDOW_DAYS = 90`).
- **Anchor Date**: Recency is measured against the **newest listedDate in the full dataset**, ensuring scores are deterministic, stable across filter changes, and independent of server clock execution time.
- **Fallback**: If `target_budget` is omitted, listings are ranked strictly by recency.
- **Tie-breaker**: Identical scores are deterministically ordered by `(-relevanceScore, id)`.

---

## Validation & Error Handling

- `min_price > max_price` returns HTTP `400` with detail `"min_price cannot be greater than max_price"`.
- Invalid types, negative prices, or out-of-range pagination parameters (`page_size <= 0`, `page < 1`) return HTTP `422` validation errors.
- Unknown cities or filters with no matches return HTTP `200` with an empty result list (`totalResults: 0`, `totalPages: 0`), avoiding crashes or silent errors.
- Malformed rows in `listings.json` (missing or non-numeric price/bedrooms) are safely skipped during load.
