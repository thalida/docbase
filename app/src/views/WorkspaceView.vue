<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'

import { useUsersStore } from '@/stores/users'
import { useWorkspacesStore } from '@/stores/workspaces'
import { useDatabasesStore } from '@/stores/databases'

const route = useRoute()
const workspacesStore = useWorkspacesStore()
const databaseStore = useDatabasesStore()

const currentWorkspaceId = ref<string>(route.params.workspaceId as string)
const workspace = computed(() => workspacesStore.getOne(currentWorkspaceId.value))
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
