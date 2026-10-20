import { useState, useEffect } from 'react'

export interface Listing {
  id: string
  source: string
  address: string
  city: string
  state: string
  zip: string
  price: number
  bedrooms: number
  bathrooms: number
  sqft: number
  latitude: number
  longitude: number
  listedDate: string
  status: string
  description: string
}

export interface ScoredListing extends Listing {
  relevanceScore: number
}

export interface PaginatedResponse {
  results: ScoredListing[]
  page: number
  pageSize: number
  totalResults: number
  totalPages: number
}

export function useListings(params: {
  minPrice: string
  maxPrice: string
  minBedrooms: string
  city: string
  keyword: string
  targetBudget: string
  page: number
  pageSize: number
  enabled: boolean
}) {
  const [data, setData] = useState<PaginatedResponse | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!params.enabled) {
      return
    }

    const controller = new AbortController()
    setLoading(true)
    setError(null)

    const searchParams = new URLSearchParams()
    if (params.minPrice !== '') searchParams.append('min_price', params.minPrice)
    if (params.maxPrice !== '') searchParams.append('max_price', params.maxPrice)
    if (params.minBedrooms !== '') searchParams.append('min_bedrooms', params.minBedrooms)
    if (params.city && params.city !== 'ALL' && params.city !== '') searchParams.append('city', params.city)
    if (params.keyword.trim() !== '') searchParams.append('keyword', params.keyword.trim())
    if (params.targetBudget !== '') searchParams.append('target_budget', params.targetBudget)
    searchParams.append('page', params.page.toString())
    searchParams.append('page_size', params.pageSize.toString())

    fetch(`/api/listings?${searchParams.toString()}`, { signal: controller.signal })
      .then(async (res) => {
        if (!res.ok) {
          const body = await res.json().catch(() => null)
          const detail = body?.detail || `Request failed (${res.status})`
          throw new Error(detail)
        }
        return res.json()
      })
      .then((json: PaginatedResponse) => {
        setData(json)
        setLoading(false)
      })
      .catch((err) => {
        if (err.name === 'AbortError') {
          return
        }
        setError(err.message || 'Error loading listings')
        setLoading(false)
      })

    return () => {
      controller.abort()
    }
  }, [
    params.minPrice,
    params.maxPrice,
    params.minBedrooms,
    params.city,
    params.keyword,
    params.targetBudget,
    params.page,
    params.pageSize,
    params.enabled,
  ])

  return { data, loading, error }
}
