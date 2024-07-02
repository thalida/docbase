import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import IndexView from '@/views/IndexView.vue'
import WorkspaceView from '@/views/WorkspaceView.vue'
import LoginView from '@/views/LoginView.vue'
import LogoutView from '@/views/LogoutView.vue'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'

export enum ROUTES {
  INDEX = 'index',
  WORKSPACE = 'workspace',
  CREATE_WORKSPACE = 'createWorkspace',
  LOGIN = 'login',
  LOGOUT = 'logout',
  ABOUT = 'about',
  NOT_FOUND = 'NotFound'
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: ROUTES.INDEX,
      component: IndexView
    },
    {
      path: '/login',
      name: ROUTES.LOGIN,
      component: LoginView,
      meta: {
        requiresAuth: false,
        redirectTo: ROUTES.INDEX
      }
    },
    {
      path: '/logout',
      name: ROUTES.LOGOUT,
      component: LogoutView,
      meta: {
        requiresAuth: true,
        redirectTo: ROUTES.LOGIN
      }
    },
    {
      path: '/:workspaceId',
      component: AppLayout,
      meta: {
        requiresAuth: true,
        redirectTo: ROUTES.LOGIN
      },
      children: [
        {
          path: '',
          name: ROUTES.WORKSPACE,
          component: WorkspaceView
        }
      ]
    },
    { path: '/:pathMatch(.*)*', name: 'NotFound', redirect: '/' }
  ]
})

router.beforeEach(async (to) => {
  const uiStore = useUIStore()

  if (!uiStore.isReady) {
    await uiStore.setup()
  }

  const authStore = useAuthStore()
  const requiresAuth = to.meta.requiresAuth as boolean | undefined | null
  if (typeof requiresAuth === 'undefined' || requiresAuth === null) {
    return
  }

  const isMatchingAuth = requiresAuth === authStore.isAuthenticated
  if (isMatchingAuth) {
    return
  }

  const redirectTo = to.meta.redirectTo as ROUTES
  const isCurrentRoute = to.name === redirectTo
  if (isCurrentRoute) {
    return
  }

  return { name: redirectTo }
})

export default router
