<script setup lang="ts">
import { ref, defineProps, computed, watch } from 'vue'
import type { Space } from '@ably/spaces'
import { useRealtimeStore } from '@/stores/realtime'
import MemberAvatar from './MemberAvatar.vue'

const props = defineProps<{
  workspaceId: string
}>()
const realtimeStore = useRealtimeStore()

const space = ref<Space>()
const members = computed(() => realtimeStore.getMembersBySpace(space.value?.name ?? ''))
const myMember = computed(() => realtimeStore.getSelfBySpace(space.value?.name ?? ''))

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
    <MemberAvatar
      v-for="(member, index) in members"
      :key="index"
      :member="member"
      :isMe="
        member.clientId === myMember?.clientId && member.connectionId === myMember?.connectionId
      "
    />
  </div>
</template>
