import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/api'
import type { IUser } from '@/types/users'

export const useUsersStore = defineStore('users', () => {
  const me = ref<IUser | null>(null)

  async function fetchMe() {
    const res = await api.users.fetchMe()
    me.value = res.data
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
