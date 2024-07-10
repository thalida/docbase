<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter, onBeforeRouteUpdate, onBeforeRouteLeave } from 'vue-router'
import { Dialog, DialogPanel, TransitionChild, TransitionRoot } from '@headlessui/vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'

import { ROUTES } from '@/router'
import AppHeader from '@/components/layout/AppHeader.vue'
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
const sidebarOpen = ref(false)

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
  await realtimeStore.enterSpace(currentWorkspaceId)
})

onBeforeRouteUpdate(async (to, from) => {
  const toWorkspaceId = to.params.workspaceId as string
  const fromWorkspaceId = from.params.workspaceId as string

  const toDatabaseId = to.params.databaseId
  const fromDatabaseId = from.params.databaseId

  const isSameWorkspace = toWorkspaceId === fromWorkspaceId
  const isSameDatabase = toDatabaseId === fromDatabaseId

  if (!isSameWorkspace) {
    realtimeStore.enterSpace(toWorkspaceId)
    realtimeStore.leaveSpace(fromWorkspaceId)
  }

  if (!isSameDatabase) {
    realtimeStore.setSpaceLocation(toWorkspaceId, { databaseId: toDatabaseId })
  }
})
</script>

<template>
  <div>
    <TransitionRoot as="template" :show="sidebarOpen">
      <Dialog class="relative z-50 lg:hidden" @close="sidebarOpen = false">
        <TransitionChild
          as="template"
          enter="transition-opacity ease-linear duration-300"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="transition-opacity ease-linear duration-300"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-gray-900/80" />
        </TransitionChild>

        <div class="fixed inset-0 flex">
          <TransitionChild
            as="template"
            enter="transition ease-in-out duration-300 transform"
            enter-from="-translate-x-full"
            enter-to="translate-x-0"
            leave="transition ease-in-out duration-300 transform"
            leave-from="translate-x-0"
            leave-to="-translate-x-full"
          >
            <DialogPanel class="relative mr-16 flex w-full max-w-xs flex-1">
              <TransitionChild
                as="template"
                enter="ease-in-out duration-300"
                enter-from="opacity-0"
                enter-to="opacity-100"
                leave="ease-in-out duration-300"
                leave-from="opacity-100"
                leave-to="opacity-0"
              >
                <div class="absolute left-full top-0 flex w-16 justify-center pt-5">
                  <button type="button" class="-m-2.5 p-2.5" @click="sidebarOpen = false">
                    <span class="sr-only">Close sidebar</span>
                    <XMarkIcon class="h-6 w-6 text-white" aria-hidden="true" />
                  </button>
                </div>
              </TransitionChild>
              <AppSidebar />
            </DialogPanel>
          </TransitionChild>
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- Static sidebar for desktop -->
    <div class="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-72 lg:flex-col">
      <AppSidebar />
    </div>

    <AppHeader @openSidebar="() => (sidebarOpen = true)" />

    <AppMain>
      <RouterView />
    </AppMain>
    <UserProfileDialog
      v-model:visible="showUserProfile"
      @update:visible="(state) => (showUserProfile = state)"
      :userId="userProfileId"
    />
  </div>
</template>
