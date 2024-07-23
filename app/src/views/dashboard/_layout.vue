<script setup lang="ts">
import AppLayout from '@/components/layout/AppLayout.vue'

const props = defineProps<{
  showUserProfile: boolean
  profileForUser?: string
}>()
</script>

<template>
  <AppLayout v-bind="props">
    <RouterView />
  </AppLayout>
</template>
