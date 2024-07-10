<script setup lang="ts">
import { defineProps, computed, watch } from 'vue'
import type { SpaceMember } from '@ably/spaces'
import { useUsersStore } from '@/stores/users'
import UserAvatar from '@/components/ui/UserAvatar.vue'

const props = defineProps<{
  member: SpaceMember
  isMe?: boolean
}>()

const usersStore = useUsersStore()
const user = computed(() => usersStore.get(props.member.clientId))

watch(
  () => props.member.clientId,
  async (clientId) => {
    await usersStore.getOrFetch(clientId)
  },
  { immediate: true }
)
</script>

<template>
  <UserAvatar :user="user" :isMe="isMe" size="small" />
</template>
