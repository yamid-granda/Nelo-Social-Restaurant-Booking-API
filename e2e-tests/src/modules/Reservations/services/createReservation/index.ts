import { CREATE_RESERVATION_API_CONFIG } from '../../configs'
import type { ICreateReservationBody, IReservation } from '../../types'
import { httpRequest } from '@/clients/http'

interface ICreateReservationConfig {
  body: ICreateReservationBody
}

export async function createReservation({
  body,
}: ICreateReservationConfig) {
  return httpRequest<IReservation>({
    ...CREATE_RESERVATION_API_CONFIG,
    body,
  })
}
