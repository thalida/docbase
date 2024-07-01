import client from '../clients'
import type { IMyUser, IUser } from '@/types/users'

export function fetchMe() {
  return client.get<IMyUser>('/users/me/')
}

export function fetch(id: string) {
  return client.get<IUser>(`/users/${id}/`)
}

export default {
  fetchMe,
  fetch
}
