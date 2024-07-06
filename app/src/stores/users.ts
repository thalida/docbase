import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/api'
import type { IMyUser, IUser } from '@/types/users'

export const useUsersStore = defineStore('users', () => {
  const me = ref<IMyUser | null>(null)
  const users = ref<IUser[] | null>(null)

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
    }

    return me.value
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
    fetchMe,
    fetchAll,
    getAll,
    $reset
  }
})
