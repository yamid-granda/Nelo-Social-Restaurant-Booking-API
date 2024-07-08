import DIETS from '@api/diets/fixtures/initial-data.json'
import type { IDiet } from '../types'

export const DIETS_BY_NAME: Record<string, IDiet> = DIETS.reduce(
  (acc, diet) => {
    acc[diet.fields.name] = {
      id: diet.pk,
      name: diet.fields.name,
      created_at: diet.fields.created_at,
    }
    return acc
  },
  {} as Record<string, IDiet>,
)
