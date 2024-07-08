import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import api from '@/api'
import type { IMyUser, IUser } from '@/types/users'
import { useWorkspaceInvitationsStore } from './workspaceInvitations'
import { InvitationStatus, type IWorkspaceInvitation } from '@/types/workspaceInvitations'

export const useUsersStore = defineStore('users', () => {
  const workspaceInvitationsStore = useWorkspaceInvitationsStore()
  const me = ref<IMyUser | null>(null)
  const users = ref<IUser[] | null>(null)

  const myPendingInvitations = computed(() => {
    if (me.value === null) {
      return []
    }

    const invitations = me.value.invitations.map((invitation) =>
      workspaceInvitationsStore.get(invitation)
    )
    return invitations.filter(
      (invitation) => invitation?.status === InvitationStatus.PENDING
    ) as IWorkspaceInvitation[]
  })

  function get(id: IUser['id']) {
    if (users.value === null) {
      return null
    }

    return users.value.find((user) => user.id === id) || null
  }

  function getAll(excludeMe = false) {
    if (users.value === null) {
      return []
    }

    if (excludeMe) {
      return users.value.filter((user) => user.id !== me.value?.id)
    }

    return users.value
  }

  async function fetchMe(reset = false) {
    if (!me.value || reset) {
      const res = await api.users.retrieveMe()
      addOrUpdateItem(res.data, true)
    }

    return me.value
  }

  async function fetch(id: IUser['id']) {
    const res = await api.users.retrieve(id)
    addOrUpdateItem(res.data)
  }

  async function fetchAll(params: { workspace?: string } = {}) {
    const res = await api.users.list(params)
    addOrUpdateItems(res.data)
  }

  function addOrUpdateItem(user: IUser | IMyUser, isMe: boolean = false) {
    users.value = users.value || []
    const index = users.value.findIndex((u) => u.id === user.id)

    if (index === -1) {
      users.value.push(user)
    } else {
      users.value[index] = {
        ...users.value[index],
        ...user
      }
    }

    if (isMe || me.value?.id === user.id) {
      me.value = me.value || ({} as IMyUser)
      me.value = {
        ...me.value,
        ...user
      }
    }
  }

  function addOrUpdateItems(users: IUser[]) {
    for (const user of users) {
      addOrUpdateItem(user)
    }
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
    myPendingInvitations,
    $reset
  }
})
