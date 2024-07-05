<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRoute } from 'vue-router'

import Breadcrumb from 'primevue/breadcrumb'

import { ROUTES } from '@/router'
import { useWorkspacesStore } from '@/stores/workspaces'
import { useDatabasesStore } from '@/stores/databases'

const route = useRoute()
const workspacesStore = useWorkspacesStore()
const databaseStore = useDatabasesStore()

const currentWorkspaceId = ref<string>(route.params.workspaceId as string)
const currentDatabaseId = ref<string>(route.params.databaseId as string)
const database = computed(() => databaseStore.getOne(currentDatabaseId.value))
const workspace = computed(() => {
  if (!database.value) return null
  return workspacesStore.getOne(database.value.workspace)
})

const items = computed(() => {
  return [
    {
      label: workspace.value?.name,
      route: { name: ROUTES.WORKSPACE, params: { workspaceId: currentWorkspaceId.value } },
      icon: 'pi pi-fw pi-folder'
    },
    // { label: database.value?.name, route: { name: ROUTES.DATABASE, params: { workspaceId: currentWorkspaceId.value, databaseId: currentDatabaseId.value } }, icon: 'pi pi-fw pi-table' },
    { label: database.value?.name, icon: 'pi pi-fw pi-database' }
  ]
})

watch(
  () => route.params.workspaceId as string,
  (workspaceId) => {
    currentWorkspaceId.value = workspaceId
  },
  { immediate: true }
)

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
    <!-- <Breadcrumb :model="items" class="p-0 !bg-transparent">
      <template #item="{ item, props }">
        <RouterLink v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
          <a :href="href" v-bind="props.action" @click="navigate">
            <span :class="[item.icon, 'text-color']" style="font-size:10px" />
            <span class="text-primary font-semibold text-xs">{{ item.label }}</span>
          </a>
        </RouterLink>
        <span v-else>
          <span :class="[item.icon, 'text-color']" />
          <span class="ml-2 font-semibold text-xs">{{ item.label }}</span>
        </span>
      </template>
    </Breadcrumb> -->
    <div>{{ database?.name }} ({{ database?.id }})</div>
    <div>{{ workspace?.name }} ({{ workspace?.id }})</div>
  </div>
</template>
