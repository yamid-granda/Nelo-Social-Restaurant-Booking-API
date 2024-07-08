export function getDateDbFormatFromStrDate(dateTime: string = ''): string {
  const split = dateTime.split('Z')
  return `${split[0]}000Z`
}

export function getTomorrowDate(): string {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  return tomorrow.toISOString()
}
