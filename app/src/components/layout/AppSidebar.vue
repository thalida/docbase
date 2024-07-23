<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Button from 'primevue/button'
import {
  SquaresPlusIcon,
  Squares2X2Icon,
  Cog6ToothIcon,
  CheckCircleIcon,
  ChevronUpDownIcon,
  XMarkIcon,
  Bars3Icon
} from '@heroicons/vue/24/outline'

import { ROUTES } from '@/router'
import ThemeSwitcher from '@/components/ThemeSwitcher.vue'
import UserAvatar from '@/components/ui/UserAvatar.vue'
import CreateWorkspaceDialog from '@/components/dialogs/CreateWorkspaceDialog.vue'
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
    isSelected: workspace.id === currentWorkspaceId.value,
    workspace
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

function handleCreateWorkspace() {
  showCreateWorkspaceDialog.value = true
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
      class="flex flex-col flex-shrink-0 flex-grow-0 h-full pb-2 fixed rounded-lg top-0 left-0 overflow-y-auto transition-[width] ease-in-out duration-150 md:relative bg-white dark:bg-gray-900"
      :class="{
        'w-72 px-4': isSidebarOpen,
        'w-14 px-1': !isSidebarOpen
      }"
    >
      <div class="flex flex-col grow shrink-0 gap-4" :class="{ hidden: isSidebarOpen }">
        <div class="flex flex-col justify-between py-4 shrink-0 items-center">
          <Button
            type="button"
            size="small"
            severity="secondary"
            text
            :style="{
              padding: 0,
              width: '2rem',
              height: '2rem'
            }"
            @click="emits('update:isSidebarOpen', true)"
          >
            <span class="sr-only">Open sidebar</span>
            <Bars3Icon class="h-6 w-6" aria-hidden="true" />
          </Button>
          <div>db</div>
        </div>
        <nav class="flex flex-1 flex-col grow">
          <ul role="list" class="flex flex-1 flex-col items-center gap-y-4">
            <li>
              <RouterLink
                :to="{ name: ROUTES.WORKSPACE, params: { workspaceId: currentWorkspaceId } }"
                class=""
              >
                <WorkspaceAvatar v-if="currentWorkspace" :workspace="currentWorkspace" />
              </RouterLink>
            </li>
            <li class="flex flex-col gap-y-2">
              <RouterLink
                :to="{ name: ROUTES.WORKSPACE, params: { workspaceId: currentWorkspaceId } }"
                class="group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6"
                exactActiveClass="bg-gray-50 text-primary-600 dark:bg-gray-800"
              >
                <Squares2X2Icon class="h-6 w-6" aria-hidden="true" />
              </RouterLink>
              <RouterLink
                :to="{
                  name: ROUTES.WORKSPACE_SETTINGS,
                  params: { workspaceId: currentWorkspaceId }
                }"
                class="group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6"
                exactActiveClass="bg-gray-50 text-primary-600 dark:bg-gray-800"
              >
                <Cog6ToothIcon class="h-6 w-6" aria-hidden="true" />
              </RouterLink>
            </li>
            <li class="mt-auto flex flex-col items-center">
              <div class="flex flex-row items-stretch justify-between">
                <Button
                  rounded
                  text
                  severity="secondary"
                  aria-label="Your profile"
                  class="flex flex-grow items-center !justify-start !px-2 text-sm font-semibold"
                  @click="handleGoToProfile"
                >
                  <UserAvatar :user="usersStore.me" />
                </Button>
              </div>
              <ThemeSwitcher displayVariant="icon" />
            </li>
          </ul>
        </nav>
      </div>
      <div class="flex flex-col grow shrink-0" :class="{ hidden: !isSidebarOpen }">
        <div class="flex justify-between py-4 shrink-0 items-center">
          <div>docbase</div>
          <Button
            type="button"
            size="small"
            severity="secondary"
            text
            :style="{
              padding: 0,
              width: '2rem',
              height: '2rem'
            }"
            @click="emits('update:isSidebarOpen', false)"
          >
            <span class="sr-only">Close sidebar</span>
            <XMarkIcon class="h-6 w-6" aria-hidden="true" />
          </Button>
        </div>
        <nav class="flex flex-1 flex-col grow w-64">
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
                <div class="flex flex-row items-center justify-between w-full flex-nowrap gap-4">
                  <div class="flex flex-row items-center justify-start gap-2 truncate">
                    <WorkspaceAvatar v-if="currentWorkspace" :workspace="currentWorkspace" />
                    <span class="truncate text-color">
                      {{ currentWorkspace?.name || 'Workspaces' }}
                    </span>
                  </div>
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
                    <span class="text-sm font-semibold leading-6 text-muted-color">
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
                    <div
                      class="flex flex-row flex-shrink items-center justify-start truncate gap-2"
                    >
                      <WorkspaceAvatar :workspace="item.workspace" />
                      <span class="truncate">{{ item.label }}</span>
                      <Tag
                        v-if="item.isDefault"
                        value="Default"
                        severity="secondary"
                        class="flex-shrink-0"
                      />
                    </div>
                    <div class="flex flex-row items-center justify-end gap-2">
                      <CheckCircleIcon
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
                      text
                      label="Create a workspace"
                      class="w-full"
                      @click="handleCreateWorkspace"
                    >
                      <SquaresPlusIcon class="h-5 w-5" aria-hidden="true" />
                      <span>Create a workspace</span>
                    </Button>
                  </div>
                </template>
              </Menu>
            </li>
            <li>
              <RouterLink
                :to="{ name: ROUTES.WORKSPACE, params: { workspaceId: currentWorkspaceId } }"
                class="group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6"
                exactActiveClass="bg-gray-50 text-primary-600 dark:bg-gray-800"
              >
                <Squares2X2Icon class="h-6 w-6" aria-hidden="true" />
                <span>Overview</span>
              </RouterLink>
              <RouterLink
                :to="{
                  name: ROUTES.WORKSPACE_SETTINGS,
                  params: { workspaceId: currentWorkspaceId }
                }"
                class="group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6"
                exactActiveClass="bg-gray-50 text-primary-600 dark:bg-gray-800"
              >
                <Cog6ToothIcon class="h-6 w-6" aria-hidden="true" />
                <span>Settings</span>
              </RouterLink>
            </li>
            <li>
              <div class="flex flex-row justify-between items-center">
                <div class="w-full flex-grow text-sm font-semibold leading-6 text-muted-color">
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
                    activeClass="bg-gray-50 text-primary-600 dark:bg-gray-800"
                  >
                    <span class="truncate">{{ database.name }}</span>
                  </RouterLink>
                </li>
              </ul>
              <div v-else>
                <Button
                  aria-label="Create a database"
                  class="w-full gap-2 mt-4 p-4"
                  @click="handleCreateDatabase"
                >
                  <span>
                    <SquaresPlusIcon class="h-5 w-5" aria-hidden="true" />
                  </span>
                  <span>Create a database</span>
                </Button>
              </div>
            </li>
            <li class="mt-auto">
              <div class="flex flex-row items-center justify-between gap-2">
                <Button
                  text
                  severity="secondary"
                  aria-label="Your profile"
                  class="flex flex-grow items-center !justify-start !px-2 text-sm font-semibold"
                  @click="handleGoToProfile"
                >
                  <UserAvatar :user="usersStore.me" />
                  <div aria-hidden="true" class="flex flex-col items-start justify-center ml-2">
                    <span>{{ usersStore.me?.display_name }}</span>
                    <span class="text-xs opacity-50">{{ usersStore.me?.email }}</span>
                  </div>
                </Button>
                <ThemeSwitcher displayVariant="icon" />
              </div>
            </li>
          </ul>
        </nav>
      </div>
    </div>
    <CreateWorkspaceDialog
      v-model:visible="showCreateWorkspaceDialog"
      @update:visible="(state) => (showCreateWorkspaceDialog = state)"
    />
    <CreateDatabaseDialog
      v-model:visible="showCreateDatabaseDialog"
      @update:visible="(state) => (showCreateDatabaseDialog = state)"
    />
  </div>
</template>
