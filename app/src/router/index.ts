import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'
import LoginView from '@/views/LoginView.vue'
import LogoutView from '@/views/LogoutView.vue'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'

export enum ROUTES {
  DASHBOARD = 'dashboard',
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
      name: ROUTES.DASHBOARD,
      component: DashboardView,
      meta: {
        requiresAuth: true,
        redirectTo: ROUTES.LOGIN
      }
    },
    {
      path: '/login',
      name: ROUTES.LOGIN,
      component: LoginView,
      meta: {
        requiresAuth: false,
        redirectTo: ROUTES.DASHBOARD
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
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // },
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
