<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import { useUsersStore } from '@/stores/users'
import { useWorkspacesStore } from '@/stores/workspaces'
import { useWorkspaceInvitationsStore } from '@/stores/workspaceInvitations'
import type { IWorkspaceUpdateRequest } from '@/types/workspaces'
import { ROUTES } from '@/router'

const props = defineProps<{ visible: boolean; workspaceId: string }>()
const emits = defineEmits(['update:visible'])
const router = useRouter()
const confirm = useConfirm()
const usersStore = useUsersStore()
const workspacesStore = useWorkspacesStore()
const workspaceInvitationsStore = useWorkspaceInvitationsStore()
const currentWorkspace = computed(() => workspacesStore.get(props.workspaceId))
const teamMembers = computed(() => workspacesStore.getMembers(props.workspaceId))
const invitations = computed(() => workspacesStore.getPendingInvitations(props.workspaceId))

const isSubmitting = ref(false)
const isDeleting = ref(false)
const isInviting = ref(false)
const form = ref<IWorkspaceUpdateRequest>({
  name: '',
  is_default: false
})
const errors = ref<Record<string, string[]>>({})
const inviteForm = ref({ email: '' })
const inviteFormErrors = ref<Record<string, string[]>>({})
const toast = useToast()

watch(
  () => props.workspaceId,
  () => {
    setup()
  },
  { immediate: true }
)

watch(
  () => props.visible,
  (visible) => {
    if (visible) {
      setup()
    } else {
      reset()
    }
  }
)

function setup() {
  form.value = {
    name: currentWorkspace.value?.name ?? '',
    is_default: currentWorkspace.value?.is_default ?? false
  }
}

function reset() {
  errors.value = {}
  form.value = {
    name: '',
    is_default: false
  }
}

function confirmDelete() {
  return confirm.require({
    message: `Are you sure you want to delete the workspace: ${currentWorkspace.value?.name}?`,
    header: 'Danger Zone',
    icon: 'pi pi-info-circle',
    rejectLabel: 'Cancel',
    rejectProps: {
      label: 'Cancel',
      severity: 'secondary',
      outlined: true
    },
    acceptProps: {
      label: 'Delete',
      severity: 'danger'
    },
    accept: handleDelete
  })
}

async function handleInvite() {
  inviteFormErrors.value = {}
  try {
    await workspaceInvitationsStore.create({
      workspace: props.workspaceId,
      ...inviteForm.value
    })
    inviteForm.value.email = ''
  } catch (e: any) {
    inviteFormErrors.value = e.response.data
  }
}

async function handleCancelInvitation(invitationId: string) {
  await workspaceInvitationsStore.destroy(invitationId)
}

async function handleCopyInvitationLink(invitationId: string) {
  const invitation = invitations.value.find((i) => i.id === invitationId)
  const host = window.location.origin
  const route = router.resolve({
    name: ROUTES.ACCEPT_INVITE,
    query: { token: invitation?.token }
  })
  const url = `${host}${route.href}`
  await navigator.clipboard.writeText(url)
  toast.add({
    group: 'clipboard',
    severity: 'success',
    summary: 'Invitation Copied',
    detail: `${invitation?.email}'s invitation link copied to clipboard`,
    life: 2000
  })
}

function handleCancel() {
  reset()
  emits('update:visible', false)
}

async function handleSubmit() {
  isSubmitting.value = true
  try {
    await workspacesStore.update(props.workspaceId, form.value)
    reset()
    emits('update:visible', false)
  } catch (e: any) {
    errors.value = e.response.data
  } finally {
    isSubmitting.value = false
  }
}

async function handleDelete() {
  isDeleting.value = true
  try {
    await workspacesStore.destroy(props.workspaceId)
    reset()
    emits('update:visible', false)
    router.push({ name: ROUTES.INDEX })
  } catch (e: any) {
    errors.value = e.response?.data
  } finally {
    isDeleting.value = false
  }
}

function onVisibleChange(visible: boolean) {
  if (!visible) {
    reset()
  }

  emits('update:visible', visible)
}
</script>

