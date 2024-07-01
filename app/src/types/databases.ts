export interface IDatabase {
  id: string
  created_at: string
  updated_at: string
  created_by: string
  updated_by: string

  workspace: string
  name: string
  description: string
  page_format_string: string
  views: string[]
}

export interface IDatabaseCreateRequest {
  workspace: string
  name: string
  description?: string
  page_format_string?: string
}

export interface IDatabaseUpdateRequest {
  id: string
  name?: string
  description?: string
  page_format_string?: string
}
