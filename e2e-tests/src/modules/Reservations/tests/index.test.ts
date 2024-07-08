import test, { expect } from '@playwright/test'
import TABLES from '@api/tables/fixtures/initial-data.json'
import { createReservation } from '../services/createReservation'
import { searchRestaurantsFromApi } from '@/modules/Restaurants/services/searchRestaurantsFromApi'
import { DIETS_BY_NAME } from '@/modules/Diets/utils'
import { getDateDbFormatFromStrDate, getTomorrowDate } from '@/utils'

test.afterEach(async ({ request }) => {
  await request.delete('/reservations/api/v1/reservations/flush/')
})

test.only('reserve searching by datetime, diets and capacity', async ({ request }) => {
  // GIVEN
  const tomorrowDate = getTomorrowDate()
  const capacity = 4

  const searchParams = {
    dateTime: tomorrowDate,
    capacity,
    dietIds: [DIETS_BY_NAME.Vegetarian.id],
  }

  // WHEN
  const { result: availableRestaurants } = await searchRestaurantsFromApi({
    request,
    ...searchParams,
  })

  console.log({ availableRestaurants: JSON.stringify(availableRestaurants, null, 2) })

  const availableTableId = availableRestaurants[0].tables[0].id

  const { result: createResponse } = await createReservation({
    request,
    body: {
      table_id: availableTableId,
      datetime: tomorrowDate,
      made_out_to: 'Test User',
      quantity: capacity,
    },
  })

  // THEN
  const expectedDateTime = getDateDbFormatFromStrDate(tomorrowDate)

  expect(createResponse).toEqual({
    datetime: expectedDateTime,
    table_id: availableTableId,
    quantity: 4, // check this
    made_out_to: 'Test User',
    id: expect.any(String),
    created_at: expect.any(String),
  })
})

test('send 100 same concurrent reservations at the same time, create just one', async ({ request }) => {
  // GIVEN
  const tomorrowDate = new Date()
  tomorrowDate.setDate(tomorrowDate.getDate() + 1)
  const datetime = tomorrowDate.toISOString()

  const data = {
    table_id: TABLES[0].pk,
    datetime,
    made_out_to: 'Test User',
  }

  const createReservationPromises = Array
    .from({ length: 100 }, () =>
      request.post('/reservations/api/v1/reservations/', { data }))

  // WHEN
  const responses = await Promise.allSettled(createReservationPromises)

  interface IMultipleRequestResults {
    success: number
    failed: number
  }

  const results: IMultipleRequestResults = { success: 0, failed: 0 }

  for (const response of responses) {
    if (response.status === 'fulfilled' && response.value.status() === 201) {
      results.success += 1
      continue
    }

    results.failed += 1
  }

  // THEN
  expect(results).toEqual({ success: 1, failed: 99 })
})
