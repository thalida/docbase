export interface IWorkspace {
  id: string
  created_at: string
  updated_at: string
  created_by: string
  updated_by: string

  name: string
  owner: string
  is_owner: boolean
  members: string[]
  databases: string[]
  is_default: boolean
}

export interface IWorkspaceCreateRequest {
  name: string
  is_default?: boolean
}

export interface IWorkspaceUpdateRequest {
  name?: string
  is_default?: boolean
}
