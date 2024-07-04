import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { IAuthTokenResponse } from '@/types/auth'
import api from '@/api'
import { LOCALSTOARGE_NAMESPACE } from '.'

export const useAuthStore = defineStore('auth', () => {
  const TOKEN_STORAGE_KEY = `${LOCALSTOARGE_NAMESPACE}:tokenData`
  const isAuthenticated = ref(false)

  function setTokenData(data: IAuthTokenResponse) {
    localStorage.setItem(TOKEN_STORAGE_KEY, JSON.stringify(data))

    isAuthenticated.value = true
  }

  function getTokenData() {
    const data = localStorage.getItem(TOKEN_STORAGE_KEY)

    if (data) {
      return JSON.parse(data) as IAuthTokenResponse
    }

    return null
  }

  function clearTokenData() {
    localStorage.removeItem(TOKEN_STORAGE_KEY)
    isAuthenticated.value = false
  }

  async function logout() {
    const tokenDataCopy = getTokenData()

    clearTokenData()

    if (tokenDataCopy !== null) {
      await api.auth.revokeToken(tokenDataCopy)
    }
  }

  async function silentLogin() {
    const tokenData = getTokenData()

    if (tokenData === null) {
      clearTokenData()
      return
    }

    try {
      const res = await api.auth.refreshToken(tokenData.refresh_token)
      setTokenData(res.data)
    } catch (error) {
      clearTokenData()
    }
  }

  async function loginWithGoogle(accessToken: string) {
    try {
      const res = await api.auth.googleLogin(accessToken)
      setTokenData(res.data)
    } catch (error) {
      clearTokenData()
      throw error
    }
  }

  function $reset() {
    clearTokenData()
  }

  return {
    isAuthenticated,
    setTokenData,
    getTokenData,
    clearTokenData,
    logout,
    silentLogin,
    loginWithGoogle,

    $reset
  }
})
