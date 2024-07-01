import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const anonClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL
})
anonClient.defaults.headers['Content-Type'] = 'application/json'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL
})
client.defaults.headers['Content-Type'] = 'application/json'
client.interceptors.request.use(function (config) {
  const authStore = useAuthStore()
  config.headers.Authorization = `${authStore.getTokenData()?.token_type} ${authStore.getTokenData()?.access_token}`
  return config
})

export default client
export { anonClient }
