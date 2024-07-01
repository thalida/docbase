import { ref, watchEffect } from 'vue'
import { defineStore } from 'pinia'
import { LOCALSTOARGE_NAMESPACE } from '.'
import type { ColorScheme, Theme } from '@/types/ui'
import { useAuthStore } from './auth'
import { useUsersStore } from './users'
import auth from '@/api/auth'

export const useUIStore = defineStore('ui', () => {
  const authStore = useAuthStore()
  const usersStore = useUsersStore()

  const THEME_STORAGE_KEY = `${LOCALSTOARGE_NAMESPACE}theme`
  const supportedThemes = ['light', 'dark', 'system'] as const
  const theme = ref<Theme>('system')
  const colorScheme = ref<ColorScheme>()

  const isReady = ref(false)

  async function setup() {
    isReady.value = false

    const theme = (localStorage.getItem(THEME_STORAGE_KEY) as Theme) || 'system'
    setTheme(theme)
    window
      .matchMedia('(prefers-color-scheme: dark)')
      .addEventListener('change', handleColorSchemeChange)

    await authStore.silentLogin()

    if (authStore.isAuthenticated) {
      await usersStore.fetchMe()
    }

    isReady.value = true
  }

  function setTheme(newTheme: Theme) {
    theme.value = newTheme

    if (
      theme.value === 'dark' ||
      (theme.value === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)
    ) {
      colorScheme.value = 'dark'
      document.documentElement.classList.add('dark')
      document.documentElement
        .querySelector('meta[name="theme-color"]')
        ?.setAttribute('content', '#0f172a')
    } else {
      colorScheme.value = 'light'
      document.documentElement.classList.remove('dark')
      document.documentElement
        .querySelector('meta[name="theme-color"]')
        ?.setAttribute('content', '#dbeafe')
    }

    if (theme.value === 'system') {
      localStorage.removeItem(THEME_STORAGE_KEY)
    } else {
      localStorage.setItem(THEME_STORAGE_KEY, theme.value)
    }
  }

  function handleColorSchemeChange() {
    if (theme.value !== 'system') {
      return
    }

    setTheme('system')
  }

  function $resetAll() {
    usersStore.$reset()
  }

  return {
    isReady,
    setup,

    theme,
    setTheme,
    supportedThemes,
    colorScheme,

    $resetAll
  }
})
