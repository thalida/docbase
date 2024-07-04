import 'primeicons/primeicons.css'
import './main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import vue3GoogleLogin from 'vue3-google-login'

import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
// import PrimeVue from 'primevue/config'
import Tooltip from 'primevue/tooltip'

import App from './App.vue'
import router from './router'
// @ts-ignore
// import AuraTheme from './themes/aura'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vue3GoogleLogin, {
  clientId: import.meta.env.VITE_GOOGLE_OAUTH2_CLIENT_ID
})

// app.use(PrimeVue, {
//   unstyled: true,
//   pt: AuraTheme
// })
app.use(PrimeVue, {
  theme: {
    preset: Aura
  }
})
app.directive('tooltip', Tooltip)

app.mount('#app')
