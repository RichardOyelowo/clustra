import API from "./api.js";

/**
 * Services module for interacting with the Clustra API.
 * Provides functions to fetch organizations, teams, projects, and user data.
 * All functions return promises and handle HTTP errors gracefully.
 *
 * @module services
 * @requires api
 *
 * @function getOrg - Get organization details by ID
 * @param {string} getOrg.orgId - The organization ID
 * @returns {Promise<Object|null>} Organization data or null if not found
 *
 * @function getTeams - Get all teams for an organization
 * @param {string} getTeams.orgId - The organization ID
 * @returns {Promise<Array>} Array of team objects or empty array on error
 *
 * @function getProjects - Get all projects for a specific team in an organization
 * @param {string} getProjects.orgId - The organization ID
 * @param {string} getProjects.teamId - The team ID
 * @returns {Promise<Array>} Array of project objects or empty array on error
 *
 * @function getOrgMembers - Get all members of an organization
 * @param {string} getOrgMembers.orgId - The organization ID
 * @returns {Promise<Array>} Array of member objects or empty array on error
 *
 * @function getTeamMembers - Get all members of a specific team
 * @param {string} getTeamMembers.orgId - The organization ID
 * @param {string} getTeamMembers.teamId - The team ID
 * @returns {Promise<Array>} Array of member objects or empty array on error
 *
 * @function getUser - Get current user information
 * @returns {Promise<Object|null>} User data or null if not authenticated
 *
 * @function getUserInfo - Get user information
 * @returns {Promise<Object|null>} User data or null if not authenticated

 */

const userCache = {}

export async function getOrg(orgId) {
    const res = await API.get(`/orgs/${orgId}`);
        if (!res.ok) {
        console.error(`getOrg failed: ${res.status} ${res.statusText}`, await res.text());
        return null;
    }
    return await res.json();
}

export async function getTeams(orgId) {
    const res = await API.get(`/orgs/${orgId}/teams`);
    if (!res.ok) {
        console.error(`getTeams failed: ${res.status} ${res.statusText}`, await res.text());
        return [];
    }
    return await res.json();
}

export async function getProjects(orgId, teamId) {
    const res = await API.get(`/orgs/${orgId}/teams/${teamId}/projects`);
    if (!res.ok) {
        console.error(`getProjects failed: ${res.status} ${res.statusText}`, await res.text());
        return [];
    }
    return await res.json();

}

export async function getOrgMembers(orgId) {
    const res = await API.get(`/orgs/${orgId}/members`);
    if (!res.ok) {
        console.error(`getOrgMembers failed: ${res.status} ${res.statusText}`, await res.text());
        return [];
    }
    return await res.json();
}

export async function getTeamMembers(orgId, teamId) {
    const res = await API.get(`/orgs/${orgId}/teams/${teamId}/members`);
    if (!res.ok) {
        console.error(`getTeamMembers failed: ${res.status} ${res.statusText}`, await res.text());
        return [];
    }
    return await res.json();
}

export async function getUser() {
    const res = await API.get(`/user/me`);
    if (!res.ok) {
        console.error(`getUser failed: ${res.status} ${res.statusText}`, await res.text());
        return [];
    }
    return await res.json();
}

export async function getUserInfo(userId) {
    if (userCache[userId]) return userCache[userId]
    
    const res = await API.get(`/user/${userId}`)
    if (!res.ok) {
        console.error(`getUserInfo failed: ${res.status}`)
        return null
    }
    const user = await res.json()
    userCache[userId] = user
    return user
}
