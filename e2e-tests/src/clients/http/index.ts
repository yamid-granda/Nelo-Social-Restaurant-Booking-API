import type { APIRequestContext } from '@playwright/test'
import type { IApiConfig, IApiMetadata, IApiResponse } from '@/types'

interface IHttpRequestConfig extends IApiConfig {
  request: APIRequestContext
}

export async function httpRequest<IResult>({
  request,
  url,
  method,
  path,
  searchParams,
  body,
}: IHttpRequestConfig): Promise<IApiResponse<IResult>> {
  let requestUrl = url

  if (path)
    requestUrl = `${url}/${path}/`

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

  try {
    console.log('the request url is', requestUrl)
    console.log('the method is', method)

    const requestResponse = await request[method](requestUrl, { data: body })
    const jsonResponse = await requestResponse?.json()

    result = jsonResponse

    if (jsonResponse.results) {
      const { results, ...rest } = jsonResponse
      result = results
      metadata = rest
    }

    return { result, metadata }
  }

  catch (error: any) {
    return { result, metadata }
  }
}
