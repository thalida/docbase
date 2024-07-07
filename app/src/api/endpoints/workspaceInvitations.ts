import type { AxiosResponse } from 'axios'
import client from '../clients'
import type {
  IWorkspaceInvitation,
  IWorkspaceInvitationCreateRequest,
  IWorkspaceInvitationUpdateRequest
} from '@/types/workspaceInvitations'

export function list(params: { workspace?: string; email?: string }) {
  return client.get<IWorkspaceInvitation[]>('/workspace-invitations/', { params })
}

export function retrieve(id: string) {
  return client.get<IWorkspaceInvitation>(`/workspace-invitations/${id}/`)
}

export function create(data: IWorkspaceInvitationCreateRequest) {
  return client.post<IWorkspaceInvitationCreateRequest, AxiosResponse<IWorkspaceInvitation>>(
    '/workspace-invitations/',
    data
  )
}

export function update(id: string, data: IWorkspaceInvitationUpdateRequest) {
  return client.patch<IWorkspaceInvitationUpdateRequest, AxiosResponse<IWorkspaceInvitation>>(
    `/workspace-invitations/${id}/`,
    data
  )
}

export function destroy(id: string) {
  return client.delete(`/workspace-invitations/${id}/`)
}

export default {
  list,
  retrieve,
  create,
  update,
  destroy
}
