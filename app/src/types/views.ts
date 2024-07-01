import type { IField } from './fields'

export enum ViewType {
  TABLE = 0,
  GRID = 10,
  LIST = 20,
  KANBAN = 30,
  CALENDAR = 40,
  META_PAGE = 110
}

export interface IView {
  id: string
  created_at: string
  updated_at: string
  created_by: string
  updated_by: string

  database: string
  label: string
  description: string
  view_type: ViewType
  fields: IField[]
  sort_by: TViewSort[]
  filter_by: any
}

export type TViewSort = [string, 'asc' | 'desc']

export interface IViewCreateRequest {
  database: string
  label: string
  description?: string
  view_type?: ViewType
  fields?: string[]
  sort_by?: TViewSort[]
  filter_by?: any
}

export interface IViewUpdateRequest {
  id: string
  label?: string
  description?: string
  view_type?: ViewType
  fields?: string[]
  sort_by?: TViewSort[]
  filter_by?: any
}
