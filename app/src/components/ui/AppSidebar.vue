<script setup lang="ts">
import { Cog8ToothIcon, FolderPlusIcon, SquaresPlusIcon } from '@heroicons/vue/24/outline'

import { ref } from 'vue'
import {
  Listbox,
  ListboxButton,
  ListboxLabel,
  ListboxOption,
  ListboxOptions
} from '@headlessui/vue'
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'
import AppThemeSwitcher from '@/components/ui/AppThemeSwitcher.vue'

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
              <div>
                <button
                  type="button"
                  class="flex flex-row items-center justify-between px-2.5 py-2 rounded-md text-sm font-semibold text-yellow-700 dark:text-yellow-400 hover:bg-gray-100 dark:hover:bg-gray-800"
                >
                  <FolderPlusIcon class="-ml-0.5 h-5 w-5" aria-hidden="true" />
                </button>
              </div>
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
              <div>
                <button
                  type="button"
                  class="flex flex-row items-center justify-between px-2.5 py-2 rounded-md text-sm font-semibold text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
                >
                  <Cog8ToothIcon class="h-5 w-5" aria-hidden="true" />
                </button>
              </div>
            </div>
          </Listbox>
        </li>
        <li>
          <div class="flex flex-row justify-between items-center">
            <div class="w-full flex-grow text-sm font-semibold leading-6 text-gray-400">
              Databases
            </div>
            <div>
              <button
                type="button"
                class="flex flex-row items-center justify-between px-2.5 py-2 rounded-md text-yellow-700 dark:text-yellow-400 hover:bg-gray-100 dark:hover:bg-gray-800"
              >
                <SquaresPlusIcon class="-ml-0.5 h-5 w-5" aria-hidden="true" />
              </button>
            </div>
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
        <li class="-mx-6 mt-auto">
          <a
            href="#"
            class="flex items-center gap-x-4 px-6 py-3 text-sm font-semibold leading-6 text-gray-900 hover:bg-gray-50 dark:text-white dark:hover:bg-gray-800"
          >
            <img
              class="h-8 w-8 rounded-full bg-gray-50 dark:bg-gray-800"
              src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
              alt=""
            />
            <span class="sr-only">Your profile</span>
            <span aria-hidden="true">Tom Cook</span>
          </a>
        </li>
      </ul>
    </nav>
  </div>
</template>
