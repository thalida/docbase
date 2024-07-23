<script setup lang="ts">
import { computed } from 'vue'
import Avatar from 'primevue/avatar'
import { $dt } from '@primevue/themes'
import type { IWorkspace } from '@/types/workspaces'

const props = defineProps<{
  workspace: IWorkspace
}>()

const colorMap: Record<string, string> = {
  A: 'red.500',
  B: 'orange.500',
  C: 'amber.500',
  D: 'yellow.500',
  E: 'lime.500',
  F: 'green.500',
  G: 'emerald.500',
  H: 'teal.500',
  I: 'cyan.500',
  J: 'sky.500',
  K: 'blue.500',
  L: 'indigo.500',
  M: 'violet.500',
  N: 'purple.500',
  O: 'fuchsia.500',
  P: 'pink.500',
  Q: 'rose.500',
  R: 'red.800',
  S: 'orange.800',
  T: 'amber.800',
  U: 'yellow.800',
  V: 'lime.800',
  W: 'green.800',
  X: 'emerald.800',
  Y: 'teal.800',
  Z: 'cyan.800'
}
const label = computed(() => props.workspace.name[0].toUpperCase())
const color = computed(() => colorMap[label.value] || 'gray.500')
</script>

<template>
  <Avatar
    v-bind="$attrs"
    :label="label"
    class="flex-shrink-0"
    :style="`background-color: ${$dt(color).value}; color: #fff;`"
  />
</template>
