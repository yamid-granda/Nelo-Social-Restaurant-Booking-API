import type { IPublicDocument } from '@/types'

export interface ICreateReservationBody {
  table_id: string
  datetime: string
  quantity: number
  made_out_to: string
}

export interface IReservation extends IPublicDocument {
  table_id: string
  datetime: string
  quantity: number
  made_out_to: string
}
