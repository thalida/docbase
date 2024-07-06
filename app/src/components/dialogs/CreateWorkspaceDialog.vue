<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import isEmail from 'validator/es/lib/isEmail'
import { useWorkspacesStore } from '@/stores/workspaces'
import { useUsersStore } from '@/stores/users'
import type { IWorkspaceCreateRequest } from '@/types/workspaces'
import type { IUser } from '@/types/users'
import UserAvatar from '@/components/ui/UserAvatar.vue'
import { ROUTES } from '@/router'
import type { AutoCompleteCompleteEvent } from 'primevue/autocomplete'

const router = useRouter()
const emits = defineEmits(['update:visible'])
const workspacesStore = useWorkspacesStore()
const usersStore = useUsersStore()

const isSubmitting = ref(false)
const form = ref<IWorkspaceCreateRequest>({
  name: '',
  is_default: false,
  members: []
})
const errors = ref<Record<string, string[]>>({})

const teamMembers = ref<IUser[]>([])

onMounted(async () => {
  await usersStore.fetchAll()
  teamMembers.value = usersStore.getAll()
})

const handleTeamMembersSearch = (event: AutoCompleteCompleteEvent) => {
  const cleanedQuery = event.query.trim().toLowerCase()

  teamMembers.value = usersStore
    .getAll()
    .filter(
      (user) =>
        user.email.toLowerCase().includes(cleanedQuery) ||
        user.first_name.toLowerCase().includes(cleanedQuery) ||
        user.last_name.toLowerCase().includes(cleanedQuery)
    )

  if (teamMembers.value.length > 0 || !isEmail(cleanedQuery) || cleanedQuery.length === 0) {
    return
  }

  teamMembers.value.push({
    id: cleanedQuery,
    email: cleanedQuery,
    display_name: cleanedQuery,
    initials: cleanedQuery[0],
    first_name: 'null',
    last_name: 'null',
    avatar: '',
    new: true
  } as IUser)
}

function reset() {
  errors.value = {}
  form.value = {
    name: '',
    is_default: false,
    members: []
  }
}

function handleCancel() {
  reset()
  emits('update:visible', false)
}

async function handleSubmit() {
  isSubmitting.value = true
  try {
    const res = await workspacesStore.create(form.value)
    reset()
    router.push({ name: ROUTES.WORKSPACE, params: { workspaceId: res.id } })
    emits('update:visible', false)
  } catch (e: any) {
    errors.value = e.response.data
  } finally {
    isSubmitting.value = false
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
    modal
    header="Create Workspace"
    v-bind="$attrs"
    @update:visible="onVisibleChange"
    :style="{ width: '25rem' }"
  >
    <div class="flex flex-col gap-4">
      <div class="flex flex-col gap-2">
        <label for="create-workspace-dialog__field-name" class="font-semibold"> Name </label>
        <InputText
          id="create-workspace-dialog__field-name"
          class="flex-auto"
          autocomplete="off"
          placeholder="My Awesome Workspace"
          v-model="form.name"
          :invalid="typeof errors.name !== 'undefined' && errors.name.length > 0"
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
          <label for="create-workspace-dialog__field-is-default" class="font-semibold">
            Make default?
          </label>
          <i
            class="pi pi-question-circle"
            v-tooltip.bottom="'Make this workspace your default dashboard'"
          />
        </div>
        <ToggleSwitch
          inputId="create-workspace-dialog__field-is-default"
          v-model="form.is_default"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for="create-workspace-dialog__field-members" class="font-semibold">
          Team Members
        </label>
        <AutoComplete
          inputId="create-workspace-dialog__field-members"
          v-model="form.members"
          optionValue="id"
          optionLabel="email"
          fluid
          multiple
          :suggestions="teamMembers"
          @complete="handleTeamMembersSearch"
        >
          <template #option="slotProps">
            <div v-if="slotProps.option.new" class="flex flex-row items-center gap-2">
              <span>Invite {{ slotProps.option.email }}</span>
            </div>
            <div v-else class="flex flex-row items-center gap-2">
              <UserAvatar :user="slotProps.option" class="mr-2" />
              <div class="flex flex-col justify-center">
                <span>{{ slotProps.option.display_name }}</span>
                <span class="text-xs">{{ slotProps.option.email }}</span>
              </div>
            </div>
          </template>
        </AutoComplete>
      </div>
    </div>
    <div class="flex justify-between items-center gap-2 mt-8">
      <Button type="button" label="Cancel" severity="secondary" @click="handleCancel"></Button>
      <Button type="button" label="Create" @click="handleSubmit" :loading="isSubmitting" />
    </div>
  </Dialog>
</template>
