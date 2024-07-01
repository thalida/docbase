<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
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

const router = useRouter()
const usersStore = useUsersStore()

const people = [
  { id: 1, name: 'Wade Cooper' },
  { id: 2, name: 'Arlene Mccoy' },
  { id: 3, name: 'Devon Webb' },
  { id: 4, name: 'Tom Cook' },
  { id: 5, name: 'Tanya Fox' },
  { id: 6, name: 'Hellen Schmidt' },
  { id: 7, name: 'Caroline Schultz' },
  { id: 8, name: 'Mason Heaney' },
  { id: 9, name: 'Claudie Smitham' },
  { id: 10, name: 'Emil Schaefer' }
]

const selected = ref(people[3])
const databases = [
  { id: 1, name: 'Heroicons', href: '#', initial: 'H', current: false },
  { id: 2, name: 'Tailwind Labs', href: '#', initial: 'T', current: false },
  { id: 3, name: 'Workcation', href: '#', initial: 'W', current: false }
]

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
          <Listbox as="div" v-model="selected">
            <div class="flex flex-row justify-between items-center">
              <ListboxLabel class="flex-grow text-sm font-semibold leading-6 text-gray-400"
                >Workspaces</ListboxLabel
              >
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
                  <span class="block truncate">{{ selected.name }}</span>
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
                      v-for="person in people"
                      :key="person.id"
                      :value="person"
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
                          >{{ person.name }}</span
                        >

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
          <ul role="list" class="-mx-2 mt-2 space-y-1">
            <li v-for="db in databases" :key="db.name">
              <a
                :href="db.href"
                :class="[
                  db.current
                    ? 'bg-gray-50 text-indigo-600 dark:bg-gray-800 dark:text-white'
                    : 'text-gray-700 hover:bg-gray-50 hover:text-indigo-600 dark:text-white dark:hover:bg-gray-800 dark:hover:text-white',
                  'group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6'
                ]"
              >
                <span class="truncate">{{ db.name }}</span>
              </a>
            </li>
          </ul>
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
