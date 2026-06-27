import API from "./api.js"


export async function getOrg(orgId) {
    const response = await API.get(`/orgs/${orgId}`)
    return response.ok ? await response.json() : null
}

export async function getTeams(orgId) {
    const res = await API.get(`/orgs/${orgId}/teams`)
    return res.ok ? await res.json() : []
}

export async function getProjects(orgId, teamId) {
    const res = await API.get(`/orgs/${orgId}/teams/${teamId}/projects`)
    return res.ok ? await res.json() : []
}

export async function getOrgMembers(orgId) {
    const res = await API.get(`/orgs/${orgId}/members`)
    return res.ok ? res.json() : []
}

export async function getTeamMembers(orgId, teamId) {
    const res = await API.get(`/orgs/${orgId}/teams/${teamId}/members`)
    return res.ok ? res.json() : []
}

export async function getUser(userId) {
    const res = await API.get(`/user/me`)
    return res.ok ? res.json() : console.error("failed to load user info")
}
