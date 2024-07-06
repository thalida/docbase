import type { AxiosResponse } from 'axios'
import client from '../clients'
import type {
  IWorkspace,
  IWorkspaceCreateRequest,
  IWorkspaceUpdateRequest
} from '@/types/workspaces'

export function list() {
  return client.get<IWorkspace[]>('/workspaces/')
}

export function retrieve(id: string) {
  return client.get<IWorkspace>(`/workspaces/${id}/`)
}

export function create(data: IWorkspaceCreateRequest) {
  return client.post<IWorkspaceCreateRequest, AxiosResponse<IWorkspace>>('/workspaces/', data)
}

export function update(id: string, data: IWorkspaceUpdateRequest) {
  return client.patch<IWorkspaceUpdateRequest, AxiosResponse<IWorkspace>>(
    `/workspaces/${id}/`,
    data
  )
}

export function destroy(id: string) {
  return client.delete(`/workspaces/${id}/`)
}

export default {
  list,
  retrieve,
  create,
  update,
  destroy
}
