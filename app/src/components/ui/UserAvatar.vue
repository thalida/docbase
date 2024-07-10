<script setup lang="ts">
import Avatar from 'primevue/avatar'
import type { IUser } from '@/types/users'

defineProps<{
  user: IUser | null | undefined
  isMe?: boolean
}>()
</script>

<template>
  <Avatar
    v-if="user?.avatar"
    :image="user?.avatar"
    shape="circle"
    :class="{
      'outline outline-2 outline-offset-1 outline-yellow-500': isMe
    }"
  />
  <Avatar
    v-else
    :label="user?.initials"
    shape="circle"
    :class="{
      'outline outline-2 outline-offset-1 outline-yellow-500': isMe
    }"
  />
</template>
