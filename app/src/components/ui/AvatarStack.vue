<script setup lang="ts">
import { ref, defineProps, computed, watchEffect, onMounted, onBeforeUnmount } from 'vue'
import type { Space } from '@ably/spaces'
import AblyInstance, { utils } from '@/services/ably'
import type { IUser } from '@/types/users'
import { useUsersStore } from '@/stores/users'
import UserAvatar from '@/components/ui/UserAvatar.vue'

const props = defineProps<{
  workspaceId: string
  databaseId?: string
}>()
const usersStore = useUsersStore()

const space = ref<Space | null>(null)
const users = ref<IUser[]>([])
const spaceId = computed(() => utils.getSpaceId(props.workspaceId, props.databaseId))
console.log('Space ID:', spaceId.value)

watchEffect(async () => {
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
    console.log(
      'Member entered:',
      clientId,
      users.value.find((user) => user.id === clientId)
    )
    if (users.value.find((user) => user.id === clientId)) {
      return
    }

    const user = (await usersStore.get(clientId)) as IUser
    users.value.push(user)
    console.log('User added:', user)
  })

  // Subscribe to member leaves in a space
  space.value.members.subscribe('leave', ({ clientId }) => {
    console.log('Member left:', clientId)
    users.value = users.value.filter((user) => user.id !== clientId)
  })

  // Subscribe to member removals in a space
  space.value.members.subscribe('remove', ({ clientId }) => {
    console.log('Member removed:', clientId)
    users.value = users.value.filter((user) => user.id !== clientId)
  })
})

onBeforeUnmount(() => {
  if (space.value) {
    console.log('Unsubscribing from space')
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
