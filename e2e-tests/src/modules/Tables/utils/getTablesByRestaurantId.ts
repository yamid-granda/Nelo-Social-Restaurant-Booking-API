import TABLES from '@api/tables/fixtures/initial-data.json'
import type { IAvailableTable } from '../types'

interface IGetTablesByRestaurantIdConfig {
  restaurantId: string
  capacity?: number
}

export function getTablesByRestaurantId({
  restaurantId,
  capacity,
}: IGetTablesByRestaurantIdConfig): IAvailableTable[] {
  const capacityConfig = capacity ?? 1

  return TABLES.reduce((tables, table) => {
    const isInFilter = table.fields.restaurant_id === restaurantId
      && table.fields.capacity >= capacityConfig

    if (!isInFilter)
      return tables

    tables.push({
      id: table.pk,
      name: table.fields.name,
      capacity: table.fields.capacity,
    })

    return tables
  }, [] as IAvailableTable[])
}
