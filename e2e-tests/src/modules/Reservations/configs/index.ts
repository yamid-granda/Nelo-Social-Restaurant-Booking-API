import type { IApiConfig } from '@/types'

const RESERVATIONS_URL = '/reservations/api/v1/reservations/'

export const CREATE_RESERVATION_API_CONFIG: IApiConfig = {
  url: RESERVATIONS_URL,
  method: 'post',
}
