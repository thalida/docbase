import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/api'
import type {
  IWorkspace,
  IWorkspaceCreateRequest,
  IWorkspaceUpdateRequest
} from '@/types/workspaces'
import { useUsersStore } from './users'
import type { IUser } from '@/types/users'
import { useWorkspaceInvitationsStore } from './workspaceInvitations'
import type { IWorkspaceInvitation } from '@/types/workspaceInvitations'

export const useWorkspacesStore = defineStore('workspaces', () => {
  const usersStore = useUsersStore()
  const workspaceInvitationsStore = useWorkspaceInvitationsStore()
  const collection = ref<Record<IWorkspace['id'], IWorkspace> | null>(null)

  const orderedCollection = computed(() => {
    if (collection.value === null) {
      return []
    }

    return Object.values(collection.value).sort((a, b) => {
      return a.name.localeCompare(b.name)
    })
  })

  const defaultWorkspace = computed(() => {
    if (collection.value === null) {
      return null
    }

    const found_default =
      Object.values(collection.value).find((workspace) => workspace.is_default) || null
    if (found_default !== null) {
      return found_default
    }

    return orderedCollection.value[0]
  })

  const get = computed(() => (id: IWorkspace['id']) => {
    if (collection.value === null) {
      return null
    }

    return collection.value[id] || null
  })

  const getMembers = computed(() => (id: IWorkspace['id']) => {
    if (collection.value === null) {
      return []
    }

    const workspace = collection.value[id]
    if (workspace === undefined) {
      return []
    }

    const sortAlphabetically = workspace.members.sort((a, b) => {
      const userA = usersStore.get(a)
      const userB = usersStore.get(b)
      if (userA && userB) {
        return userA.display_name.localeCompare(userB.display_name)
      }

      return 0
    })
    const sortedMembers = sortAlphabetically.sort((a, b) => {
      if (a === workspace.owner) {
        return -1
      }

      if (b === workspace.owner) {
        return 1
      }

      return 0
    })

    const teamMembers = sortedMembers.map((member) => usersStore.get(member))
    return teamMembers as IUser[]
  })

  const getInvitations = computed(() => (id: IWorkspace['id']) => {
    if (collection.value === null) {
      return []
    }

    const workspace = collection.value[id]
    if (workspace === undefined) {
      return []
    }

    const invitations = workspace.invitations.map((invitation) =>
      workspaceInvitationsStore.get(invitation)
    )
    return invitations as IWorkspaceInvitation[]
  })

  async function fetch(id: IWorkspace['id']) {
    if (collection.value === null || !collection.value[id]) {
      const { data: workspace } = await api.workspaces.retrieve(id)
      addOrUpdateItem(workspace)
    }
  }

  async function fetchAll() {
    const { data: workspaces } = await api.workspaces.list()
    addOrUpdateItems(workspaces)
  }

  async function create(data: IWorkspaceCreateRequest) {
    const { data: workspace } = await api.workspaces.create(data)
    addOrUpdateItem(workspace)
    return workspace
  }

  async function update(id: IWorkspace['id'], data: IWorkspaceUpdateRequest) {
    const { data: workspace } = await api.workspaces.update(id, data)
    addOrUpdateItem(workspace)
    return workspace
  }

  async function destroy(id: IWorkspace['id']) {
    await api.workspaces.destroy(id)

    if (collection.value === null) {
      return
    }

    collection.value = Object.values(collection.value).reduce(
      (acc, workspace) => {
        if (workspace.id !== id) {
          acc[workspace.id] = workspace
        }
        return acc
      },
      {} as Record<IWorkspace['id'], IWorkspace>
    )
  }

  function addOrUpdateItems(workspaces: IWorkspace[]) {
    for (const workspace of workspaces) {
      addOrUpdateItem(workspace)
    }
  }

  function addOrUpdateItem(workspace: IWorkspace) {
    collection.value = {
      ...collection.value,
      [workspace.id]: {
        ...collection.value?.[workspace.id],
        ...workspace
      }
    }

    for (const key in collection.value) {
      if (key === workspace.id) {
        continue
      }
      const otherWorkspace = collection.value[key]
      otherWorkspace.is_default = workspace.is_default ? false : otherWorkspace.is_default
    }

    const foundDefaultWorkspace = Object.values(collection.value).find(
      (workspace) => workspace.is_default
    )

    if (usersStore.me !== null) {
      usersStore.me = {
        ...usersStore.me,
        default_workspace: foundDefaultWorkspace?.id || null
      }
    }
  }

  function $reset() {
    collection.value = null
  }

  return {
    // state
    collection,

    // computed
    orderedCollection,
    defaultWorkspace,

    // methods
    get,
    getMembers,
    getInvitations,
    fetch,
    fetchAll,
    addOrUpdateItem,
    addOrUpdateItems,
    create,
    update,
    destroy,

    $reset
  }
})
