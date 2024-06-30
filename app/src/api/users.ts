import api from './index'
import { getHeaders } from './utils'

export function fetchMe() {
  return api.get('/users/me/', {
    headers: getHeaders()
  })
}

export default {
  fetchMe
}
