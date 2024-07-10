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
    v-bind="$attrs"
    :image="user?.avatar"
    shape="circle"
    :class="{
      'border !border-yellow-500': isMe
    }"
  />
  <Avatar
    v-else
    v-bind="$attrs"
    :label="user?.initials"
    shape="circle"
    :class="{
      'border !border-yellow-500': isMe
    }"
  />
</template>
