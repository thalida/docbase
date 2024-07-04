import type { IFieldWithResponse } from './fields'

export interface IPage {
  id: string
  created_at: string
  updated_at: string
  created_by: string
  updated_by: string

  database: string
  title: string
  content: string
  attachments: string[]
  fields: IFieldWithResponse[]
}

export interface IPageCreateRequest {
  database: string
  title: string
  content?: string
}

export interface IPageUpdateRequest {
  id: string
  title?: string
  content?: string
}
