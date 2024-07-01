export interface IWorkspace {
  id: string
  created_at: string
  updated_at: string
  created_by: string
  updated_by: string

  name: string
  owner: string
  members: string[]
}
