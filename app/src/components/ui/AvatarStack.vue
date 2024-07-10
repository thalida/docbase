<script setup lang="ts">
import { ref, defineProps, computed, watch, watchEffect, onMounted, onBeforeUnmount } from 'vue'
import type { Space } from '@ably/spaces'
import type { IUser } from '@/types/users'
import { useRealtimeStore } from '@/stores/realtime'
import { useUsersStore } from '@/stores/users'
import UserAvatar from '@/components/ui/UserAvatar.vue'

const props = defineProps<{
  workspaceId: string
}>()
const realtimeStore = useRealtimeStore()

const space = ref<Space>()
const users = computed(() => realtimeStore.getUsersBySpace(space.value?.name ?? ''))

watch(
  () => props.workspaceId,
  async (workspaceId) => {
    space.value = await realtimeStore.getSpace(workspaceId)
  },
  { immediate: true }
)
</script>

<template>
  <div>
    <div v-for="user in users" :key="user.id">
      <UserAvatar :user="user" />
    </div>
  </div>
</template>
