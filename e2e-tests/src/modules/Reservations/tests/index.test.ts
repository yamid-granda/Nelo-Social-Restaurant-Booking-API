import test, { expect } from '@playwright/test'
import TABLES from '@api/tables/fixtures/initial-data.json'
import { createReservation } from '../services/createReservation'
import { deleteAllReservations } from '../services/deleteAllReservations'
import { searchRestaurantsFromApi } from '@/modules/Restaurants/services/searchRestaurantsFromApi'
import { DIETS_BY_NAME } from '@/modules/Diets/utils'
import { getDateDbFormatFromStrDate, getTomorrowDate } from '@/utils'
import { getAvailableRestaurants } from '@/modules/Restaurants/utils/getAvailableRestaurants'
import type { IMultipleRequestResults } from '@/types'

test('search and reserve with full availability', async () => {
  // ------------------------------
  // 1. Restaurant Search
  // ------------------------------

  // GIVEN
  const tomorrowDate = getTomorrowDate()
  const capacity = 4

  const searchParams = {
    dateTime: tomorrowDate,
    capacity,
    dietIds: [DIETS_BY_NAME.Vegetarian.id],
  }

  // WHEN
  const { result: availableRestaurants } = await searchRestaurantsFromApi(searchParams)

  // THEN
  expect(availableRestaurants).toEqual(getAvailableRestaurants({
    names: ['Panadería Rosetta'],
    capacity,
  }))

  // ------------------------------
  // 2. Reservation Creation
  // ------------------------------

  // GIVEN
  const availableTableId = availableRestaurants[0].tables[0].id
  const madeOutTo = 'Test User'

  // WHEN
  const { result: createResponse } = await createReservation({
    body: {
      table_id: availableTableId,
      datetime: tomorrowDate,
      made_out_to: madeOutTo,
      quantity: capacity,
    },
  })

  // THEN
  const expectedDateTime = getDateDbFormatFromStrDate(tomorrowDate)

  expect(createResponse).toEqual({
    datetime: expectedDateTime,
    table_id: availableTableId,
    quantity: capacity,
    made_out_to: madeOutTo,
    id: expect.any(String),
    created_at: expect.any(String),
  })
})

test('availability reduction', async () => {
  const expectedResults = [7, 6, 5, 4, 3, 2, 1, 5, 4, 3, 2, 1, 7, 6, 5, 4, 3, 2, 1]
  let restaurantsLength

  for (let index = 0; index < expectedResults.length; index++) {
    // GIVEN
    const tomorrowDate = getTomorrowDate()
    const capacity = 2
    const madeOutTo = 'Test User'

    const searchParams = {
      dateTime: tomorrowDate,
      capacity,
      dietIds: [DIETS_BY_NAME['Gluten Free'].id],
    }

    const { result: availableRestaurants } = await searchRestaurantsFromApi(searchParams)

    restaurantsLength = availableRestaurants.length

    if (!restaurantsLength)
      break

    // WHEN
    const availableTables = availableRestaurants[0].tables

    await createReservation({
      body: {
        table_id: availableTables[0].id,
        datetime: tomorrowDate,
        made_out_to: madeOutTo,
        quantity: capacity,
      },
    })

    // THEN
    expect(availableTables.length).toBe(expectedResults[index])
  }
})

test('reserve 10 times at the same time', async () => {
  // GIVEN
  const tomorrowDate = getTomorrowDate()
  const requestsQuantity = 10

  const createReservationPromises = Array
    .from({ length: requestsQuantity }, () =>
      createReservation({ body: {
        datetime: tomorrowDate,
        made_out_to: 'Test User',
        quantity: 1,
        table_id: TABLES[0].pk,
      } }))

  // WHEN
  const responses = await Promise.allSettled(createReservationPromises)
  const results: IMultipleRequestResults = { success: 0, failed: 0 }

  for (const response of responses) {
    if (response.status === 'fulfilled' && response.value.status === 201) {
      results.success += 1
      continue
    }

    results.failed += 1
  }

  // THEN
  expect(results).toEqual({ success: 1, failed: requestsQuantity - 1 })
})

test.afterEach(async () => {
  await deleteAllReservations()
})
