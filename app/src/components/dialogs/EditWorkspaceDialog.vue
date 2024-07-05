<script setup lang="ts">
import { computed } from 'vue'
import { useWorkspacesStore } from '@/stores/workspaces'

const props = defineProps<{
  workspaceId: string
}>()
const emits = defineEmits(['update:visible'])

const workspacesStore = useWorkspacesStore()
const currentWorkspace = computed(() => workspacesStore.getOne(props.workspaceId))
function handleCancel() {
  emits('update:visible', false)
}

function handleSave() {
  emits('update:visible', false)
}
</script>

<template>
  <Dialog
    v-if="typeof currentWorkspace !== 'undefined' && currentWorkspace !== null"
    modal
    :header="`Edit ${currentWorkspace.name}`"
    v-bind="$attrs"
    @update:visible="emits('update:visible')"
    :style="{ width: '25rem' }"
  >
    <span class="text-surface-500 dark:text-surface-400 block mb-8">Update your information.</span>
    <div class="flex items-center gap-4 mb-4">
      <label for="username" class="font-semibold w-24">Username</label>
      <InputText id="username" class="flex-auto" autocomplete="off" />
    </div>
    <div class="flex items-center gap-4 mb-8">
      <label for="email" class="font-semibold w-24">Email</label>
      <InputText id="email" class="flex-auto" autocomplete="off" />
    </div>
    <div class="flex justify-end gap-2">
      <Button type="button" label="Cancel" severity="secondary" @click="handleCancel"></Button>
      <Button type="button" label="Save" @click="handleSave"></Button>
    </div>
  </Dialog>
</template>
