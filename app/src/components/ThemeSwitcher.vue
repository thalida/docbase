<script setup lang="ts">
import { ref } from 'vue'
import { useUIStore } from '@/stores/ui'

const uiStore = useUIStore()
const menu = ref()
const items = ref([
  {
    label: 'Light',
    icon: 'pi pi-sun',
    command: () => uiStore.setTheme('light')
  },
  {
    label: 'Dark',
    icon: 'pi pi-moon',
    command: () => uiStore.setTheme('dark')
  },
  {
    label: 'System',
    icon: 'pi pi-desktop',
    command: () => uiStore.setTheme('system')
  }
])

function toggleMenu(event) {
  menu.value.toggle(event)
}
</script>

<template>
  <div>
    <Button
      type="button"
      :icon="uiStore.colorScheme === 'light' ? 'pi pi-sun' : 'pi pi-moon'"
      text
      @click="toggleMenu"
      aria-haspopup="true"
      aria-controls="app_theme_overlay_menu"
    />
    <Menu ref="menu" id="app_theme_overlay_menu" :model="items" :popup="true" />
  </div>
</template>
