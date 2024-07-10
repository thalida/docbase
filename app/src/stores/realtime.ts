import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import Spaces, { type LocationsEvents, type Space, type SpaceMember } from '@ably/spaces'
import Ably from 'ably'
import api from '@/api'
import { useUsersStore } from './users'

export const useRealtimeStore = defineStore('realtime', () => {
  const usersStore = useUsersStore()
  const client = ref<Ably.Types.RealtimePromise | null>(null)
  const spacesClient = ref<Spaces | null>(null)
  const spaces = ref<Record<string, Space>>({})
  const spaceMembers = ref<Record<string, SpaceMember[]>>({})
  const mySpaceMembers = ref<Record<string, SpaceMember>>({})

  const getMembersBySpace = computed(() => (spaceName: string) => {
    return spaceMembers.value[spaceName] ?? []
  })

  const getSelfBySpace = computed(() => (spaceName: string) => {
    return mySpaceMembers.value[spaceName]
  })

  async function connect() {
    client.value = new Ably.Realtime.Promise({
      key: import.meta.env.VITE_ABLY_API_KEY,
      authCallback: async (tokenParams, callback) => {
        try {
          const res = await api.auth.ablyToken()
          callback(null, res.data)
        } catch (error: any) {
          callback(error, null)
        }
      }
    })

    await client.value.auth.createTokenRequest()
    spacesClient.value = new Spaces(client.value)
  }

  async function getSpace(workspaceId: string) {
    const spaceId = _getSpaceId(workspaceId)
    const foundSpace = spaces.value[spaceId]

    if (foundSpace) {
      return foundSpace
    }

    const newSpace = await spacesClient.value?.get(spaceId)
    if (!newSpace) {
      return
    }

    spaces.value[spaceId] = newSpace
    return spaces.value[spaceId]
  }

  async function enterSpace(workspaceId: string) {
    const space = await getSpace(workspaceId)
    if (!space) {
      return
    }

    await space.enter()
    spaceMembers.value[space.name] = await space.members.getAll()

    const self = await space.members.getSelf()
    if (self) {
      mySpaceMembers.value[space.name] = self
    }

    _subscribe(space)
  }

  async function leaveSpace(workspaceId: string) {
    const space = await getSpace(workspaceId)
    if (!space) {
      return
    }

    space.leave()

    delete mySpaceMembers.value[space.name]

    _unsubscribe(space)
  }

  async function setSpaceLocation(workspaceId: string, location: unknown) {
    const space = await getSpace(workspaceId)
    if (!space) {
      return
    }

    space.locations.set(location)
  }

  function _getSpaceId(workspaceId: string) {
    const workspaceSpaceId = `workspace:${workspaceId}`
    return `${workspaceSpaceId}`
  }

  function _subscribe(space: Space) {
    space.members.subscribe(['enter', 'leave'], (member) => {
      _onSpaceMemberUpdate(member, space.name)
    })
    space.locations.subscribe('update', (location) => {
      _onSpaceLocationUpdate(location, space.name)
    })
  }

  function _unsubscribe(space: Space) {
    space.members.unsubscribe()
    space.locations.unsubscribe()
  }

  async function _onSpaceMemberUpdate(member: SpaceMember, spaceName: string) {
    const space = await getSpace(spaceName)

    if (!space) {
      return
    }

    spaceMembers.value[spaceName] = spaceMembers.value[spaceName] || []

    const lastEvent = member.lastEvent
    if (lastEvent.name === 'enter') {
      await usersStore.getOrFetch(member.clientId)

      const foundIndex = spaceMembers.value[spaceName].findIndex(
        (m) => m.clientId === member.clientId && m.connectionId === member.connectionId
      )
      if (foundIndex > -1) {
        spaceMembers.value[spaceName][foundIndex] = member
      } else {
        spaceMembers.value[spaceName].push(member)
      }
      return
    }

    if (lastEvent.name === 'leave') {
      spaceMembers.value[spaceName] =
        spaceMembers.value[spaceName]?.filter(
          (m) => !(m.clientId === member.clientId && m.connectionId === member.connectionId)
        ) ?? []
      return
    }

    console.log('Member updated:', member, spaceName, lastEvent)
  }

  async function _onSpaceLocationUpdate(location: LocationsEvents.UpdateEvent, spaceName: string) {
    const space = await getSpace(spaceName)

    if (!space) {
      return
    }

    spaceMembers.value[spaceName] = spaceMembers.value[spaceName] || []
    const member = location.member
    const foundIndex = spaceMembers.value[spaceName].findIndex(
      (m) => m.clientId === member.clientId && m.connectionId === member.connectionId
    )
    if (foundIndex > -1) {
      spaceMembers.value[spaceName][foundIndex] = member
    } else {
      spaceMembers.value[spaceName].push(member)
    }
  }

  return {
    client,
    spacesClient,

    connect,

    spaces,
    spaceMembers,
    mySpaceMembers,

    getSpace,
    enterSpace,
    leaveSpace,
    setSpaceLocation,

    getMembersBySpace,
    getSelfBySpace
  }
})
