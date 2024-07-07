export enum InvitationStatus {
  PENDING = 'pending',
  ACCEPTED = 'accepted',
  REJECTED = 'rejected'
}

export interface IWorkspaceInvitation {
  id: string
  created_at: string
  updated_at: string
  created_by: string
  updated_by: string

  email: string
  workspace: string
  status: InvitationStatus
}

export interface IWorkspaceInvitationCreateRequest {
  workspace: string
  email: string
}

export interface IWorkspaceInvitationUpdateRequest {
  status: InvitationStatus
}
