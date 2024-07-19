<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Button from 'primevue/button'
import {
  FolderPlusIcon,
  SquaresPlusIcon,
  CheckIcon,
  ChevronUpDownIcon,
  XMarkIcon,
  Bars3Icon
} from '@heroicons/vue/24/outline'

import { ROUTES } from '@/router'
import ThemeSwitcher from '@/components/ThemeSwitcher.vue'
import UserAvatar from '@/components/ui/UserAvatar.vue'
import CreateWorkspaceDialog from '@/components/dialogs/CreateWorkspaceDialog.vue'
import EditWorkspaceDialog from '@/components/dialogs/EditWorkspaceDialog.vue'
import CreateDatabaseDialog from '@/components/dialogs/CreateDatabaseDialog.vue'
import { useUsersStore } from '@/stores/users'
import { useWorkspacesStore } from '@/stores/workspaces'
import { useDatabasesStore } from '@/stores/databases'

defineProps<{
  isSidebarOpen: boolean
}>()
const emits = defineEmits(['update:isSidebarOpen'])

const route = useRoute()
const router = useRouter()
const usersStore = useUsersStore()
const workspacesStore = useWorkspacesStore()
const databaseStore = useDatabasesStore()

const currentWorkspaceId = ref(route.params.workspaceId as string)
const currentWorkspace = computed(() => workspacesStore.get(currentWorkspaceId.value))
const workspaceDBs = computed(() => databaseStore.getAllByWorkspace(currentWorkspaceId.value))
const showCreateWorkspaceDialog = ref(false)
const showEditWorkspaceDialog = ref(false)
const showCreateDatabaseDialog = ref(false)
const workspacesMenu = ref()
const workspaceMenuItems = computed(() => {
  return workspacesStore.orderedCollection.map((workspace) => ({
    label: workspace.name,
    command: () => handleChangeWorkspace(workspace.id),
    isDefault: workspace.is_default,
    isSelected: workspace.id === currentWorkspaceId.value
  }))
})

watch(
  () => route.params.workspaceId as string,
  (workspaceId) => {
    currentWorkspaceId.value = workspaceId
  },
  { immediate: true }
)

function handleChangeWorkspace(workspaceId: string) {
  router.push({ name: ROUTES.WORKSPACE, params: { workspaceId } })
}

function handleLogout() {
  router.push({ name: ROUTES.LOGOUT })
}

function handleCreateWorkspace() {
  showCreateWorkspaceDialog.value = true
}

function handleEditWorkspace() {
  showEditWorkspaceDialog.value = true
}

function handleCreateDatabase() {
  showCreateDatabaseDialog.value = true
}

function handleGoToProfile() {
  router.replace({
    query: { profile: 'me' }
  })
}

function toggleWorkspacesMenu(event: Event) {
  workspacesMenu.value.toggle(event)
}
</script>

