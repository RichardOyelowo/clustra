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
 */

export async function getOrg(orgId) {
    const response = await API.get(`/orgs/${orgId}`);
    return response.ok ? await response.json() : null;
}

export async function getTeams(orgId) {
    const res = await API.get(`/orgs/${orgId}/teams`);
    return res.ok ? await res.json() : [];
}

export async function getProjects(orgId, teamId) {
    const res = await API.get(`/orgs/${orgId}/teams/${teamId}/projects`);
    return res.ok ? await res.json() : [];
}

export async function getOrgMembers(orgId) {
    const res = await API.get(`/orgs/${orgId}/members`);
    return res.ok ? await res.json() : [];
}

export async function getTeamMembers(orgId, teamId) {
    const res = await API.get(`/orgs/${orgId}/teams/${teamId}/members`);
    return res.ok ? await res.json() : [];
}

export async function getUser() {
    const res = await API.get(`/user/me`);
    return res.ok ? await res.json() : null;
}
