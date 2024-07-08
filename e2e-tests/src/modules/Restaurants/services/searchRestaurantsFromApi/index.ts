import type { APIRequestContext } from '@playwright/test'
import { SEARCH_RESTAURANTS_API_CONFIG } from '../../configs'
import type { IRestaurantAvailability } from '../../types'
import { httpRequest } from '@/clients/http'

interface ISearchRestaurantsConfig {
  request: APIRequestContext
  capacity?: number
  dateTime?: string
  dietIds?: string[]
}

export async function searchRestaurantsFromApi({
  request,
  capacity,
  dateTime,
  dietIds,
}: ISearchRestaurantsConfig) {
  return httpRequest<IRestaurantAvailability[]>({
    request,
    ...SEARCH_RESTAURANTS_API_CONFIG,
    searchParams: {
      capacity,
      datetime: dateTime,
      diet_ids: dietIds?.join(','),
    },
  })
}
