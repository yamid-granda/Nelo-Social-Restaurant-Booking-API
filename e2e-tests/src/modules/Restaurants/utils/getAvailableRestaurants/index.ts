import RESTAURANTS from '@api/restaurants/fixtures/initial-data.json'
import type { IAvailableRestaurant } from '../../types'
import { getTablesByRestaurantId } from '@/modules/Tables/utils/getTablesByRestaurantId'

interface IGetRestaurantsFromInitialDataConfig {
  names: string[]
  capacity?: number
}

export function getAvailableRestaurants({
  names,
  capacity,
}: IGetRestaurantsFromInitialDataConfig): IAvailableRestaurant[] {
  const capacityConfig = capacity ?? 1

  return RESTAURANTS.reduce((availableRestaurants, restaurant) => {
    if (!names.includes(restaurant.fields.name))
      return availableRestaurants

    const tables = getTablesByRestaurantId({
      restaurantId: restaurant.pk,
      capacity: capacityConfig,
    })

    availableRestaurants.push({
      id: restaurant.pk,
      created_at: restaurant.fields.created_at,
      name: restaurant.fields.name,
      tables,
    })

    return availableRestaurants
  }, [] as IAvailableRestaurant[])
}
