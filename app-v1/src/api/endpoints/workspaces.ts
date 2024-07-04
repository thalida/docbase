import client from '../clients'
import type { IWorkspace } from '@/types/workspaces'

export function list() {
  return client.get<IWorkspace[]>('/workspaces/')
}

export function retrieve(id: string) {
  return client.get<IWorkspace>(`/workspaces/${id}/`)
}

export default {
  list,
  retrieve
}
