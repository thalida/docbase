<script setup lang="ts">
import { watch } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { ROUTES } from '@/router'
import { useWorkspaceInvitationsStore } from '@/stores/workspaceInvitations'

const props = defineProps<{
  invitation: string
}>()
const router = useRouter()
const toast = useToast()
const workspaceInvitationsStore = useWorkspaceInvitationsStore()

watch(
  () => props.invitation,
  async (invitationId) => {
    if (!invitationId) {
      console.error('No invitation ID provided')
      router.replace({ name: ROUTES.INDEX })
      return
    }

    let invitation
    try {
      invitation = await workspaceInvitationsStore.fetch(invitationId)
    } catch (error) {
      console.error('Error fetching invitation', error)
      router.replace({ name: ROUTES.INDEX })
      return
    }

    if (!invitation) {
      console.error('Invitation not found')
      router.replace({ name: ROUTES.INDEX })
      return
    }

    try {
      await workspaceInvitationsStore.accept(invitationId)
      toast.add({
        group: 'globalNotifications',
        severity: 'success',
        summary: 'Invitation accepted',
        detail: `You have joined ${invitation.workspace_meta.name}`,
        life: 2000
      })
      router.replace({ name: ROUTES.WORKSPACE, params: { workspaceId: invitation.workspace } })
    } catch (error) {
      console.error('Error accepting invitation', error)
      router.replace({ name: ROUTES.INDEX })
      return
    }
  },
  { immediate: true }
)
</script>

<template>
  <div></div>
</template>
