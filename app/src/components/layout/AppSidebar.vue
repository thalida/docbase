<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import Button from 'primevue/button'
import { FolderPlusIcon, SquaresPlusIcon } from '@heroicons/vue/24/outline'
import {
  Listbox,
  ListboxButton,
  ListboxLabel,
  ListboxOption,
  ListboxOptions
} from '@headlessui/vue'
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'

import { ROUTES } from '@/router'
import AppThemeSwitcher from '@/components/ui/AppThemeSwitcher.vue'
import XAvatar from '@/components/ui/XAvatar.vue'
import { useUsersStore } from '@/stores/users'
import { useWorkspacesStore } from '@/stores/workspaces'
import { useDatabasesStore } from '@/stores/databases'

const route = useRoute()
const router = useRouter()
const usersStore = useUsersStore()
const workspacesStore = useWorkspacesStore()
const databaseStore = useDatabasesStore()

const currentWorkspaceId = ref(route.params.workspaceId as string)
const currentWorkspace = computed(() => workspacesStore.getOne(currentWorkspaceId.value))
const workspaceDBs = computed(() => databaseStore.getAllByWorkspace(currentWorkspaceId.value))

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
      <AppThemeSwitcher />
    </div>
    <nav class="flex flex-1 flex-col">
      <ul role="list" class="flex flex-1 flex-col gap-y-7">
        <li>
          <Listbox
            as="div"
            :modelValue="currentWorkspaceId"
            @update:modelValue="handleChangeWorkspace"
          >
            <div class="flex flex-row justify-between items-center">
              <ListboxLabel class="flex-grow text-sm font-semibold leading-6 text-gray-400">
                Workspaces
              </ListboxLabel>
              <Button
                icon=""
                text
                v-tooltip.right="{ value: 'Create a workspace', showDelay: 300, hideDelay: 300 }"
                aria-label="Create a workspace"
              >
                <span>
                  <FolderPlusIcon class="h-5 w-5" aria-hidden="true" />
                </span>
              </Button>
            </div>
            <div class="flex flex-row items-center justify-center gap-2 mt-2">
              <div class="relative flex-grow">
                <ListboxButton
                  class="relative w-full cursor-default rounded-md bg-white dark:bg-gray-900 py-1.5 pl-3 pr-10 text-left text-gray-900 dark:text-white shadow-sm ring-1 ring-inset ring-gray-300 dark:ring-white/10 focus:outline-none focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6"
                >
                  <span class="block truncate">{{ currentWorkspace?.name }}</span>
                  <span
                    class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2"
                  >
                    <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                  </span>
                </ListboxButton>

                <transition
                  leave-active-class="transition ease-in duration-100"
                  leave-from-class="opacity-100"
                  leave-to-class="opacity-0"
                >
                  <ListboxOptions
                    class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white dark:bg-gray-900 py-1 text-base shadow-lg ring-1 ring-black dark:ring-white/10 ring-opacity-5 focus:outline-none sm:text-sm"
                  >
                    <ListboxOption
                      as="template"
                      v-for="workspace in workspacesStore.orderedCollection"
                      :key="workspace.id"
                      :value="workspace.id"
                      v-slot="{ active, selected }"
                    >
                      <li
                        :class="[
                          active ? 'bg-indigo-600 text-white' : 'text-gray-900 dark:text-white',
                          'relative cursor-default select-none py-2 pl-3 pr-9'
                        ]"
                      >
                        <span
                          :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']"
                        >
                          {{ workspace.name }}
                        </span>

                        <span
                          v-if="selected"
                          :class="[
                            active ? 'text-white' : 'text-indigo-600',
                            'absolute inset-y-0 right-0 flex items-center pr-4'
                          ]"
                        >
                          <CheckIcon class="h-5 w-5" aria-hidden="true" />
                        </span>
                      </li>
                    </ListboxOption>
                  </ListboxOptions>
                </transition>
              </div>
              <Button
                icon="pi pi-cog"
                text
                severity="secondary"
                v-tooltip.right="{ value: 'Workspace Settings', showDelay: 300, hideDelay: 300 }"
                aria-label="Workspace Settings"
              />
            </div>
          </Listbox>
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
            >
              <span>
                <SquaresPlusIcon class="h-5 w-5" aria-hidden="true" />
              </span>
            </Button>
          </div>
          <ul v-if="workspaceDBs.length > 0" role="list" class="-mx-2 mt-2 space-y-1">
            <li v-for="database in workspaceDBs" :key="database.id">
              <a
                :href="database.id"
                :class="[
                  false
                    ? 'bg-gray-50 text-indigo-600 dark:bg-gray-800 dark:text-white'
                    : 'text-gray-700 hover:bg-gray-50 hover:text-indigo-600 dark:text-white dark:hover:bg-gray-800 dark:hover:text-white',
                  'group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6'
                ]"
              >
                <span class="truncate">{{ database.name }}</span>
              </a>
            </li>
          </ul>
          <div v-else>
            <Button aria-label="Create a database" class="w-full gap-2">
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
              icon="pi pi-sign-out"
              text
              severity="secondary"
              aria-label="Your profile"
              class="flex flex-grow items-center !justify-start gap-x-2 !px-2 text-sm font-semibold"
            >
              <XAvatar />
              <span aria-hidden="true">{{ usersStore.me?.display_name }}</span>
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
  </div>
</template>
