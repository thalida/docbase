<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUsersStore } from '@/stores/users'
import { useWorkspacesStore } from '@/stores/workspaces'
import { useWorkspaceInvitationsStore } from '@/stores/workspaceInvitations'
import { useToast } from 'primevue/usetoast'
import type { IWorkspaceInvitation } from '@/types/workspaceInvitations'

const props = defineProps<{
  visible: boolean
  userId?: string
}>()
const emits = defineEmits(['update:visible'])
const route = useRoute()
const router = useRouter()
const toast = useToast()
const usersStore = useUsersStore()
const workspacesStore = useWorkspacesStore()
const workspaceInvitationsStore = useWorkspaceInvitationsStore()
const isMe = computed(() => props.userId === usersStore.me?.id)
const user = computed(() => {
  return usersStore.get(props.userId || '')
})
const myPendingInvitations = computed(() => {
  return usersStore.myPendingInvitations
})
const invitationErrors = ref<Record<string, string[]>>({})

watch(
  () => props.userId,
  (userId) => {
    if (typeof userId === 'undefined') return
    usersStore.fetch(userId)
  },
  { immediate: true }
)

function handleCloseProfile() {
  const queryParams = { ...route.query }
  delete queryParams.profile

  router.replace({ query: queryParams })
}

function handleUpdateVisible(visible: boolean) {
  emits('update:visible', visible)
}

async function handleAcceptInvitation(invitation: IWorkspaceInvitation) {
  try {
    await workspaceInvitationsStore.accept(invitation.id)
    toast.add({
      group: 'globalNotifications',
      severity: 'success',
      summary: 'Invitation accepted',
      detail: `You have joined ${invitation.workspace_meta.name}`,
      life: 2000
    })
    workspacesStore.fetchAll()
    invitationErrors.value = {}
  } catch (error: any) {
    invitationErrors.value = error.response.data
  }
}

async function handleRejectInvitation(invitation: IWorkspaceInvitation) {
  workspaceInvitationsStore.reject(invitation.id)
}

async function handleRefreshPendingInvitations() {
  invitationErrors.value = {}
  await usersStore.fetchMe(true)
  workspaceInvitationsStore.fetchAll({ email: usersStore.me?.email })
}
</script>

<template>
  <Dialog
    :visible="props.visible"
    @update:visible="handleUpdateVisible"
    @hide="handleCloseProfile"
    :header="isMe ? 'My Profile' : 'Profile'"
    :modal="false"
    position="right"
    :draggable="false"
    :maximizable="false"
    :style="{
      height: '100%',
      maxHeight: '100%',
      margin: 0,
      width: '30rem',
      borderRadius: 0
    }"
  >
    <div v-if="user" class="flex flex-col gap-4">
      <Panel header="Profile">
        <div class="flex flex-row gap-4 items-center">
          <UserAvatar :user="user" />
          <div class="flex flex-col">
            <span>{{ user.display_name }}</span>
            <span class="text-xs text-surface-500 dark:text-surface-400">{{ user.email }}</span>
          </div>
        </div>
      </Panel>
      <Panel v-if="isMe" header="Pending Invitations" toggleable>
        <template #icons>
          <Button
            icon="pi pi-refresh"
            severity="secondary"
            rounded
            text
            @click="handleRefreshPendingInvitations"
          />
        </template>
        <div v-if="myPendingInvitations.length === 0" class="text-center italic text-gray-500">
          No pending invitations
        </div>
        <div v-if="invitationErrors">
          <div v-for="(errors, key) in invitationErrors" :key="key">
            <div v-for="error in errors" :key="error" class="text-red-500 text-sm">{{ error }}</div>
          </div>
        </div>
        <div
          v-for="invitation in myPendingInvitations"
          :key="invitation.id"
          class="flex flex-row gap-4 items-center justify-between"
        >
          <span class="font-semibold">
            {{ invitation.workspace_meta.name }}
          </span>
          <ButtonGroup>
            <Button
              size="small"
              severity="danger"
              icon="pi pi-times"
              @click="() => handleRejectInvitation(invitation)"
              v-tooltip.left="{ value: 'Reject Invitation' }"
            />
            <Button
              size="small"
              severity="success"
              icon="pi pi-check"
              @click="() => handleAcceptInvitation(invitation)"
              v-tooltip.left="{ value: 'Accept Invitation' }"
            />
          </ButtonGroup>
        </div>
      </Panel>
    </div>
  </Dialog>
</template>
