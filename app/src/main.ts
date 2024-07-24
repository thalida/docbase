import 'primeicons/primeicons.css'
import './main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import vue3GoogleLogin from 'vue3-google-login'
import PrimeVue from 'primevue/config'
import { definePreset } from '@primevue/themes'
import Aura from '@primevue/themes/aura'
import Ripple from 'primevue/ripple'
import ConfirmationService from 'primevue/confirmationservice'
import ToastService from 'primevue/toastservice'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vue3GoogleLogin, {
  clientId: import.meta.env.VITE_GOOGLE_OAUTH2_CLIENT_ID
})

const MyTheme = definePreset(Aura)
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
app.use(ToastService)
app.directive('ripple', Ripple)

app.mount('#app')
