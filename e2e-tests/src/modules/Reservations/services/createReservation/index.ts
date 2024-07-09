import type { APIRequestContext } from '@playwright/test'
import { CREATE_RESERVATION_API_CONFIG } from '../../configs'
import type { ICreateReservationBody, IReservation } from '../../types'
import { httpRequest } from '@/clients/http'

interface ICreateReservationConfig {
  request: APIRequestContext
  body: ICreateReservationBody
}

export async function createReservation({
  request,
  body,
}: ICreateReservationConfig) {
  return httpRequest<IReservation>({
    request,
    ...CREATE_RESERVATION_API_CONFIG,
    body,
  })
}
