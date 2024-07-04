import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/api'
import type { IMyUser, IUser } from '@/types/users'

export const useUsersStore = defineStore('users', () => {
  const me = ref<IMyUser | null>(null)

  async function fetchMe() {
    if (!me.value) {
      const res = await api.users.retrieveMe()
      me.value = res.data
    }

    return me.value
  }
  function $reset() {
    me.value = null
  }

  return {
    me,
    fetchMe,
    $reset
  }
})
