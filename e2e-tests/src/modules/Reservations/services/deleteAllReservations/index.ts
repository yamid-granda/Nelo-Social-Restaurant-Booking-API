import { DELETE_ALL_RESERVATIONS_API_CONFIG } from '../../configs'
import type { IReservation } from '../../types'
import { httpRequest } from '@/clients/http'

export async function deleteAllReservations() {
  return httpRequest<IReservation>({
    ...DELETE_ALL_RESERVATIONS_API_CONFIG,
  })
}
