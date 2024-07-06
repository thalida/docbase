<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useConfirm } from 'primevue/useconfirm'
import { useWorkspacesStore } from '@/stores/workspaces'
import type { IWorkspaceUpdateRequest } from '@/types/workspaces'
import { ROUTES } from '@/router'

const props = defineProps<{ visible: boolean; workspaceId: string }>()
const emits = defineEmits(['update:visible'])
const router = useRouter()
const confirm = useConfirm()
const workspacesStore = useWorkspacesStore()
const currentWorkspace = computed(() => workspacesStore.get(props.workspaceId))

const isSubmitting = ref(false)
const isDeleting = ref(false)
const form = ref<IWorkspaceUpdateRequest>({
  name: '',
  is_default: false
})
const errors = ref<Record<string, string[]>>({})

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
    :header="`Edit Workspace: ${currentWorkspace.name}`"
    @update:visible="onVisibleChange"
    :style="{ width: '25rem' }"
  >
    <template #header>
      <div class="flex flex-row gap-2 items-center justify-start">
        <i class="pi pi-pencil" />
        <span>Editing: {{ currentWorkspace.name }}</span>
      </div>
    </template>

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
            Make default?
          </label>
          <i
            class="pi pi-question-circle"
            v-tooltip.bottom="'Make this workspace your default dashboard'"
          />
        </div>
        <ToggleSwitch inputId="edit-workspace-dialog__field-is-default" v-model="form.is_default" />
      </div>
    </div>
    <div class="flex justify-between items-center gap-2 mt-8">
      <Button
        type="button"
        label="Delete"
        severity="danger"
        @click="confirmDelete()"
        :loading="isDeleting"
        :disabled="!currentWorkspace.is_owner"
        v-tooltip.bottom="{
          value: 'Only owner\'s can delete a workspace',
          disabled: currentWorkspace.is_owner
        }"
      />
      <Button type="button" label="Update" @click="handleSubmit" :loading="isSubmitting" />
    </div>
  </Dialog>
  <ConfirmDialog />
</template>
