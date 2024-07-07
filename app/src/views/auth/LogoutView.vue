<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUIStore } from '@/stores/ui'
import { useAuthStore } from '@/stores/auth'
import { ROUTES } from '@/router'

const router = useRouter()
const uiStore = useUIStore()
const authStore = useAuthStore()

onMounted(() => {
  authStore.logout().finally(() => {
    uiStore.$resetAll()
    router.push({ name: ROUTES.LOGIN })
  })
})
</script>

<template>
  <main class="flex h-full max-h-full flex-col bg-blue-100 dark:bg-slate-900"></main>
</template>