<template>
  <div>
    <div
      class="fixed top-0 left-0 w-full h-full md:hidden bg-slate-200/90 dark:bg-slate-800/90"
      :class="{
        block: isSidebarOpen,
        hidden: !isSidebarOpen
      }"
      @click="emits('update:isSidebarOpen', false)"
    />
    <div
      class="flex flex-col flex-shrink-0 flex-grow-0 h-full px-4 pb-2 fixed top-0 left-0 overflow-y-auto transition-[width] ease-in-out duration-150 md:relative bg-white dark:bg-gray-900"
      :class="{
        'w-72': isSidebarOpen,
        'w-14': !isSidebarOpen
      }"
    >
      <div
        class="flex justify-between py-4 shrink-0 items-center"
        :class="{
          'flex-row': isSidebarOpen,
          'flex-col-reverse': !isSidebarOpen
        }"
      >
        <div :class="{ hidden: !isSidebarOpen }">docbase</div>
        <div :class="{ hidden: isSidebarOpen }">db</div>
        <!-- <ThemeSwitcher :class="{ hidden: !isSidebarOpen }" /> -->
        <Button
          type="button"
          size="small"
          text
          :style="{
            padding: 0,
            width: '2rem',
            height: '2rem'
          }"
          @click="emits('update:isSidebarOpen', !isSidebarOpen)"
        >
          <span class="sr-only">Toggle sidebar</span>
          <Bars3Icon class="h-6 w-6" aria-hidden="true" v-if="!isSidebarOpen" />
          <XMarkIcon class="h-6 w-6" aria-hidden="true" v-else-if="isSidebarOpen" />
        </Button>
      </div>
      <nav class="flex flex-1 flex-col w-64" :class="{ hidden: !isSidebarOpen }">
        <ul role="list" class="flex flex-1 flex-col gap-y-4">
          <li>
            <Button
              type="button"
              size="normal"
              severity="secondary"
              outlined
              class="w-full"
              @click="toggleWorkspacesMenu"
              aria-haspopup="true"
              aria-controls="workspaces_menu"
            >
              <div class="flex flex-row items-center justify-between w-full flex-nowrap gap-2">
                <span class="truncate">
                  {{ currentWorkspace?.name || 'Workspaces' }}
                </span>
                <ChevronUpDownIcon class="flex-shrink-0 h-4 w-4" />
              </div>
            </Button>
            <Menu
              ref="workspacesMenu"
              id="workspaces_menu"
              :model="workspaceMenuItems"
              :popup="true"
              :pt="{
                list: {
                  class: 'max-h-64 overflow-auto max-w-80'
                }
              }"
            >
              <template #start>
                <div class="px-4 pt-3 pb-1">
                  <span class="text-sm font-semibold leading-6 text-gray-400">
                    Switch Workspace
                  </span>
                </div>
              </template>
              <template #item="{ item, props }">
                <div
                  class="flex flex-row items-center justify-between px-2 py-2 gap-2 cursor-pointer flex-nowrap"
                  v-tooltip.bottom="{
                    value: item.label,
                    showDelay: 1000,
                    pt: {
                      text: 'text-xs'
                    }
                  }"
                >
                  <div class="flex flex-row flex-shrink items-center justify-start truncate gap-2">
                    <span class="truncate">{{ item.label }}</span>
                    <Tag
                      v-if="item.isDefault"
                      value="Default"
                      severity="secondary"
                      class="flex-shrink-0"
                    />
                  </div>
                  <div class="flex flex-row items-center justify-end gap-2">
                    <CheckIcon
                      v-if="item.isSelected"
                      class="flex-shrink-0 h-5 w-5 text-green-400"
                      aria-hidden="true"
                    />
                  </div>
                </div>
              </template>
              <template #end>
                <div>
                  <div class="border-t border-gray-200 dark:border-gray-700"></div>
                  <Button
                    type="button"
                    size="small"
                    text
                    icon="pi pi-plus"
                    label="Create a workspace"
                    class="w-full"
                    @click="handleCreateWorkspace"
                  />
                </div>
              </template>
            </Menu>
          </li>
          <li>
            <RouterLink
              :to="{ name: ROUTES.WORKSPACE, params: { workspaceId: currentWorkspaceId } }"
              class="group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6"
              exactActiveClass="bg-gray-50 text-indigo-600 dark:bg-gray-800 dark:text-white"
            >
              <span>Overview</span>
            </RouterLink>
            <RouterLink
              :to="{ name: ROUTES.WORKSPACE_SETTINGS, params: { workspaceId: currentWorkspaceId } }"
              class="group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6"
              exactActiveClass="bg-gray-50 text-indigo-600 dark:bg-gray-800 dark:text-white"
            >
              <span>Settings</span>
            </RouterLink>
          </li>
          <li>
            <div class="flex flex-row justify-between items-center">
              <div class="w-full flex-grow text-sm font-semibold leading-6 text-gray-400">
                Databases
              </div>
              <Button
                icon=""
                text
                v-tooltip.right="{ value: 'Create a database', showDelay: 300, hideDelay: 300 }"
                aria-label="Create a database"
                class="w-10 h-10"
                @click="handleCreateDatabase"
              >
                <span>
                  <SquaresPlusIcon class="h-5 w-5" aria-hidden="true" />
                </span>
              </Button>
            </div>
            <ul v-if="workspaceDBs.length > 0" role="list" class="-mx-2 mt-2 space-y-1">
              <li v-for="database in workspaceDBs" :key="database.id">
                <RouterLink
                  :to="{
                    name: ROUTES.DATABASE,
                    params: { workspaceId: currentWorkspaceId, databaseId: database.id }
                  }"
                  class="group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6"
                  activeClass="bg-gray-50 text-indigo-600 dark:bg-gray-800 dark:text-white"
                >
                  <span class="truncate">{{ database.name }}</span>
                </RouterLink>
              </li>
            </ul>
            <div v-else>
              <Button
                aria-label="Create a database"
                class="w-full gap-2 mt-4"
                @click="handleCreateDatabase"
              >
                <span>
                  <SquaresPlusIcon class="h-5 w-5" aria-hidden="true" />
                </span>
                <span>Create a database</span>
              </Button>
            </div>
          </li>
          <li class="-mx-2 mt-auto">
            <div class="flex flex-row items-stretch justify-between">
              <Button
                text
                severity="secondary"
                aria-label="Your profile"
                class="flex flex-grow items-center !justify-start !px-2 text-sm font-semibold"
                @click="handleGoToProfile"
              >
                <UserAvatar :user="usersStore.me" />
                <div aria-hidden="true" class="ml-2">{{ usersStore.me?.display_name }}</div>
              </Button>
              <Button
                icon="pi pi-sign-out"
                text
                severity="danger"
                aria-label="Sign out"
                @click="handleLogout"
              />
            </div>
          </li>
        </ul>
      </nav>
      <CreateWorkspaceDialog
        v-model:visible="showCreateWorkspaceDialog"
        @update:visible="(state) => (showCreateWorkspaceDialog = state)"
      />
      <EditWorkspaceDialog
        :workspaceId="currentWorkspaceId"
        v-model:visible="showEditWorkspaceDialog"
        @update:visible="(state) => (showEditWorkspaceDialog = state)"
      />
      <CreateDatabaseDialog
        v-model:visible="showCreateDatabaseDialog"
        @update:visible="(state) => (showCreateDatabaseDialog = state)"
      />
    </div>
  </div>
</template>
