<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useWorkspacesStore } from '@/stores/workspaces'
import type { IWorkspaceUpdateRequest } from '@/types/workspaces'

const props = defineProps<{ visible: boolean; workspaceId: string }>()
const emits = defineEmits(['update:visible'])
const workspacesStore = useWorkspacesStore()
const currentWorkspace = computed(() => workspacesStore.get(props.workspaceId))

const isSubmitting = ref(false)
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

function handleCancel() {
  reset()
  emits('update:visible', false)
}

async function handleSubmit() {
  isSubmitting.value = true
  try {
    await workspacesStore.update(props.workspaceId, form.value)
    emits('update:visible', false)
  } catch (e: any) {
    errors.value = e.response.data
  } finally {
    reset()
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
        <label for="create-workspace-dialog__field-name" class="font-semibold"> Name </label>
        <InputText
          id="create-workspace-dialog__field-name"
          class="flex-auto"
          autocomplete="off"
          placeholder="My Awesome Workspace"
          v-model="form.name"
          :invalid="typeof errors.name !== 'undefined' && errors.name.length > 0"
          :disabled="!currentWorkspace.is_owner"
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
            Is default?
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
    </div>
    <div class="flex justify-between items-center gap-2 mt-8">
      <Button type="button" label="Cancel" severity="secondary" @click="handleCancel"></Button>
      <Button type="button" label="Update" @click="handleSubmit" :loading="isSubmitting" />
    </div>
  </Dialog>
</template>
