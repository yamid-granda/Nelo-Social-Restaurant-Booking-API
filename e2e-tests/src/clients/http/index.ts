import { request } from '@playwright/test'
import type { IApiConfig, IApiMetadata, IApiResponse } from '@/types'

interface IHttpRequestConfig extends IApiConfig {}

export async function httpRequest<IResult>({
  url,
  method,
  path,
  searchParams,
  body,
}: IHttpRequestConfig): Promise<IApiResponse<IResult>> {
  let requestUrl = url

  if (path)
    requestUrl = `${url}${path}/`

  if (searchParams) {
    const stringSearchParams = Object
      .entries(searchParams)
      .reduce(
        (acc, [key, value]) => {
          if (value)
            acc[key] = String(value)

          return acc
        },
        {} as Record<string, string>,
      )

    const searchParamsString = new URLSearchParams(stringSearchParams).toString()
    requestUrl = `${requestUrl}?${searchParamsString}`
  }

  let result = {} as IResult
  let metadata = {} as IApiMetadata
  let status = 0

  try {
    const requestContext = await request.newContext()
    const requestResponse = await requestContext[method](requestUrl, { data: body })
    status = requestResponse?.status()
    const jsonResponse = await requestResponse?.json()

    result = jsonResponse

    if (jsonResponse.results) {
      const { results, ...rest } = jsonResponse
      result = results
      metadata = rest
    }

    return { result, status, metadata }
  }

  catch {
    return { result, status, metadata }
  }
}
