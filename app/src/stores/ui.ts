import { ref } from 'vue'
import { defineStore } from 'pinia'
import { palette as primevuePalette, updatePreset } from '@primevue/themes'
import { LOCALSTOARGE_NAMESPACE } from '.'
import type { ColorScheme, Theme } from '@/types/ui'
import { useAuthStore } from './auth'
import { useUsersStore } from './users'
import { useWorkspacesStore } from './workspaces'
import { useDatabasesStore } from './databases'
import { useWorkspaceInvitationsStore } from './workspaceInvitations'
import { useRealtimeStore } from './realtime'

export const useUIStore = defineStore('ui', () => {
  const authStore = useAuthStore()
  const usersStore = useUsersStore()
  const workspacesStore = useWorkspacesStore()
  const databasesStore = useDatabasesStore()
  const workspaceInvitationsStore = useWorkspaceInvitationsStore()
  const realtimeStore = useRealtimeStore()

  const THEME_STORAGE_KEY = `${LOCALSTOARGE_NAMESPACE}:theme`
  const PALETTE_STORAGE_KEY = `${LOCALSTOARGE_NAMESPACE}:palette`
  const UI_SIDEBAR_STATE_KEY = `${LOCALSTOARGE_NAMESPACE}:sidebarOpenState`

  const supportedThemes = ['light', 'dark', 'system'] as const
  const defaultTheme = 'system'
  const theme = ref<Theme>(defaultTheme)
  const colorScheme = ref<ColorScheme>()
  const supportedPalettes = [
    'red',
    'orange',
    'amber',
    'yellow',
    'lime',
    'green',
    'emerald',
    'teal',
    'cyan',
    'sky',
    'blue',
    'indigo',
    'violet',
    'purple',
    'fuchsia',
    'pink',
    'rose',
    'slate',
    'stone',
    'contrast'
  ]
  const defaultPalette = 'blue'
  const palette = ref(defaultPalette)

  const isSidebarOpen = ref(true)

  const isReady = ref(false)

  async function setup() {
    isReady.value = false

    const theme = (localStorage.getItem(THEME_STORAGE_KEY) as Theme) || defaultTheme
    setTheme(theme)
    window
      .matchMedia('(prefers-color-scheme: dark)')
      .addEventListener('change', handleDeviceColorSchemeChange)

    const palette = (localStorage.getItem(PALETTE_STORAGE_KEY) as string) || defaultPalette
    setPalette(palette)

    const isMobile = window.innerWidth < 768
    if (isMobile) {
      setIsSidebarOpen(false)
    } else {
      const sidebarOpenState = localStorage.getItem(UI_SIDEBAR_STATE_KEY)
      setIsSidebarOpen(sidebarOpenState ? sidebarOpenState === 'true' : true)
    }

    await authStore.silentLogin()

    if (authStore.isAuthenticated) {
      const promises = [
        realtimeStore.connect(),
        usersStore.fetchMe(),
        workspacesStore.fetchAll(),
        workspaceInvitationsStore.fetchAll({ email: usersStore.me?.email })
      ]

      await Promise.all(promises)
    }

    isReady.value = true
  }

  function setIsSidebarOpen(value: boolean) {
    isSidebarOpen.value = value
  }

  function toggleSidebarStore() {
    setIsSidebarOpen(!isSidebarOpen.value)
    localStorage.setItem(UI_SIDEBAR_STATE_KEY, isSidebarOpen.value.toString())
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

  function handleDeviceColorSchemeChange() {
    if (theme.value !== 'system') {
      return
    }

    setTheme('system')
  }

  function setPalette(newPalette: string) {
    const isValid = supportedPalettes.includes(newPalette)

    if (!isValid) {
      newPalette = defaultPalette
    }

    palette.value = newPalette

    let paletteConfig = {}
    if (newPalette === 'contrast') {
      paletteConfig = {
        primary: {
          50: '{zinc.50}',
          100: '{zinc.100}',
          200: '{zinc.200}',
          300: '{zinc.300}',
          400: '{zinc.400}',
          500: '{zinc.500}',
          600: '{zinc.600}',
          700: '{zinc.700}',
          800: '{zinc.800}',
          900: '{zinc.900}',
          950: '{zinc.950}'
        },
        colorScheme: {
          light: {
            surface: {
              0: '#ffffff',
              50: '{slate.50}',
              100: '{slate.100}',
              200: '{slate.200}',
              300: '{slate.300}',
              400: '{slate.400}',
              500: '{slate.500}',
              600: '{slate.600}',
              700: '{slate.700}',
              800: '{slate.800}',
              900: '{slate.900}',
              950: '{slate.950}'
            },
            primary: {
              color: '{zinc.950}',
              inverseColor: '#ffffff',
              hoverColor: '{zinc.900}',
              activeColor: '{zinc.800}'
            },
            highlight: {
              background: '{zinc.950}',
              focusBackground: '{zinc.700}',
              color: '#ffffff',
              focusColor: '#ffffff'
            }
          },
          dark: {
            surface: {
              0: '#ffffff',
              50: '{slate.50}',
              100: '{slate.100}',
              200: '{slate.200}',
              300: '{slate.300}',
              400: '{slate.400}',
              500: '{slate.500}',
              600: '{slate.600}',
              700: '{slate.700}',
              800: '{slate.800}',
              900: '{slate.900}',
              950: '{slate.950}'
            },
            primary: {
              color: '{zinc.50}',
              inverseColor: '{zinc.950}',
              hoverColor: '{zinc.100}',
              activeColor: '{zinc.200}'
            },
            highlight: {
              background: 'rgba(250, 250, 250, .16)',
              focusBackground: 'rgba(250, 250, 250, .24)',
              color: 'rgba(255,255,255,.87)',
              focusColor: 'rgba(255,255,255,.87)'
            }
          }
        }
      }
    } else {
      paletteConfig = {
        primary: primevuePalette(`{${newPalette}}`),
        colorScheme: {
          light: {
            surface: {
              0: '#ffffff',
              50: '{slate.50}',
              100: '{slate.100}',
              200: '{slate.200}',
              300: '{slate.300}',
              400: '{slate.400}',
              500: '{slate.500}',
              600: '{slate.600}',
              700: '{slate.700}',
              800: '{slate.800}',
              900: '{slate.900}',
              950: '{slate.950}'
            },
            primary: {
              color: '{primary.500}',
              contrastColor: '#ffffff',
              hoverColor: '{primary.600}',
              activeColor: '{primary.700}'
            },
            highlight: {
              background: '{primary.50}',
              focusBackground: '{primary.100}',
              color: '{primary.700}',
              focusColor: '{primary.800}'
            }
          },
          dark: {
            surface: {
              0: '#ffffff',
              50: '{slate.50}',
              100: '{slate.100}',
              200: '{slate.200}',
              300: '{slate.300}',
              400: '{slate.400}',
              500: '{slate.500}',
              600: '{slate.600}',
              700: '{slate.700}',
              800: '{slate.800}',
              900: '{slate.900}',
              950: '{slate.950}'
            },
            primary: {
              color: '{primary.400}',
              contrastColor: '{surface.900}',
              hoverColor: '{primary.300}',
              activeColor: '{primary.200}'
            },
            highlight: {
              background: 'color-mix(in srgb, {primary.400}, transparent 84%)',
              focusBackground: 'color-mix(in srgb, {primary.400}, transparent 76%)',
              color: 'rgba(255,255,255,.87)',
              focusColor: 'rgba(255,255,255,.87)'
            }
          }
        }
      }
    }
    updatePreset({
      semantic: {
        ...paletteConfig
      }
    })
    localStorage.setItem(PALETTE_STORAGE_KEY, palette.value)
  }

  function $resetAll() {
    databasesStore.$reset()
    workspacesStore.$reset()
    usersStore.$reset()
    authStore.$reset()
  }

  return {
    isReady,
    setup,

    theme,
    setTheme,
    colorScheme,
    palette,
    setPalette,
    supportedThemes,
    supportedPalettes,

    isSidebarOpen,
    setIsSidebarOpen,
    toggleSidebarStore,

    $resetAll
  }
})
