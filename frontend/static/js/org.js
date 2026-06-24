import { requireAuth, logout } from "./auth.js";
import { renderSidebar } from "./sidebar.js";
import API from "./api.js";

requireAuth();

const params = new URLSearchParams(window.location.search);
const orgId = params.get("org_id");

async function loadOrgs() {
    const response = await API.get(`/orgs/${orgId}`);

    if (!response.ok) {
        console.error("failed to load org");
        return;
    }

    return await response.json();
}

// renders the teams table rows
function renderTeams(teams) {
    const tbody = document.getElementById("teams_tbody");

    if (teams.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" class="empty_state">No teams yet. Create one to get started.</td></tr>`;
        return;
    }

    tbody.innerHTML = teams
        .map(
            (team) => `
        <tr class="clickable" onclick="window.location.href='/teams.html?org_id=${orgId}&team_id=${team.id}'">
            <td><span class="team_dot"></span><span class="team_name_cell">${team.name}</span></td>
            <td class="team_slug_cell">${team.slug}</td>
            <td class="team_desc_cell">${team.desc ?? "—"}</td>
            <td></td>
        </tr>
    `,
        )
        .join("");
}

// renders the members table rows
function renderOrgMembers(orgMembers) {
    const tbody = document.getElementById("members_tbody");

    if (orgMembers.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" class="empty_state">No members found.</td></tr>`;
        return;
    }

    tbody.innerHTML = orgMembers
        .map(
            (orgMember) => `
        <tr>
            <td class="mono">${orgMember.user_id}</td>
            <td><span class="role_badge role_${orgMember.role}">${orgMember.role}</span></td>
            <td>${new Date(orgMember.joined_at).toLocaleDateString()}</td>
            <td><button class="remove_btn">Remove</button></td>
        </tr>
    `,
        )
        .join("");
}

// renders activity feed items
function renderActivity(activities) {
    const list = document.getElementById('activity_list')

    if (activities.length === 0) {
        list.innerHTML = `<p class="empty_state">No recent activity.</p>`
        return
    }

    const icons = {
        created: '✦',
        updated: '✎',
        deleted: '✕'
    }

    list.innerHTML = activities.map(a => `
        <div class="activity_item">
            <div class="activity_icon">${icons[a.action] ?? '⚡'}</div>
            <div class="activity_body">
                <div class="activity_text">
                    <strong>${a.action}</strong> ${a.model_type.toLowerCase().replace('_', ' ')}
                </div>
                <div class="activity_meta">
                    ${a.user_id.slice(0, 8)}... · ${new Date(a.created_at).toLocaleDateString()}
                </div>
            </div>
        </div>
    `).join('')
}

async function init() {
    const org = await loadOrgs();

    if (!org) return;

    renderSidebar({
        orgId: orgId,
        orgName: org.name,
        teamId: null,
        projectId: null,
        activePage: "org",
        counts: {
            teams: 0,
            projects: 0,
            tasks: 0,
            milestones: 0,
        },
        user: {
            initial: "RO",
            name: "Richard Oyelowo",
            role: "Org Admin",
        },
    });

    const [teamsRes, orgMembersRes, activityRes] = await Promise.all([
        API.get(`/orgs/${orgId}/teams/`),
        API.get(`/orgs/${orgId}/members`),
        API.get(`/orgs/${orgId}/activity`),
    ]);

    const teams = teamsRes.ok ? await teamsRes.json() : [];
    const orgMembers = orgMembersRes.ok ? await orgMembersRes.json() : [];
    const activities = activityRes.ok ? await activityRes.json() : [];

    // stat chips
    document.getElementById("stat_teams").textContent = teams.length;
    document.getElementById("stat_members").textContent = orgMembers.length;

    // org info card
    document.getElementById("info_name").textContent = org.name;
    document.getElementById("info_slug").textContent = org.slug;
    document.getElementById("info_owner").textContent = org.owner_id;
    document.getElementById("info_desc").textContent = org.desc ?? "—";

    // render all three sections
    renderTeams(teams);
    renderOrgMembers(orgMembers);
    renderActivity(activities);

    document.getElementById("org_name_title").textContent = org.name;
    document.getElementById("breadcrumb_org_name").textContent = org.name;
}

init();
