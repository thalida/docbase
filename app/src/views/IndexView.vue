<script setup lang="ts">
import { watchEffect } from 'vue'
import { useRouter } from 'vue-router'
import { ROUTES } from '@/router'
import { useAuthStore } from '@/stores/auth'
import { useUsersStore } from '@/stores/users'

const router = useRouter()
const authStore = useAuthStore()
const usersStore = useUsersStore()

watchEffect(async () => {
  if (!authStore.isAuthenticated) {
    router.replace({ name: ROUTES.LOGIN })
    return
  }

  const myWorkspaces = usersStore.me?.workspaces || []
  if (myWorkspaces.length === 0) {
    return
  }

  const defaultWorkspace = usersStore.me?.default_workspace || myWorkspaces[0]
  router.replace({ name: ROUTES.WORKSPACE, params: { workspaceId: defaultWorkspace } })
})
</script>

<template>
  <div></div>
</template>
