# HouseFinder — Property Listing & Relevance Search

HouseFinder is a React + TypeScript real estate listing web application that allows buyers to search, filter, and rank property listings in Northern Virginia.

## Relevance Ranking System (`targetBudget` + Recency Scoring)

HouseFinder implements a custom composite **Relevance Scoring Model** that ranks properties by combining **Target Budget Proximity** and **Listing Recency**.

### Relevance Score Formula
$
\text{Relevance Score} = 0.60 \times S_{\text{budget}} + 0.40 \times S_{\text{recency}}
$

The composite score ranges from **0%** to **100%**, where higher scores indicate a property that better aligns with the user's budget and is freshly listed on the market.

---

### 1. Target Budget Proximity Score ($S_{\text{budget}}$) — Weight: 60%

The target budget score measures how closely a property's listing price matches the buyer's target budget ($B_{\text{target}}$):

$
\text{diffRatio} = \frac{|\text{price} - B_{\text{target}}|}{B_{\text{target}}}
$
$
S_{\text{budget}} = \max\left(0, \min\left(100, (1 - \text{diffRatio}) \times 100\right)\right)
$

- **Exact Budget Match**: If a property is priced exactly at the target budget ($500,000 against a $500,000 budget), $S_{\text{budget}} = 100\%$.
- **Price Deviation Decay**: A 10% price variance (above or below budget) results in $S_{\text{budget}} = 90\%$. A 50% deviation gives $50\%$.

---

### 2. Recency Score ($S_{\text{recency}}$) — Weight: 40%

The recency score rewards newly listed properties relative to the newest listing in the dataset ($T_{\text{max}}$):

$
\text{daysAgo} = \frac{T_{\text{max}} - T_{\text{listed}}}{1\text{ day in ms}}
$
$
S_{\text{recency}} = \max\left(0, \min\left(100, \left(1 - \frac{\text{daysAgo}}{30}\right) \times 100\right)\right)
$

- **Brand New Listings**: Properties listed on the reference day ($0$ days ago) score $100\%$.
- **Decay Rate**: Scores decay linearly over a 30-day window, reaching $0\%$ for listings older than 30 days.

---

### Scoring Example

Given a **Target Budget** of **$500,000**:

| Property | Price | Listed Date | Budget Score | Recency Score | Composite Relevance Score |
|---|---|---|---|---|---|
| **Listing A** | $500,000 | Today (0 days) | 100% | 100% | **100% Match** |
| **Listing B** | $525,000 | Today (0 days) | 95% | 100% | **97% Match** |
| **Listing C** | $500,000 | 15 days ago | 100% | 50% | **80% Match** |
| **Listing D** | $600,000 | 30 days ago | 80% | 0% | **48% Match** |

---

## Features & Capabilities

- **Target Budget Input**: Adjust target budget to re-calculate property relevance in real time.
- **Description Keyword Search**: Perform free-text searches on property descriptions (e.g. *pets*, *condo*, *kitchen*, *metro*).
- **City & Bedroom Filters**: Narrow listings by specific cities (Springfield, Fairfax, Reston, Vienna, Manassas, Chantilly) and minimum bedroom count.
- **Min / Max Price Range**: Cap minimum or maximum listing prices.
- **Multi-criteria Sorting**: Sort by Relevance (Budget & Recency), Price (Low-to-High / High-to-Low), Bedrooms, or Newest Date.
- **Visual Relevance Badges**: Visual indicator (`🎯 XX% Match`) on every property card detailing match scores.
