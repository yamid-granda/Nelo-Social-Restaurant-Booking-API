import type { APIRequestContext } from '@playwright/test'
import { DELETE_ALL_RESERVATIONS_API_CONFIG } from '../../configs'
import type { ICreateReservationBody, IReservation } from '../../types'
import { httpRequest } from '@/clients/http'

interface IDeleteAllReservationsConfig {
  request: APIRequestContext
}

export async function deleteAllReservations({
  request,
}: IDeleteAllReservationsConfig) {
  return httpRequest<IReservation>({
    request,
    ...DELETE_ALL_RESERVATIONS_API_CONFIG,
  })
}
