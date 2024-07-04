<script setup lang="ts">
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { useUIStore } from '@/stores/ui'
import type { Theme } from '@/types/ui'

import { SunIcon, MoonIcon, ComputerDesktopIcon } from '@heroicons/vue/24/outline'

const uiStore = useUIStore()

const menuOptions = [
  {
    key: 'light',
    icon: SunIcon,
    label: 'Light'
  },
  {
    key: 'dark',
    icon: MoonIcon,
    label: 'Dark'
  },
  {
    key: 'system',
    icon: ComputerDesktopIcon,
    label: 'System'
  }
]
</script>

<template>
  <Menu as="div" class="relative inline-block text-left">
    <div>
      <MenuButton
        class="flex flex-row items-center justify-between px-2.5 py-2 rounded-md text-sm font-semibold text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
      >
        <span class="sr-only">Open options</span>
        <SunIcon v-if="uiStore.colorScheme === 'light'" class="h-5 w-5" />
        <MoonIcon v-else class="h-5 w-5" />
      </MenuButton>
    </div>

    <transition
      enter-active-class="transition duration-100 ease-out"
      enter-from-class="scale-95 transform opacity-0"
      enter-to-class="scale-100 transform opacity-100"
      leave-active-class="transition duration-75 ease-in"
      leave-from-class="scale-100 transform opacity-100"
      leave-to-class="scale-95 transform opacity-0"
    >
      <MenuItems
        class="absolute top-8 right-1 z-10 mt-2 min-w-32 origin-top-right overflow-hidden rounded-md bg-white dark:bg-gray-900 shadow-lg ring-1 ring-black dark:ring-white/10 ring-opacity-5 focus:outline-none sm:text-sm"
      >
        <div>
          <MenuItem v-for="option in menuOptions" :key="option.key" v-slot="{ active: hover }">
            <button
              @click="uiStore.setTheme(option.key as Theme)"
              class="flex w-full flex-row items-center justify-start gap-2 px-4 py-2 text-left text-sm"
              :class="{
                'text-indigo-600': uiStore.theme === option.key,
                'bg-indigo-600 text-white': uiStore.theme !== option.key && hover,
                'text-gray-900 dark:text-white': uiStore.theme !== option.key && !hover
              }"
            >
              <component :is="option.icon" class="mr-2 inline-block h-4 w-4" />
              <span>{{ option.label }}</span>
            </button>
          </MenuItem>
        </div>
      </MenuItems>
    </transition>
  </Menu>
</template>
