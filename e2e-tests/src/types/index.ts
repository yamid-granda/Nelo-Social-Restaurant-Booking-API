export interface IPublicDocument {
  id: string
  created_at: string
}

export type IApiMethod = 'get' | 'post' | 'put' | 'patch' | 'delete'

export interface IApiConfig {
  url: string
  method: IApiMethod
  path?: string
  searchParams?: Record<string, unknown>
  body?: unknown
}

export interface IApiMetadata {
  count: number
  next: string | null
  previous: string | null
}

export interface IApiResponse<IResult> {
  result: IResult
  metadata: IApiMetadata
  status: number
}

export interface IMultipleRequestResults {
  success: number
  failed: number
}
