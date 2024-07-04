import client from '../clients'
import type { IDatabase, IDatabaseRequestFilters } from '@/types/databases'

export function list(params: IDatabaseRequestFilters = {}) {
  return client.get<IDatabase[]>('/databases/', { params })
}

export function retrieve(id: string) {
  return client.get<IDatabase>(`/databases/${id}/`)
}

export default {
  list,
  retrieve
}
