import type { IPublicDocument } from '@/types'

interface IAvailableRestaurantTable {
  id: string
  name: string
  capacity: number
}

export interface IAvailableRestaurant extends IPublicDocument {
  name: string
  tables: IAvailableRestaurantTable[]
}
