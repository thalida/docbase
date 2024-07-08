import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/api'
import {
  type IWorkspaceInvitation,
  type IWorkspaceInvitationCreateRequest,
  type IWorkspaceInvitationUpdateRequest
} from '@/types/workspaceInvitations'
import { useWorkspacesStore } from './workspaces'
import type { IWorkspace } from '@/types/workspaces'

export const useWorkspaceInvitationsStore = defineStore('workspaceInvitations', () => {
  const workspacesStore = useWorkspacesStore()
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

  async function accept(id: IWorkspaceInvitation['id']) {
    const { data } = await api.workspaceInvitations.accept(id)
    addOrUpdateItem(data)
    return data
  }

  async function reject(id: IWorkspaceInvitation['id']) {
    const { data } = await api.workspaceInvitations.reject(id)
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

  function addOrUpdateItems(workspaceInvitations: IWorkspaceInvitation[]) {
    for (const workspaceInvitation of workspaceInvitations) {
      addOrUpdateItem(workspaceInvitation)
    }
  }

  function addOrUpdateItem(workspaceInvitation: IWorkspaceInvitation) {
    collection.value = {
      ...collection.value,
      [workspaceInvitation.id]: workspaceInvitation
    }

    const workspace = workspacesStore.get(workspaceInvitation.workspace)
    if (!workspace) {
      return
    }

    const hasInvitation = workspace.invitations?.includes(workspaceInvitation.id)

    if (hasInvitation) {
      return
    }

    workspacesStore.addOrUpdateItem({
      id: workspaceInvitation.workspace,
      invitations: [
        ...(workspacesStore.get(workspaceInvitation.workspace)?.invitations || []),
        workspaceInvitation.id
      ]
    } as IWorkspace)
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
    accept,
    reject,

    $reset
  }
})
