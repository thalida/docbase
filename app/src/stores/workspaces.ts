import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/api'
import type { IWorkspace, IWorkspaceCreateRequest } from '@/types/workspaces'
import { useUsersStore } from './users'

export const useWorkspacesStore = defineStore('workspaces', () => {
  const usersStore = useUsersStore()
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

  const getOne = computed(() => (id: IWorkspace['id']) => {
    if (collection.value === null) {
      return null
    }

    return collection.value[id] || null
  })

  async function fetchOne(id: IWorkspace['id']) {
    if (collection.value === null || !collection.value[id]) {
      const { data: workspace } = await api.workspaces.retrieve(id)
      addOrUpdateItem(workspace)
    }
  }

  async function fetchAll() {
    const { data: workspaces } = await api.workspaces.list()
    addOrUpdateItems(workspaces)
  }

  async function createOne(data: IWorkspaceCreateRequest) {
    const { data: workspace } = await api.workspaces.create(data)
    addOrUpdateItem(workspace)
    return workspace
  }

  function addOrUpdateItems(workspaces: IWorkspace[]) {
    for (const workspace of workspaces) {
      addOrUpdateItem(workspace)
    }
  }

  function addOrUpdateItem(workspace: IWorkspace) {
    collection.value = {
      ...collection.value,
      [workspace.id]: workspace
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
    getOne,
    fetchOne,
    fetchAll,
    createOne,

    $reset
  }
})
