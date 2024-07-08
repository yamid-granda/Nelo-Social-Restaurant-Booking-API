import type { IApiConfig } from '@/types'

const RESTAURANTS_URL = '/restaurants/api/v1/restaurants'

export const SEARCH_RESTAURANTS_API_CONFIG: IApiConfig = {
  url: RESTAURANTS_URL,
  method: 'get',
  path: 'search',
}
