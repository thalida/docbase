<script setup lang="ts">
import { ref, defineProps, computed, watch, watchEffect, onMounted, onBeforeUnmount } from 'vue'
import type { Space } from '@ably/spaces'
import AblyInstance, { utils } from '@/services/ably'
import type { IUser } from '@/types/users'
import { useUsersStore } from '@/stores/users'
import UserAvatar from '@/components/ui/UserAvatar.vue'

const props = defineProps<{
  workspaceId: string
}>()
const usersStore = useUsersStore()

const space = ref<Space | null>(null)
const users = ref<IUser[]>([])
const spaceId = ref<string>('')

watch(
  () => props.workspaceId,
  async (workspaceId) => {
    spaceId.value = utils.getSpaceId(workspaceId)

    if (space.value) {
      space.value.members.unsubscribe()
    }

    space.value = await AblyInstance.spaces.get(spaceId.value)

    const allMembers = await space.value.members.getAll()
    users.value = await Promise.all(
      allMembers
        .filter((member) => member.isConnected)
        .map(async (member) => {
          return (await usersStore.get(member.clientId)) as IUser
        })
    )

    // Subscribe to member enters in a space
    space.value.members.subscribe('enter', async ({ clientId }) => {
      console.info('Member entered:', clientId)
      if (users.value.find((user) => user.id === clientId)) {
        return
      }

      const user = (await usersStore.get(clientId)) as IUser
      users.value.push(user)
      console.info('User added:', user)
    })

    // Subscribe to member leaves in a space
    space.value.members.subscribe('leave', ({ clientId }) => {
      console.info('Member left:', clientId)
      users.value = users.value.filter((user) => user.id !== clientId)
    })

    // Subscribe to member removals in a space
    space.value.members.subscribe('remove', ({ clientId }) => {
      console.info('Member removed:', clientId)
      users.value = users.value.filter((user) => user.id !== clientId)
    })
  },
  { immediate: true }
)

onBeforeUnmount(() => {
  if (space.value) {
    space.value.members.unsubscribe()
  }
})
</script>

<template>
  <div>
    <div v-for="user in users" :key="user.id">
      <UserAvatar :user="user" />
    </div>
  </div>
</template>
