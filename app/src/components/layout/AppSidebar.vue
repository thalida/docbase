<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Button from 'primevue/button'
import { FolderPlusIcon, SquaresPlusIcon } from '@heroicons/vue/24/outline'

import { ROUTES } from '@/router'
import ThemeSwitcher from '@/components/ThemeSwitcher.vue'
import UserAvatar from '@/components/ui/UserAvatar.vue'
import CreateWorkspaceDialog from '@/components/dialogs/CreateWorkspaceDialog.vue'
import EditWorkspaceDialog from '@/components/dialogs/EditWorkspaceDialog.vue'
import CreateDatabaseDialog from '@/components/dialogs/CreateDatabaseDialog.vue'
import { useUsersStore } from '@/stores/users'
import { useWorkspacesStore } from '@/stores/workspaces'
import { useDatabasesStore } from '@/stores/databases'

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
</script>

<template>
  <div
    class="flex grow flex-col gap-y-5 overflow-y-auto bg-white border-r border-gray-200 px-4 pb-2 dark:bg-gray-900 dark:border-0 :ring-1 dark:ring-white/10"
  >
    <div class="flex flex-row justify-between h-16 shrink-0 items-center">
      <div>
        <img
          class="h-8 w-auto"
          src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600"
          alt="Your Company"
        />
      </div>
      <ThemeSwitcher />
    </div>
    <nav class="flex flex-1 flex-col">
      <ul role="list" class="flex flex-1 flex-col gap-y-7">
        <li>
          <div class="flex flex-row justify-between items-center">
            <div class="w-full flex-grow text-sm font-semibold leading-6 text-gray-400">
              Workspaces
            </div>
            <Button
              icon=""
              text
              v-tooltip.right="{ value: 'Create a workspace', showDelay: 300, hideDelay: 300 }"
              aria-label="Create a workspace"
              class="w-10 h-10"
              @click="handleCreateWorkspace"
            >
              <span>
                <FolderPlusIcon class="h-5 w-5" aria-hidden="true" />
              </span>
            </Button>
          </div>
          <div class="flex flex-row items-center justify-between gap-2 mt-2">
            <Select
              :modelValue="currentWorkspaceId"
              @update:modelValue="handleChangeWorkspace"
              :options="workspacesStore.orderedCollection"
              optionValue="id"
              optionLabel="name"
              placeholder="Select a workspace"
              :highlightOnSelect="false"
              class="flex-grow min-w-0"
            >
              <template #option="slotProps">
                <div class="flex flex-row items-center justify-between gap-4">
                  <div>{{ slotProps.option.name }}</div>
                  <Tag v-if="slotProps.option.is_default" value="Default" />
                </div>
              </template>
            </Select>
            <Button
              icon="pi pi-cog"
              text
              severity="secondary"
              v-tooltip.right="{ value: 'Workspace Settings', showDelay: 300, hideDelay: 300 }"
              aria-label="Workspace Settings"
              class="flex-shrink-0 w-10 h-10"
              @click="handleEditWorkspace"
            />
          </div>
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
              class="w-full gap-2"
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
</template>
