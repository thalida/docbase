<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'

import { ROUTES } from '@/router'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import AppMain from '@/components/layout/AppMain.vue'
import UserProfileDialog from '@/components/dialogs/UserProfileDialog.vue'
import { useDatabasesStore } from '@/stores/databases'
import { useRealtimeStore } from '@/stores/realtime'
import { useWorkspacesStore } from '@/stores/workspaces'
import { useWorkspaceInvitationsStore } from '@/stores/workspaceInvitations'
import { useUsersStore } from '@/stores/users'

const props = defineProps<{
  showUserProfile: boolean
  profileForUser?: string
}>()

const route = useRoute()
const router = useRouter()
const realtimeStore = useRealtimeStore()
const databasesStore = useDatabasesStore()
const workspacesStore = useWorkspacesStore()
const workspaceInvitationsStore = useWorkspaceInvitationsStore()
const usersStore = useUsersStore()

const currentWorkspaceId = ref<string | null | undefined>(
  route.params.workspaceId as string | null | undefined
)
const showUserProfile = ref(props.showUserProfile)
const userProfileId = ref(props.profileForUser === 'me' ? usersStore.me?.id : props.profileForUser)

watch(
  () => route.params.workspaceId as string,
  (workspaceId) => fetchData(workspaceId),
  { immediate: true }
)

watch(
  () => props.showUserProfile,
  (val) => {
    showUserProfile.value = val
  },
  { immediate: true }
)

watch(
  () => props.profileForUser,
  (val) => {
    userProfileId.value = val === 'me' ? usersStore.me?.id : val
  },
  { immediate: true }
)

async function fetchData(workspaceId: string) {
  currentWorkspaceId.value = workspaceId
  try {
    await workspacesStore.fetch(currentWorkspaceId.value)
  } catch (e) {
    router.replace({ name: ROUTES.INDEX })
  }

  databasesStore.fetchAll({
    workspace: currentWorkspaceId.value
  })

  usersStore.fetchAll({
    workspace: currentWorkspaceId.value
  })

  workspaceInvitationsStore.fetchAll({
    workspace: currentWorkspaceId.value
  })
}

onMounted(async () => {
  const currentWorkspaceId = route.params.workspaceId as string
  const currentDatabaseId = route.params.databaseId as string
  await realtimeStore.enterSpace(currentWorkspaceId)
  if (currentDatabaseId) {
    realtimeStore.setSpaceLocation(currentWorkspaceId, { databaseId: currentDatabaseId })
  }
})

onBeforeRouteUpdate(async (to, from) => {
  const toWorkspaceId = to.params.workspaceId as string
  const fromWorkspaceId = from.params.workspaceId as string

  const toDatabaseId = to.params.databaseId
  const fromDatabaseId = from.params.databaseId

  const isSameWorkspace = toWorkspaceId === fromWorkspaceId
  const isSameDatabase = toDatabaseId === fromDatabaseId

  if (!isSameWorkspace) {
    await realtimeStore.enterSpace(toWorkspaceId)
    realtimeStore.leaveSpace(fromWorkspaceId)
  }

  if (!isSameDatabase) {
    realtimeStore.setSpaceLocation(toWorkspaceId, { databaseId: toDatabaseId })
  }
})
</script>

<template>
  <div class="flex flex-row items-stretch h-full w-full md:p-4">
    <AppSidebar />
    <AppMain>
      <slot />
    </AppMain>
    <UserProfileDialog
      v-model:visible="showUserProfile"
      @update:visible="(state) => (showUserProfile = state)"
      :userId="userProfileId"
    />
  </div>
</template>
