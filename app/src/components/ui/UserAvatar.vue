<script setup lang="ts">
import Avatar from 'primevue/avatar'
import type { IUser } from '@/types/users'

defineProps<{
  user: IUser | null | undefined
}>()
</script>

<template>
  <Avatar v-if="user?.avatar" :image="user?.avatar" shape="circle" />
  <Avatar v-else :label="user?.initials" shape="circle" />
</template>
