import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/api'
import type { IDatabase, IDatabaseRequestFilters } from '@/types/databases'

export const useDatabasesStore = defineStore('databases', () => {
  const collection = ref<Record<IDatabase['id'], IDatabase> | null>(null)
  const byWorkspace = ref<Record<IDatabase['workspace'], IDatabase['id'][]> | null>(null)

  const get = computed(() => (id: IDatabase['id']) => {
    if (collection.value === null) {
      return null
    }

    return collection.value[id] || null
  })

  const getAllByWorkspace = computed(() => (workspaceId: IDatabase['workspace']) => {
    if (byWorkspace.value === null) {
      return []
    }

    if (
      typeof byWorkspace.value[workspaceId] === 'undefined' ||
      byWorkspace.value[workspaceId] === null
    ) {
      return []
    }

    if (collection.value === null) {
      return []
    }

    return byWorkspace.value[workspaceId]
      .map((id) => collection.value?.[id])
      .filter((item) => typeof item !== 'undefined' && item !== null) as IDatabase[]
  })

  async function fetch(id: IDatabase['id']) {
    if (collection.value === null || !collection.value[id]) {
      const { data: database } = await api.databases.retrieve(id)
      addOrUpdateItem(database)
    }
  }

  async function fetchAll(params: IDatabaseRequestFilters = {}) {
    const { data: databases } = await api.databases.list(params)
    addOrUpdateItems(databases)
  }

  function addOrUpdateItems(databases: IDatabase[]) {
    for (const database of databases) {
      addOrUpdateItem(database)
    }
  }

  function addOrUpdateItem(database: IDatabase) {
    collection.value = {
      ...collection.value,
      [database.id]: database
    }

    if (byWorkspace.value === null) {
      byWorkspace.value = {}
    }

    if (typeof byWorkspace.value[database.workspace] === 'undefined') {
      byWorkspace.value[database.workspace] = []
    }

    if (!byWorkspace.value[database.workspace].includes(database.id)) {
      byWorkspace.value[database.workspace].push(database.id)
    }
  }

  function $reset() {
    collection.value = null
    byWorkspace.value = null
  }

  return {
    collection,

    get,
    getAllByWorkspace,

    fetch,
    fetchAll,

    $reset
  }
})