<template>
  <Dialog
    v-if="typeof currentWorkspace !== 'undefined' && currentWorkspace !== null"
    modal
    v-bind="$attrs"
    :visible="props.visible"
    header="Workspace Settings"
    @update:visible="onVisibleChange"
    :style="{ width: '50%', minWidth: '25rem' }"
  >
    <div class="flex flex-col gap-4">
      <div class="flex flex-col gap-2">
        <label for="edit-workspace-dialog__field-name" class="font-semibold"> Name </label>
        <InputText
          id="edit-workspace-dialog__field-name"
          class="flex-auto"
          autocomplete="off"
          placeholder="My Awesome Workspace"
          v-model="form.name"
          :invalid="typeof errors.name !== 'undefined' && errors.name.length > 0"
          :disabled="!currentWorkspace.is_owner"
          v-tooltip.bottom="{
            value: 'Only owner\'s can edit the workspace name',
            disabled: currentWorkspace.is_owner
          }"
        />
        <div
          v-if="typeof errors.name !== 'undefined' && errors.name.length > 0"
          class="text-red-500 text-sm"
        >
          <span v-for="(error, i) in errors.name" :key="i">{{ error }}</span>
        </div>
      </div>
      <div class="flex flex-row items-center justify-between gap-2">
        <div class="flex flex-row gap-2 items-center justify-start">
          <label for="edit-workspace-dialog__field-is-default" class="font-semibold">
            Default workspace?
          </label>
          <i
            class="pi pi-question-circle"
            v-tooltip.bottom="'Make this workspace your default dashboard'"
          />
        </div>
        <ToggleSwitch inputId="edit-workspace-dialog__field-is-default" v-model="form.is_default" />
      </div>
      <Tabs value="0">
        <TabList>
          <Tab as="div" value="0" class="flex flex-row gap-1 items-center justify-center">
            <span>Team Members</span>
            <Badge :value="teamMembers.length" severity="secondary" size="small" />
          </Tab>
          <Tab
            v-if="currentWorkspace.is_owner"
            as="div"
            value="1"
            class="flex flex-row gap-1 items-center justify-center"
          >
            <span>Pending Invitations</span>
            <Badge :value="invitations.length" severity="secondary" size="small" />
          </Tab>
        </TabList>
        <TabPanels>
          <TabPanel value="0">
            <ul class="flex flex-col gap-4">
              <li
                v-for="member in teamMembers"
                :key="member.id"
                class="flex items-center justify-between"
              >
                <div class="flex flex-row items-center justify-start gap-2">
                  <UserAvatar :user="member" class="w-8 h-8" />
                  <div class="flex flex-col items-start justify-center">
                    <span> {{ member.display_name }}</span>
                    <span class="text-xs text-gray-400 dark:text-gray-500">{{ member.email }}</span>
                  </div>
                  <Tag
                    v-if="currentWorkspace.owner === member.id"
                    value="Owner"
                    severity="danger"
                  />
                  <Tag v-if="usersStore.me?.id === member.id" value="You" />
                </div>
                <div>
                  <Button
                    v-if="currentWorkspace.is_owner && usersStore.me?.id !== member.id"
                    type="button"
                    icon="pi pi-trash"
                    severity="danger"
                    v-tooltip.right="{ value: 'Remove member', showDelay: 300, hideDelay: 300 }"
                  />
                </div>
              </li>
            </ul>
          </TabPanel>
          <TabPanel value="1" v-if="currentWorkspace.is_owner" class="flex flex-col gap-4">
            <div class="flex flex-col gap-2">
              <span class="font-semibold">Create Invitation</span>
              <InputGroup>
                <InputText
                  id="edit-workspace-dialog__invite__field-email"
                  class="flex-auto"
                  autocomplete="off"
                  placeholder="your-teammate@email.com"
                  @update:modelValue="inviteFormErrors.email = []"
                  v-model="inviteForm.email"
                  :invalid="
                    typeof inviteFormErrors.email !== 'undefined' &&
                    inviteFormErrors.email.length > 0
                  "
                />
                <Button
                  type="button"
                  icon="pi pi-users"
                  label="Invite"
                  severity="primary"
                  @click="handleInvite"
                  :loading="isInviting"
                  :disabled="!currentWorkspace.is_owner"
                />
              </InputGroup>
              <div
                v-if="
                  typeof inviteFormErrors.email !== 'undefined' && inviteFormErrors.email.length > 0
                "
                class="text-red-500 text-sm"
              >
                <span v-for="(error, i) in inviteFormErrors.email" :key="i">{{ error }}</span>
              </div>
            </div>
            <ul class="flex flex-col gap-2">
              <li
                v-for="invitation in invitations"
                :key="invitation.id"
                class="flex items-center justify-between"
              >
                <div class="flex flex-row items-center justify-start gap-2">
                  <span>{{ invitation.email }}</span>
                </div>
                <div class="flex flex-row gap-2">
                  <Button
                    type="button"
                    icon="pi pi-copy"
                    severity="secondary"
                    v-tooltip.right="{
                      value: 'Copy invitation link',
                      showDelay: 300,
                      hideDelay: 300
                    }"
                    @click="
                      () => {
                        handleCopyInvitationLink(invitation.id)
                      }
                    "
                  />
                  <Button
                    type="button"
                    icon="pi pi-trash"
                    text
                    severity="danger"
                    v-tooltip.right="{ value: 'Cancel invitation', showDelay: 300, hideDelay: 300 }"
                    @click="
                      () => {
                        handleCancelInvitation(invitation.id)
                      }
                    "
                  />
                </div>
              </li>
            </ul>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </div>
    <div class="flex justify-between items-center gap-2 mt-8">
      <div class="flex justify-start items-center gap-2">
        <Button type="button" severity="secondary" label="Cancel" @click="handleCancel" />
        <Button
          v-if="currentWorkspace.is_owner"
          type="button"
          label="Delete"
          severity="danger"
          @click="confirmDelete()"
          :loading="isDeleting"
        />
      </div>
      <Button type="button" label="Update" @click="handleSubmit" :loading="isSubmitting" />
    </div>
  </Dialog>
  <ConfirmDialog />
  <Toast group="clipboard" successIcon="pi pi-clipboard" />
</template>
