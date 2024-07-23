<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Button from 'primevue/button'
import {
  SquaresPlusIcon,
  Squares2X2Icon,
  Cog6ToothIcon,
  CheckIcon,
  ChevronUpDownIcon,
  XMarkIcon,
  Bars3Icon,
  CircleStackIcon
} from '@heroicons/vue/24/outline'

import { ROUTES } from '@/router'
import ThemeSwitcher from '@/components/ThemeSwitcher.vue'
import UserAvatar from '@/components/ui/UserAvatar.vue'
import CreateWorkspaceDialog from '@/components/dialogs/CreateWorkspaceDialog.vue'
import CreateDatabaseDialog from '@/components/dialogs/CreateDatabaseDialog.vue'
import { useUIStore } from '@/stores/ui'
import { useUsersStore } from '@/stores/users'
import { useWorkspacesStore } from '@/stores/workspaces'
import { useDatabasesStore } from '@/stores/databases'

const route = useRoute()
const router = useRouter()
const uiStore = useUIStore()
const usersStore = useUsersStore()
const workspacesStore = useWorkspacesStore()
const databaseStore = useDatabasesStore()

const currentWorkspaceId = ref(route.params.workspaceId as string)
const currentWorkspace = computed(() => workspacesStore.get(currentWorkspaceId.value))
const workspaceDBs = computed(() => databaseStore.getAllByWorkspace(currentWorkspaceId.value))
const showCreateWorkspaceDialog = ref(false)
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
        block: uiStore.isSidebarOpen,
        hidden: !uiStore.isSidebarOpen
      }"
      @click="uiStore.setIsSidebarOpen(false)"
    />
    <div
      class="fixed top-0 left-0 md:relative flex flex-col flex-shrink-0 flex-grow-0 gap-4 h-full rounded-lg overflow-y-auto transition-all ease-in-out duration-300 bg-white dark:bg-gray-900"
      :class="{
        'w-72': uiStore.isSidebarOpen,
        'w-16': !uiStore.isSidebarOpen
      }"
    >
      <div
        class="flex justify-between shrink-0 items-center px-2"
        :class="{
          'flex-row pt-2': uiStore.isSidebarOpen,
          'flex-col pt-4': !uiStore.isSidebarOpen
        }"
      >
        <div
          :class="{
            'px-3 py-2': uiStore.isSidebarOpen
          }"
        >
          {{ uiStore.isSidebarOpen ? 'docbase' : 'db' }}
        </div>
        <Button
          type="button"
          size="small"
          severity="secondary"
          text
          :class="[
            {
              '!w-full': !uiStore.isSidebarOpen,
              '!p-2': uiStore.isSidebarOpen
            }
          ]"
          @click="uiStore.toggleSidebarStore"
        >
          <span class="sr-only">Toggle sidebar</span>
          <XMarkIcon v-if="uiStore.isSidebarOpen" class="h-6 w-6" aria-hidden="true" />
          <Bars3Icon v-else class="h-6 w-6" aria-hidden="true" />
        </Button>
      </div>
      <nav class="flex flex-1 flex-col grow px-2 pb-2">
        <ul role="list" class="flex flex-1 flex-col gap-2">
          <li
            :class="{
              'px-3': uiStore.isSidebarOpen
            }"
          >
            <Button
              type="button"
              size="normal"
              severity="secondary"
              :outlined="uiStore.isSidebarOpen"
              :text="!uiStore.isSidebarOpen"
              class="w-full !p-2 !rounded-lg"
              @click="toggleWorkspacesMenu"
              aria-haspopup="true"
              aria-controls="workspaces_menu"
            >
              <div
                class="grow flex flex-row items-center flex-nowrap gap-4 w-full"
                :class="{
                  'justify-center': !uiStore.isSidebarOpen,
                  'justify-between': uiStore.isSidebarOpen
                }"
              >
                <div
                  class="flex flex-row items-center gap-2 truncate w-full"
                  :class="{
                    'justify-center': !uiStore.isSidebarOpen,
                    'justify-start': uiStore.isSidebarOpen
                  }"
                >
                  <WorkspaceAvatar v-if="currentWorkspace" :workspace="currentWorkspace" />
                  <div v-if="uiStore.isSidebarOpen" class="flex flex-row flex-shrink truncate">
                    <span class="truncate text-color">
                      {{ currentWorkspace?.name || 'Workspaces' }}
                    </span>
                  </div>
                </div>
                <ChevronUpDownIcon v-if="uiStore.isSidebarOpen" class="flex-shrink-0 h-4 w-4" />
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
                  <div class="flex flex-row flex-shrink items-center justify-start truncate gap-2">
                    <WorkspaceAvatar :workspace="item.workspace" />
                    <span
                      class="truncate"
                      :class="{
                        'text-color': item.isSelected,
                        'text-muted-color': !item.isSelected
                      }"
                    >
                      {{ item.label }}
                    </span>
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
                <div class="p-2">
                  <Button
                    type="button"
                    outlined
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
          <li class="flex flex-col">
            <Button
              as="RouterLink"
              text
              :severity="route.name === ROUTES.WORKSPACE ? 'primary' : 'secondary'"
              :to="{ name: ROUTES.WORKSPACE, params: { workspaceId: currentWorkspaceId } }"
            >
              <div
                class="flex flex-row gap-2 items-center grow"
                :class="{
                  'justify-start': uiStore.isSidebarOpen,
                  'justify-center': !uiStore.isSidebarOpen
                }"
              >
                <Squares2X2Icon class="h-6 w-6" aria-hidden="true" />
                <span v-if="uiStore.isSidebarOpen">Overview</span>
              </div>
            </Button>
            <Button
              as="RouterLink"
              text
              :severity="route.name === ROUTES.WORKSPACE_SETTINGS ? 'primary' : 'secondary'"
              :to="{
                name: ROUTES.WORKSPACE_SETTINGS,
                params: { workspaceId: currentWorkspaceId }
              }"
            >
              <div
                class="flex flex-row gap-2 items-center grow"
                :class="{
                  'justify-start': uiStore.isSidebarOpen,
                  'justify-center': !uiStore.isSidebarOpen
                }"
              >
                <Cog6ToothIcon class="h-6 w-6" aria-hidden="true" />
                <span v-if="uiStore.isSidebarOpen">Settings</span>
              </div>
            </Button>
          </li>
          <li>
            <Divider />
          </li>
          <li v-if="uiStore.isSidebarOpen" class="flex flex-col gap-2">
            <div
              class="w-full flex-grow text-sm font-semibold leading-6 text-muted-color opacity-60 px-4"
            >
              Databases
            </div>
            <ul role="list">
              <li v-for="database in workspaceDBs" :key="database.id">
                <Button
                  as="RouterLink"
                  text
                  :severity="
                    route.name === ROUTES.DATABASE && route.params.databaseId === database.id
                      ? 'primary'
                      : 'secondary'
                  "
                  :to="{
                    name: ROUTES.DATABASE,
                    params: { workspaceId: currentWorkspaceId, databaseId: database.id }
                  }"
                  :class="{
                    'w-full': uiStore.isSidebarOpen
                  }"
                >
                  <div class="flex flex-row gap-2 items-center grow justify-start">
                    <span class="truncate">{{ database.name }}</span>
                  </div>
                </Button>
              </li>
              <li
                v-if="workspaceDBs.length === 0"
                class="flex flex-row items-center justify-center px-3"
              >
                <span class="text-muted-color text-sm"> You don't have any databases yet. </span>
              </li>
              <li class="px-3">
                <Button
                  aria-label="Create a database"
                  class="w-full gap-2 mt-4 p-4"
                  @click="handleCreateDatabase"
                  severity="secondary"
                  outlined
                >
                  <CircleStackIcon class="h-5 w-5" aria-hidden="true" />
                  <span>Create a database</span>
                </Button>
              </li>
            </ul>
          </li>
          <li class="mt-auto">
            <div
              class="flex gap-2"
              :class="{
                'flex-col': !uiStore.isSidebarOpen,
                'flex-row items-center justify-between': uiStore.isSidebarOpen
              }"
            >
              <Button
                text
                severity="secondary"
                aria-label="Your profile"
                class="flex flex-grow items-center !justify-start !px-2 text-sm font-semibold"
                @click="handleGoToProfile"
              >
                <UserAvatar :user="usersStore.me" />
                <div
                  v-if="uiStore.isSidebarOpen"
                  aria-hidden="true"
                  class="flex flex-col items-start justify-center ml-2"
                >
                  <span>{{ usersStore.me?.display_name }}</span>
                  <span class="text-xs opacity-50">{{ usersStore.me?.email }}</span>
                </div>
              </Button>
              <ThemeSwitcher
                displayVariant="icon"
                :class="{
                  '!w-full': !uiStore.isSidebarOpen
                }"
              />
            </div>
          </li>
        </ul>
      </nav>
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
