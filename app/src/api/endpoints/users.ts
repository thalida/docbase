import client from '../clients'
import type { IMyUser, IUser } from '@/types/users'

export function retrieve(id: string) {
  return client.get<IUser>(`/users/${id}/`)
}

export function retrieveMe() {
  return client.get<IMyUser>('/users/me/')
}

export function list() {
  return client.get<IUser[]>('/users/')
}

export default {
  retrieve,
  retrieveMe,
  list
}
