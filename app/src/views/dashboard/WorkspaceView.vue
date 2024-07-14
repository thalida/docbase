<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import type { SpaceMember } from '@ably/spaces'

import { useDatabasesStore } from '@/stores/databases'
import { useWorkspacesStore } from '@/stores/workspaces'
import MemberAvatarStack from '@/components/realtime/MemberAvatarStack.vue'

const route = useRoute()
const workspacesStore = useWorkspacesStore()
const databaseStore = useDatabasesStore()

const currentWorkspaceId = ref<string>(route.params.workspaceId as string)
const workspace = computed(() => workspacesStore.get(currentWorkspaceId.value))
const workspaceDBs = computed(() => databaseStore.getAllByWorkspace(currentWorkspaceId.value))

const items = ref([
  {
    label: 'Update',
    icon: 'pi pi-refresh'
  },
  {
    label: 'Delete',
    icon: 'pi pi-times'
  }
])

watch(
  () => route.params.workspaceId as string,
  (workspaceId) => {
    currentWorkspaceId.value = workspaceId
  },
  { immediate: true }
)

function filterMembersByDatabase(members: SpaceMember[], databaseId: string) {
  return members.filter((member) => {
    const location = member.location
    if (!location) return false
    return (member.location as Record<string, any>).databaseId === databaseId
  })
}
</script>

<template>
  <div class="p-2">
    <div class="card">
      <Toolbar>
        <template #start>
          <Button icon="pi pi-plus" class="mr-2" severity="secondary" text />
          <Button icon="pi pi-print" class="mr-2" severity="secondary" text />
          <Button icon="pi pi-upload" severity="secondary" text />
        </template>

        <template #center>
          <IconField>
            <InputIcon>
              <i class="pi pi-search" />
            </InputIcon>
            <InputText placeholder="Search" />
          </IconField>
        </template>

        <template #end> <SplitButton label="Save" :model="items"></SplitButton></template>
      </Toolbar>
    </div>

    <MemberAvatarStack :workspaceId="currentWorkspaceId" />
    {{ workspace?.name }} ({{ workspace?.id }})

    <div class="p-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <Card v-for="database in workspaceDBs" :key="database.id">
        <template #title>
          <div class="flex flex-row justify-between items-center">
            <span>{{ database.name }}</span>
            <MemberAvatarStack
              :workspaceId="currentWorkspaceId"
              :filter="(members) => filterMembersByDatabase(members, database.id)"
            />
          </div>
        </template>
        <template #content>
          <p class="m-0">
            {{ database.description }}
          </p>
        </template>
      </Card>
    </div>
  </div>
</template>
