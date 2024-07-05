import type { AxiosResponse } from 'axios'
import client from '../clients'
import type { IWorkspace, IWorkspaceCreateRequest } from '@/types/workspaces'

export function list() {
  return client.get<IWorkspace[]>('/workspaces/')
}

export function retrieve(id: string) {
  return client.get<IWorkspace>(`/workspaces/${id}/`)
}

export function create(data: IWorkspaceCreateRequest) {
  return client.post<IWorkspaceCreateRequest, AxiosResponse<IWorkspace>>('/workspaces/', data)
}

export default {
  create,
  list,
  retrieve
}
