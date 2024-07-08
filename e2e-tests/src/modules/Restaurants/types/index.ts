import type { IPublicDocument } from '@/types'

interface IRestaurantAvailabilityTable {
  id: string
  name: string
  capacity: number
}

export interface IRestaurantAvailability extends IPublicDocument {
  name: string
  tables: IRestaurantAvailabilityTable[]
}
