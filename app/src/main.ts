import 'primeicons/primeicons.css'
import './main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import vue3GoogleLogin from 'vue3-google-login'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import ConfirmationService from 'primevue/confirmationservice'

import App from './App.vue'
import router from './router'
import { definePreset } from '@primevue/themes'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vue3GoogleLogin, {
  clientId: import.meta.env.VITE_GOOGLE_OAUTH2_CLIENT_ID
})

const MyTheme = definePreset(Aura, {
  semantic: {
    // primary: {
    //   50: '{indigo.50}',
    //   100: '{indigo.100}',
    //   200: '{indigo.200}',
    //   300: '{indigo.300}',
    //   400: '{indigo.400}',
    //   500: '{indigo.500}',
    //   600: '{indigo.600}',
    //   700: '{indigo.700}',
    //   800: '{indigo.800}',
    //   900: '{indigo.900}',
    //   950: '{indigo.950}'
    // },
    primary: {
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
    colorScheme: {
      light: {
        surface: {
          0: '#ffffff',
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
        primary: {
          color: '{primary.950}',
          contrastColor: '{primary.50}',
          hoverColor: '{primary.800}',
          activeColor: '{primary.700}',
          secondaryColor: '{primary.100}'
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
          color: '{primary.50}',
          contrastColor: '{primary.950}',
          hoverColor: '{primary.200}',
          activeColor: '{primary.300}',
          secondaryColor: '{primary.500}'
        }
      }
    }
  }
})
app.use(PrimeVue, {
  theme: {
    preset: MyTheme,
    options: {
      darkModeSelector: '.dark'
    }
  },
  ripple: true
})
app.use(ConfirmationService)

app.mount('#app')
