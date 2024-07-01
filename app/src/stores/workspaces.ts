import { ref } from 'vue'
import { defineStore } from 'pinia'
// import $workspaces from '@/api/workspaces'
import type { IWorkspace } from '@/types/workspaces'

// export const useWorkspacesStore = defineStore('workspaces', () => {
//   const me = ref<IWorkspace | null>(null)

//   async function fetchMe() {
//     const res = await $workspaces.fetchMe()
//     me.value = res.data
//   }

//   function $reset() {
//     me.value = null
//   }

//   return {
//     me,
//     fetchMe,

//     $reset
//   }
// })
