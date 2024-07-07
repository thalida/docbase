import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/api'
import type { IMyUser, IUser } from '@/types/users'

export const useUsersStore = defineStore('users', () => {
  const me = ref<IMyUser | null>(null)
  const users = ref<IUser[] | null>(null)

  function get(id: IUser['id']) {
    if (users.value === null) {
      return null
    }

    return users.value.find((user) => user.id === id) || null
  }

  function getAll(excludeMe = true) {
    if (users.value === null) {
      return []
    }

    if (excludeMe) {
      return users.value.filter((user) => user.id !== me.value?.id)
    }

    return users.value
  }

  async function fetchMe() {
    if (!me.value) {
      const res = await api.users.retrieveMe()
      me.value = res.data
      users.value = users.value || []
      users.value.push(res.data)
    }

    return me.value
  }

  async function fetch(id: IUser['id']) {
    const res = await api.users.retrieve(id)
    users.value = users.value || []
    users.value.push(res.data)
    return res.data
  }

  async function fetchAll() {
    const res = await api.users.list()
    users.value = res.data
    return users.value
  }

  function $reset() {
    me.value = null
    users.value = null
  }

  return {
    me,
    fetch,
    fetchMe,
    fetchAll,
    get,
    getAll,
    $reset
  }
})
