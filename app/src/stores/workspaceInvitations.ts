import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/api'
import type {
  IWorkspaceInvitation,
  IWorkspaceInvitationCreateRequest,
  IWorkspaceInvitationUpdateRequest
} from '@/types/workspaceInvitations'

export const useWorkspaceInvitationsStore = defineStore('workspaceInvitations', () => {
  const collection = ref<Record<IWorkspaceInvitation['id'], IWorkspaceInvitation> | null>(null)

  const get = computed(() => (id: IWorkspaceInvitation['id']) => {
    if (collection.value === null) {
      return null
    }

    return collection.value[id] || null
  })

  async function fetch(id: IWorkspaceInvitation['id']) {
    if (collection.value === null || !collection.value[id]) {
      const { data } = await api.workspaceInvitations.retrieve(id)
      addOrUpdateItem(data)
    }
  }

  async function fetchAll(params: { workspace?: string; email?: string } = {}) {
    const { data } = await api.workspaceInvitations.list(params)
    addOrUpdateItems(data)
  }

  async function create(inputData: IWorkspaceInvitationCreateRequest) {
    const { data } = await api.workspaceInvitations.create(inputData)
    addOrUpdateItem(data)
    return data
  }

  async function update(
    id: IWorkspaceInvitation['id'],
    inputData: IWorkspaceInvitationUpdateRequest
  ) {
    const { data } = await api.workspaceInvitations.update(id, inputData)
    addOrUpdateItem(data)
    return data
  }

  async function destroy(id: IWorkspaceInvitation['id']) {
    await api.workspaceInvitations.destroy(id)

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
      {} as Record<IWorkspaceInvitation['id'], IWorkspaceInvitation>
    )
  }

  function addOrUpdateItems(workspaces: IWorkspaceInvitation[]) {
    for (const workspace of workspaces) {
      addOrUpdateItem(workspace)
    }
  }

  function addOrUpdateItem(workspace: IWorkspaceInvitation) {
    collection.value = {
      ...collection.value,
      [workspace.id]: workspace
    }
  }

  function $reset() {
    collection.value = null
  }

  return {
    // state
    collection,

    // methods
    get,
    fetch,
    fetchAll,
    create,
    update,
    destroy,

    $reset
  }
})
