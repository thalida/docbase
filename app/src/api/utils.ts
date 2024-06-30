import { useAuthStore } from '@/stores/auth'

export function getHeaders() {
  const authStore = useAuthStore()
  return {
    'Content-Type': 'application/json',
    Authorization: `${authStore.getTokenData()?.token_type} ${authStore.getTokenData()?.access_token}`
  }
}

export default {
  getHeaders
}
