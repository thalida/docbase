<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRoute } from 'vue-router'

import { useDatabasesStore } from '@/stores/databases'
import { useWorkspacesStore } from '@/stores/workspaces'

const route = useRoute()
const workspacesStore = useWorkspacesStore()
const databaseStore = useDatabasesStore()

const currentWorkspaceId = ref<string>(route.params.workspaceId as string)
const workspace = computed(() => workspacesStore.get(currentWorkspaceId.value))
const workspaceDBs = computed(() => databaseStore.getAllByWorkspace(currentWorkspaceId.value))

watch(
  () => route.params.workspaceId as string,
  (workspaceId) => {
    currentWorkspaceId.value = workspaceId
  },
  { immediate: true }
)
</script>

<template>
  <div>
    {{ workspace?.name }} ({{ workspace?.id }})
    <div v-for="database in workspaceDBs" :key="database.id">
      {{ database.name }}
    </div>
  </div>
</template>