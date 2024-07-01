<script setup lang="ts">
import Avatar from 'primevue/avatar'
import { useUsersStore } from '@/stores/users'

const usersStore = useUsersStore()
</script>

<template>
  <Avatar v-if="usersStore.me?.avatar" :image="usersStore.me?.avatar" shape="circle" />
  <Avatar v-else :label="usersStore.me?.initials" shape="circle" />
</template>
