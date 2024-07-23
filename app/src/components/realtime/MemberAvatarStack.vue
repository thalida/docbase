<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { Space } from '@ably/spaces'
import type { SpaceMember } from '@ably/spaces'
import { useRealtimeStore } from '@/stores/realtime'
import MemberAvatar from './MemberAvatar.vue'

const props = defineProps<{
  workspaceId: string
  filter?: (members: SpaceMember[]) => SpaceMember[]
}>()
const realtimeStore = useRealtimeStore()

const space = ref<Space>()
const members = computed(() => realtimeStore.getMembersBySpace(space.value?.name ?? ''))
const myMember = computed(() => realtimeStore.getSelfBySpace(space.value?.name ?? ''))
const filteredMembers = computed(() => (props.filter ? props.filter(members.value) : members.value))

watch(
  () => props.workspaceId,
  async (workspaceId) => {
    space.value = await realtimeStore.getSpace(workspaceId)
  },
  { immediate: true }
)
</script>

<template>
  <AvatarGroup>
    <MemberAvatar
      v-for="(member, index) in filteredMembers"
      :key="index"
      :member="member"
      :isMe="
        member.clientId === myMember?.clientId && member.connectionId === myMember?.connectionId
      "
    />
  </AvatarGroup>
</template>
