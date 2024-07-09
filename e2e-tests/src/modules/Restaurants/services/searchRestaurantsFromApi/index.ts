import { SEARCH_RESTAURANTS_API_CONFIG } from '../../configs'
import type { IAvailableRestaurant } from '../../types'
import { httpRequest } from '@/clients/http'

interface ISearchRestaurantsConfig {
  capacity?: number
  dateTime?: string
  dietIds?: string[]
}

export async function searchRestaurantsFromApi({
  capacity,
  dateTime,
  dietIds,
}: ISearchRestaurantsConfig) {
  return httpRequest<IAvailableRestaurant[]>({
    ...SEARCH_RESTAURANTS_API_CONFIG,
    searchParams: {
      capacity,
      datetime: dateTime,
      diet_ids: dietIds?.join(','),
    },
  })
}
