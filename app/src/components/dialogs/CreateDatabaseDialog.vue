<script setup lang="ts">
const emits = defineEmits(['update:visible'])

function handleCancel() {
  emits('update:visible', false)
}

function handleSave() {
  emits('update:visible', false)
}
</script>

<template>
  <Dialog
    modal
    header="Create Database"
    v-bind="$attrs"
    @update:visible="emits('update:visible')"
    :style="{ width: '50%', minWidth: '25rem' }"
    dismissableMask
    :draggable="false"
  >
    <span class="text-color block mb-8">Update your information.</span>
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
      <Button type="button" label="Save" icon="pi pi-plus-cirlce" @click="handleSave"></Button>
    </div>
  </Dialog>
</template>
