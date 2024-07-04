<script setup lang="ts">
import { Bars3Icon } from '@heroicons/vue/24/outline'

const emit = defineEmits<{
  (e: 'openSidebar'): void
}>()
</script>

<template>
  <header
    class="sticky top-0 z-40 flex items-center gap-x-6 bg-white dark:bg-gray-900 px-4 py-4 shadow-sm sm:px-6 lg:hidden"
  >
    <button
      type="button"
      class="-m-2.5 p-2.5 text-gray-700 dark:text-gray-400 lg:hidden"
      @click="emit('openSidebar')"
    >
      <span class="sr-only">Open sidebar</span>
      <Bars3Icon class="h-6 w-6" aria-hidden="true" />
    </button>
    <div class="flex-1 text-sm font-semibold leading-6 text-gray-900 dark:text-white">
      Dashboard
    </div>
  </header>
</template>
