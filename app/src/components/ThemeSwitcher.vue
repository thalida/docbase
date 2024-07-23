<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUIStore } from '@/stores/ui'
import { $dt } from '@primevue/themes'

const props = defineProps({
  displayVariant: {
    type: String,
    default: 'icon',
    validator: (value: string) => ['icon', 'text'].includes(value)
  }
})

const uiStore = useUIStore()
const palettePopover = ref()

const colorSchemeOptions = ref([
  { value: 'light', label: 'Light', icon: 'pi pi-sun' },
  { value: 'dark', label: 'Dark', icon: 'pi pi-moon' },
  { value: 'system', label: 'System', icon: 'pi pi-desktop' }
])
const customStyles = computed(() => {
  const styles: Record<string, string> = {}

  if (props.displayVariant === 'icon') {
    styles.padding = '0'
    styles.width = '2rem'
    styles.height = '2rem'
  }

  return styles
})
const label = computed(() => {
  return uiStore.palette.charAt(0).toUpperCase() + uiStore.palette.slice(1)
})

function togglePalettePopover(event: Event) {
  palettePopover.value.toggle(event)
}
</script>

<template>
  <div>
    <Button
      v-bind="$attrs"
      type="button"
      size="small"
      :icon="uiStore.colorScheme === 'light' ? 'pi pi-sun' : 'pi pi-moon'"
      :label="displayVariant === 'icon' ? '' : label"
      text
      :class="['!p-2', {}]"
      @click="togglePalettePopover"
    />
    <Popover ref="palettePopover">
      <div class="flex flex-col gap-4 items-center justify-start">
        <SelectButton
          :modelValue="uiStore.theme"
          :options="colorSchemeOptions"
          optionLabel="label"
          optionValue="value"
          dataKey="value"
          :allowEmpty="false"
          aria-labelledby="custom"
          @change="(e) => uiStore.setTheme(e.value)"
        >
          <template #option="slotProps">
            <i :class="slotProps.option.icon"></i>
            <span>{{ slotProps.option.label }}</span>
          </template>
        </SelectButton>
        <div class="grid grid-cols-5 grid-flow-row gap-4 items-center">
          <Button
            v-for="color in uiStore.supportedPalettes"
            :key="color"
            class="w-6 h-6 place-self-center"
            icon=""
            :class="[
              color,
              {
                'outline outline-2 outline-offset-2': color === uiStore.palette
              }
            ]"
            :style="{
              backgroundColor:
                color === 'contrast'
                  ? `var(--p-button-contrast-background)`
                  : $dt(`${color}.500`).value,
              outlineColor:
                color === uiStore.palette ? `var(--p-button-contrast-border-color)` : 'transparent',
              padding: 0,
              border: 0
            }"
            @click="uiStore.setPalette(color)"
            v-tooltip.bottom="{
              value: `${color.charAt(0).toUpperCase()}${color.slice(1)}`
            }"
          />
        </div>
      </div>
    </Popover>
  </div>
</template>
