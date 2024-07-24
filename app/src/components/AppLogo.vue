<script setup lang="ts">
defineProps({
  displayFormat: {
    type: String,
    default: 'full',
    validator: (value: string) => ['full', 'short'].includes(value)
  }
})
</script>

<template>
  <div class="app-logo">
    <span>{{ displayFormat === 'full' ? 'docbase' : 'db' }}</span>
  </div>
</template>

<style scoped>
.app-logo {
  font-family: 'Zain', sans-serif;
  font-size: 1.7rem;
  font-weight: 400;
  font-style: normal;
  line-height: 1;
  background-image: linear-gradient(to bottom right, var(--p-primary-300), var(--p-primary-800));
  color: transparent;
  background-clip: text;
}

.app-logo span {
  display: inline-block;
  margin-top: 0.2rem;
}
</style>
