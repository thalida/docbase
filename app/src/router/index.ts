import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import DashboardLayout from '@/views/dashboard/_layout.vue'
import IndexView from '@/views/IndexView.vue'
import LoginView from '@/views/auth/LoginView.vue'
import LogoutView from '@/views/auth/LogoutView.vue'
import WorkspaceView from '@/views/dashboard/WorkspaceView.vue'
import WorkspaceSettingsView from '@/views/dashboard/WorkspaceSettingsView.vue'
import DatabaseView from '@/views/dashboard/DatabaseView.vue'
import AcceptInviteView from '@/views/AcceptInviteView.vue'

export enum ROUTES {
  INDEX = 'index',

  WORKSPACE = 'workspace',
  WORKSPACE_ACCEPT_INVITE = 'acceptInvite',
  WORKSPACE_SETTINGS = 'settings',
  DATABASE = 'database',

  LOGIN = 'login',
  LOGOUT = 'logout',
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
      },
      props: (route) => ({ redirectTo: route.query.redirectTo as string })
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
      path: '/accept-invitation',
      name: ROUTES.WORKSPACE_ACCEPT_INVITE,
      component: AcceptInviteView,
      meta: {
        requiresAuth: true,
        redirectTo: ROUTES.LOGIN
      },
      props: (route) => ({ invitation: route.query.invitation as string })
    },
    {
      path: '/ws-:workspaceId',
      component: DashboardLayout,
      meta: {
        requiresAuth: true,
        redirectTo: ROUTES.LOGIN
      },
      props(route) {
        return {
          showUserProfile:
            typeof route.query.profile === 'string' && route.query.profile.length > 0,
          profileForUser: route.query.profile
        }
      },
      children: [
        {
          path: '',
          name: ROUTES.WORKSPACE,
          component: WorkspaceView
        },
        {
          path: 'settings',
          name: ROUTES.WORKSPACE_SETTINGS,
          component: WorkspaceSettingsView
        },
        {
          path: 'db-:databaseId',
          name: ROUTES.DATABASE,
          component: DatabaseView
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

  const query = to.meta.requiresAuth ? { redirectTo: to.fullPath } : {}

  return { name: redirectTo, query }
})

export default router
