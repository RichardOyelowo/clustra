import { requireAuth } from "./auth.js";
import { renderSidebar } from "./sidebar.js";
import { getOrg, getTeams, getProjects, getTeamMembers } from "./services.js";

requireAuth();

const params = new URLSearchParams(window.location.search);
const orgId = params.get("org_id");

let allTeams = [];
let currentOrg = null;
let currentTeamId = null;

async function init() {
    // fetch org and teams in parallel
    const [org, teams] = await Promise.all([getOrg(orgId), getTeams(orgId)]);

    if (!org) {
        console.error("failed to load org");
        return;
    }

    allTeams = teams;
    currentOrg = org;

    // default to first team
    if (allTeams.length === 0) {
        document.getElementById("switcher_team_name").textContent =
            "No teams yet";
        currentTeamId = null;
    } else {
        currentTeamId = allTeams[0].id;
    }

    // populate breadcrumb org link
    const orgLink = document.getElementById("breadcrumb_org_link");
    orgLink.href = `/org.html?org_id=${orgId}`;

    await loadTeam(currentTeamId);
}

async function loadTeam(teamId) {
    const [projects, members] = await Promise.all([
        getProjects(orgId, teamId),
        getTeamMembers(orgId, teamId),
    ]);

    const team = allTeams.find((t) => t.id === teamId);

    renderSidebar({
        orgId,
        orgName: currentOrg.name,
        teamId,
        projectId: null,
        activePage: "teams",
        counts: {
            teams: allTeams.length,
            projects: projects.length,
            tasks: 0,
            milestones: 0,
        },
        user: { initial: "R", name: "Richard", role: "Team Lead" },
    });

    // populate switcher + header
    document.getElementById("breadcrumb_org_link").textContent =
        currentOrg.name;
    document.getElementById("switcher_team_name").textContent = team.name;
    document.getElementById("member_count").textContent =
        members.length !== 0 ? `${members.length} members` : "No members yet.";
    renderSwitcher(allTeams, teamId);

    // populate team info card
    document.getElementById("info_name").textContent = team.name;
    document.getElementById("info_slug").textContent = team.slug;
    document.getElementById("info_desc").textContent = team.desc ?? "—";
    document.getElementById("info_created").textContent = new Date(
        team.created_at,
    ).toLocaleDateString();

    // populate stats
    document.getElementById("stat_projects").textContent = projects.length;
    document.getElementById("stat_members").textContent = members.length;

    renderProjects(projects, orgId, teamId);
    renderOrgMembers(members);
}

function renderSwitcher(teams, activeTeamId) {
    const dropdown = document.getElementById("switcher_dropdown");

    dropdown.innerHTML = teams
        .map(
            (team) => `
        <button 
            class="switcher_item ${team.id === activeTeamId ? "active" : ""}"
            data-team-id="${team.id}">
            <span class="switcher_dot"></span>
            <span>${team.name}</span>
        </button>
    `,
        )
        .join("");

    // wire up team switch on click
    dropdown.querySelectorAll(".switcher_item").forEach((btn) => {
        btn.addEventListener("click", async () => {
            const teamId = btn.dataset.teamId;
            currentTeamId = teamId;
            history.replaceState(
                null,
                "",
                `?org_id=${orgId}&team_id=${teamId}`,
            );
            closeSwitcher();
            loadTeam(teamId);
        });
    });
}

function renderProjects(projects, orgId, teamId) {
    const list = document.getElementById("projects_list");

    if (projects.length === 0) {
        list.innerHTML = `<p class="empty_state">No projects yet. Create one to get started.</p>`;
        return;
    }

    list.innerHTML = projects
        .map(
            (p) => `
        <a class="project_item" href="/project.html?org_id=${orgId}&team_id=${teamId}&proj_id=${p.id}">
            <div class="project_icon">📋</div>
            <div class="project_info">
                <div class="project_name">${p.name}</div>
                <div class="project_desc">${p.desc ?? "—"}</div>
            </div>
            <span class="material-symbols-outlined project_arrow">chevron_right</span>
        </a>
    `,
        )
        .join("");
}

function renderOrgMembers(members) {
    const list = document.getElementById("members_list");

    if (members.length === 0) {
        list.innerHTML = `<p class="empty_state">No members found.</p>`;
        return;
    }

    list.innerHTML = members
        .map(
            (m) => `
        <div class="member_item">
            <div class="member_avatar">${m.id.slice(0, 2).toUpperCase()}</div>
            <div class="member_info">
                <div class="member_id">${m.id.slice(0, 12)}...</div>
            </div>
            <span class="role_badge role_${m.role}">${m.role}</span>
        </div>
    `,
        )
        .join("");
}

// switcher open/close
const switcherBtn = document.getElementById("switcher_btn");
const switcher = document.getElementById("team_switcher");
const dropdown = document.getElementById("switcher_dropdown");

// dropdown menu
function openSwitcher() {
    dropdown.classList.remove("hidden");
    switcher.classList.add("open");
}

function closeSwitcher() {
    dropdown.classList.add("hidden");
    switcher.classList.remove("open");
}

switcherBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    dropdown.classList.contains("hidden") ? openSwitcher() : closeSwitcher();
});

// close when clicking outside
document.addEventListener("click", () => closeSwitcher());

init();
