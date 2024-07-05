<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useWorkspacesStore } from '@/stores/workspaces'
import type { IWorkspaceCreateRequest } from '@/types/workspaces'
import { ROUTES } from '@/router'

const router = useRouter()
const emits = defineEmits(['update:visible'])
const workspacesStore = useWorkspacesStore()

const isSubmitting = ref(false)
const newWorkspaceForm = ref<IWorkspaceCreateRequest>({
  name: '',
  is_default: false
})
const errors = ref<Record<string, string[]>>({})

function reset() {
  errors.value = {}
  newWorkspaceForm.value = {
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
    const res = await workspacesStore.createOne(newWorkspaceForm.value)
    router.push({ name: ROUTES.WORKSPACE, params: { workspaceId: res.id } })
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
          v-model="newWorkspaceForm.name"
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
          <label for="create-workspace-dialog__field-is-default" class="font-semibold"
            >Make default?</label
          >
          <i
            class="pi pi-question-circle"
            v-tooltip.bottom="'Make this workspace your default dashboard'"
          />
        </div>
        <ToggleSwitch
          inputId="create-workspace-dialog__field-is-default"
          v-model="newWorkspaceForm.is_default"
        />
      </div>
    </div>
    <div class="flex justify-between items-center gap-2 mt-8">
      <Button type="button" label="Cancel" severity="secondary" @click="handleCancel"></Button>
      <Button type="button" label="Create" @click="handleSubmit" :loading="isSubmitting" />
    </div>
  </Dialog>
</template>
