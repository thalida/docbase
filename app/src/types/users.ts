export interface IUser {
  id: string
  email: string
  first_name: string
  last_name: string
  display_name: string
  initials: string
  avatar: string
}

export interface IMyUser extends IUser {
  workspaces: string[]
  default_workspace: string | null
  invitations: string[]
}
