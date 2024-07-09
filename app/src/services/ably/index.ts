import Spaces from '@ably/spaces'
import Ably from 'ably'
import api from '@/api'

import * as utils from './utils'

export default class AblyInstance {
  public static client: Ably.Types.RealtimePromise | null = null
  public static spaces: Spaces

  static async connect() {
    if (AblyInstance.client) {
      return
    }

    AblyInstance.client = new Ably.Realtime.Promise({
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

    await AblyInstance.client.auth.createTokenRequest()
    AblyInstance.spaces = new Spaces(AblyInstance.client)
  }
}

export { utils }
