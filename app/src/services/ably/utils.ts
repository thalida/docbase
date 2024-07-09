export function getSpaceId(workspaceId: string, databaseId?: string) {
  const workspaceSpaceId = `workspace:${workspaceId}`
  const databaseSpaceId = databaseId ? `database:${databaseId}` : ''
  const seperator = databaseId ? '|' : ''

  return `${workspaceSpaceId}${seperator}${databaseSpaceId}`
}

export default {
  getSpaceId
}
