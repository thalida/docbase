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
  <div />
</template>
