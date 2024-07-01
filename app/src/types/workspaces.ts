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
}

export interface IWorkspaceCreateRequest {
  name: string
}

export interface IWorkspaceUpdateRequest {
  id: string
  name?: string
}
