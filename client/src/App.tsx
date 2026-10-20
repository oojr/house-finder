import { useState, useEffect } from 'react'
import './App.css'
import { useListings } from './hooks/useListings'
import { useDebounce } from './utils/debounce'

const PAGE_SIZE = 4

export default function App() {
  const [targetBudget, setTargetBudget] = useState<string>('500000')
  const [minPrice, setMinPrice] = useState<string>('')
  const [maxPrice, setMaxPrice] = useState<string>('')
  const [minBedrooms, setMinBedrooms] = useState<string>('')
  const [city, setCity] = useState<string>('')
  const [keyword, setKeyword] = useState<string>('')
  const [page, setPage] = useState<number>(1)
  const [prevFilterKey, setPrevFilterKey] = useState<string>('')

  const [citiesList, setCitiesList] = useState<string[]>( [])

  // Debounce inputs
  const debouncedTargetBudget = useDebounce(targetBudget, 300)
  const debouncedMinPrice = useDebounce(minPrice, 300)
  const debouncedMaxPrice = useDebounce(maxPrice, 300)
  const debouncedKeyword = useDebounce(keyword, 300)

  // Client-side validation before fetching
  const minNum = debouncedMinPrice !== '' ? Number(debouncedMinPrice) : null
  const maxNum = debouncedMaxPrice !== '' ? Number(debouncedMaxPrice) : null
  const budgetNum = debouncedTargetBudget !== '' ? Number(debouncedTargetBudget) : null

  const isMinMaxInvalid = minNum !== null && maxNum !== null && minNum > maxNum
  const isBudgetInvalid = budgetNum !== null && budgetNum <= 0
  const validationError = isMinMaxInvalid
    ? 'Min price cannot be greater than max price.'
    : isBudgetInvalid
    ? 'Target budget must be greater than 0.'
    : null

  const fetchEnabled = !validationError

  // Fetch cities list on mount
  useEffect(() => {
    fetch('/api/cities')
      .then((res) => (res.ok ? res.json() : []))
      .then((list) => setCitiesList(list))
      .catch(() => setCitiesList([]))
  }, [])

  const filterKey = JSON.stringify([debouncedTargetBudget, debouncedMinPrice, debouncedMaxPrice, minBedrooms, city, debouncedKeyword])
  if (filterKey !== prevFilterKey) {
    setPrevFilterKey(filterKey)
    setPage(1)
  }

  const { data, loading, error } = useListings({
    minPrice: debouncedMinPrice,
    maxPrice: debouncedMaxPrice,
    minBedrooms,
    city,
    keyword: debouncedKeyword,
    targetBudget: debouncedTargetBudget,
    page,
    pageSize: PAGE_SIZE,
    enabled: fetchEnabled,
  })

  const handleResetFilters = () => {
    setTargetBudget('500000')
    setMinPrice('')
    setMaxPrice('')
    setMinBedrooms('')
    setCity('')
    setKeyword('')
    setPage(1)
  }

  const isFiltered =
    minPrice !== '' ||
    maxPrice !== '' ||
    minBedrooms !== '' ||
    city !== '' ||
    keyword !== '' ||
    targetBudget !== '500000'

  const formatCurrency = (val: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0,
    }).format(val)
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="brand">
          <span className="brand-icon">🏠</span>
          <div>
            <h1>HouseFinder</h1>
            <p className="subtitle">Discover your perfect home in Northern Virginia</p>
          </div>
        </div>
      </header>

      <main className="main-content">
        <section className="filter-panel" aria-label="Search and filter listings">
          <div className="filter-panel-header">
            <h2>Search & Filter</h2>
            {isFiltered && (
              <button className="btn-reset" onClick={handleResetFilters}>
                Clear Filters
              </button>
            )}
          </div>

          {validationError && (
            <div className="validation-alert" role="alert">
              ⚠️ {validationError}
            </div>
          )}

          <div className="filter-grid">
            <div className="filter-group full-width">
              <label htmlFor="keyword-input">Description Keyword</label>
              <div className="input-wrapper">
                <span className="input-icon">🔍</span>
                <input
                  id="keyword-input"
                  type="text"
                  placeholder="e.g. condo, pets, kitchen, pool, metro..."
                  value={keyword}
                  onChange={(e) => setKeyword(e.target.value)
                }
                />
                {keyword && (
                  <button
                    type="button"
                    className="clear-field-btn"
                    onClick={() => setKeyword('')}
                    aria-label="Clear keyword"
                  >
                    ✕
                  </button>
                )}
              </div>
            </div>

            <div className="filter-group">
              <label htmlFor="city-select">City</label>
              <select
                id="city-select"
                value={city}
                onChange={(e) => setCity(e.target.value)}
              >
                <option value="">All Cities</option>
                {citiesList.map((cityName) => (
                  <option key={cityName} value={cityName}>
                    {cityName}
                  </option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="min-bedrooms">Min Bedrooms</label>
              <select
                id="min-bedrooms"
                value={minBedrooms}
                onChange={(e) => setMinBedrooms(e.target.value)}
              >
                <option value="">Any</option>
                <option value="1">1+ Bed</option>
                <option value="2">2+ Beds</option>
                <option value="3">3+ Beds</option>
                <option value="4">4+ Beds</option>
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="target-budget">Target Budget ($)</label>
              <input
                id="target-budget"
                type="number"
                placeholder="e.g. 500000"
                min="0"
                step="10000"
                value={targetBudget}
                onChange={(e) => setTargetBudget(e.target.value)}
              />
            </div>

            <div className="filter-group">
              <label htmlFor="min-price">Min Price ($)</label>
              <input
                id="min-price"
                type="number"
                placeholder="No min"
                min="0"
                step="25000"
                value={minPrice}
                onChange={(e) => setMinPrice(e.target.value)}
              />
            </div>

            <div className="filter-group">
              <label htmlFor="max-price">Max Price ($)</label>
              <input
                id="max-price"
                type="number"
                placeholder="No max"
                min="0"
                step="25000"
                value={maxPrice}
                onChange={(e) => setMaxPrice(e.target.value)}
              />
            </div>
          </div>
        </section>

        <section className="results-section">
          <div className="results-bar">
            <div className="results-count">
              <strong>{data?.totalResults ?? 0}</strong>{' '}
              {(data?.totalResults ?? 0) === 1 ? 'property' : 'properties'} found
            </div>
          </div>

          {loading && !data && <div className="loading-state">Loading property listings...</div>}

          {error && <div className="error-state">Error: {error}</div>}

          {!loading && !error && data && data.totalResults === 0 && (
            <div className="empty-state">
              <span className="empty-icon">🔎</span>
              <h3>No properties match your criteria</h3>
              <p>Try adjusting your price range, bedrooms, city, or description keyword.</p>
              <button className="btn-primary" onClick={handleResetFilters}>
                Reset All Filters
              </button>
            </div>
          )}

          {!error && data && data.results.length > 0 && (
            <div className={`listings-grid ${loading ? 'loading-opacity' : ''}`}>
              {data.results.map((listing) => (
                <article key={listing.id} className="listing-card">
                  <div className="card-header">
                    <div className="card-price-status">
                      <span className="price">{formatCurrency(listing.price)}</span>
                      <span
                        className={`status-badge ${
                          listing.status === 'active' ? 'status-active' : 'status-pending'
                        }`}
                      >
                        {listing.status}
                      </span>
                    </div>
                    <div className="header-right-badges">
                      <span
                        className="relevance-badge"
                        title="Relevance Score calculated from Target Budget proximity (70%) and Recency (30%)"
                      >
                        🎯 {listing.relevanceScore}% Match
                      </span>
                      <span className="source-badge">{listing.source}</span>
                    </div>
                  </div>

                  <div className="card-body">
                    <h3 className="address">{listing.address}</h3>
                    <p className="location">
                      {listing.city}, {listing.state} {listing.zip}
                    </p>

                    <div className="specs-row">
                      <span className="spec-item">
                        <strong>{listing.bedrooms}</strong> Beds
                      </span>
                      <span className="spec-divider">•</span>
                      <span className="spec-item">
                        <strong>{listing.bathrooms}</strong> Baths
                      </span>
                      <span className="spec-divider">•</span>
                      <span className="spec-item">
                        <strong>{listing.sqft.toLocaleString()}</strong> sqft
                      </span>
                    </div>

                    <p className="description">{listing.description}</p>
                  </div>

                  <div className="card-footer">
                    <span className="listed-date">
                      Listed on {new Date(listing.listedDate).toLocaleDateString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric',
                      })}
                    </span>
                    <span className="listing-id">ID: {listing.id}</span>
                  </div>
                </article>
              ))}
            </div>
          )}

          {data && data.totalPages > 1 && (
            <nav className="pagination-nav" aria-label="Pagination Navigation">
              <button
                className="btn-page"
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={loading || data.page <= 1}
              >
                Previous
              </button>
              <span className="page-indicator">
                Page {data.page} of {data.totalPages}
              </span>
              <button
                className="btn-page"
                onClick={() => setPage((p) => Math.min(data.totalPages, p + 1))}
                disabled={loading || data.page >= data.totalPages}
              >
                Next
              </button>
            </nav>
          )}
        </section>
      </main>
    </div>
  )
}
