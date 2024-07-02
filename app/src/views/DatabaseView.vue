<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRoute } from 'vue-router'

import { useWorkspacesStore } from '@/stores/workspaces'
import { useDatabasesStore } from '@/stores/databases'

const route = useRoute()
const workspacesStore = useWorkspacesStore()
const databaseStore = useDatabasesStore()

const currentDatabaseId = ref<string>(route.params.databaseId as string)
const database = computed(() => databaseStore.getOne(currentDatabaseId.value))
const workspace = computed(() => {
  if (!database.value) return null
  return workspacesStore.getOne(database.value.workspace)
})

watch(
  () => route.params.databaseId as string,
  (databaseId) => {
    currentDatabaseId.value = databaseId
  },
  { immediate: true }
)
</script>

<template>
  <div>
    DATABASE!!
    <div>{{ database?.name }} ({{ database?.id }})</div>
    <div>{{ workspace?.name }} ({{ workspace?.id }})</div>
  </div>
</template>
