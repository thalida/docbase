<script setup lang="ts">
import { ref } from 'vue'
import { googleTokenLogin } from 'vue3-google-login'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ROUTES } from '@/router'
import { useUIStore } from '@/stores/ui'

const props = defineProps<{
  redirectTo?: string | null | undefined
}>()
const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUIStore()
const error = ref<string | null>(null)

async function handleGoogleLogin() {
  try {
    error.value = null
    const response = await googleTokenLogin()
    await authStore.loginWithGoogle(response.access_token)
    await uiStore.setup()

    if (props.redirectTo) {
      router.push(props.redirectTo)
      return
    }

    router.push({ name: ROUTES.INDEX })
  } catch (e) {
    console.error(e)
    error.value = 'Failed to login with Google'
  }
}
</script>

<template>
  <main class="flex flex-col min-h-full flex-1 md:flex-row text-color">
    <div
      class="flex flex-1 flex-col justify-center px-4 py-12 sm:px-6 lg:flex-none lg:px-20 xl:px-24"
    >
      <div class="mx-auto w-full max-w-sm lg:w-96">
        <div>
          <img
            class="h-10 w-auto"
            src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600"
            alt="Your Company"
          />
          <h2 class="mt-8 text-2xl font-bold leading-9 tracking-tight text-color">
            Sign in to your account
          </h2>
        </div>

        <div
          v-if="error"
          class="mt-4 flex flex-row items-center justify-start gap-2 rounded-md bg-red-50 p-4 sm:mx-auto sm:w-full sm:max-w-sm dark:bg-red-200"
        >
          <i
            class="flex-shrink-0 pi pi-times-circle text-red-400 dark:text-red-600"
            aria-hidden="true"
          />
          <p class="text-sm font-medium text-red-800">
            {{ error }}
          </p>
        </div>

        <div class="flex flex-col mt-10 gap-4">
          <button
            @click="handleGoogleLogin"
            class="flex w-full items-center justify-center gap-3 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus-visible:ring-transparent"
          >
            <svg class="h-5 w-5" aria-hidden="true" viewBox="0 0 24 24">
              <path
                d="M12.0003 4.75C13.7703 4.75 15.3553 5.36002 16.6053 6.54998L20.0303 3.125C17.9502 1.19 15.2353 0 12.0003 0C7.31028 0 3.25527 2.69 1.28027 6.60998L5.27028 9.70498C6.21525 6.86002 8.87028 4.75 12.0003 4.75Z"
                fill="#EA4335"
              />
              <path
                d="M23.49 12.275C23.49 11.49 23.415 10.73 23.3 10H12V14.51H18.47C18.18 15.99 17.34 17.25 16.08 18.1L19.945 21.1C22.2 19.01 23.49 15.92 23.49 12.275Z"
                fill="#4285F4"
              />
              <path
                d="M5.26498 14.2949C5.02498 13.5699 4.88501 12.7999 4.88501 11.9999C4.88501 11.1999 5.01998 10.4299 5.26498 9.7049L1.275 6.60986C0.46 8.22986 0 10.0599 0 11.9999C0 13.9399 0.46 15.7699 1.28 17.3899L5.26498 14.2949Z"
                fill="#FBBC05"
              />
              <path
                d="M12.0004 24.0001C15.2404 24.0001 17.9654 22.935 19.9454 21.095L16.0804 18.095C15.0054 18.82 13.6204 19.245 12.0004 19.245C8.8704 19.245 6.21537 17.135 5.2654 14.29L1.27539 17.385C3.25539 21.31 7.3104 24.0001 12.0004 24.0001Z"
                fill="#34A853"
              />
            </svg>
            <span class="text-sm font-semibold leading-6">Continue with Google</span>
          </button>
        </div>
      </div>
    </div>
    <div class="relative block flex-1 md:w-0">
      <img
        class="absolute inset-0 h-full w-full object-cover"
        src="https://images.unsplash.com/photo-1496917756835-20cb06e75b4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1908&q=80"
        alt=""
      />
    </div>
  </main>
</template>
