import API from "./api.js";
import { requireAuth } from "./auth.js";
import { renderSidebar } from "./sidebar.js";
import {
    getUser,
    getOrg,
    getTeams,
    getUserInfo,
    getProjects,
    getTeamMembers,
    getTeamMemberCandidates
} from "./services.js";

requireAuth();

const params = new URLSearchParams(window.location.search);
const orgId = params.get("org_id");
const teamId = params.get("team_id")

let allTeams = [];
let currentOrg = null;
let currentUser = null;
let currentTeamId = null;

async function init() {
    // fetch org and teams in parallel
    const [org, teams, user] = await Promise.all([
        getOrg(orgId),
        getTeams(orgId),
        getUser(),
    ]);

    if (!org) {
        console.error("failed to load org");
        return;
    }

    allTeams = teams;
    currentOrg = org;
    currentUser = user;

    // defaults to team id in url or first team
    if (allTeams.length === 0) {
        document.getElementById("switcher_team_name").textContent = "No teams yet";
        currentTeamId = null;
    } else {
        const teamExists = allTeams.some((t) => t.id === teamId);

        if (teamId && teamExists) {
            currentTeamId = teamId;
        } else {
            currentTeamId = allTeams[0].id;
            history.replaceState(
                null,
                "",
                `?org_id=${orgId}&team_id=${currentTeamId}`,
            );
        }
    }
    renderSidebar({
        orgId,
        orgName: currentOrg.name,
        teamId: currentTeamId,
        projectId: null,
        activePage: "teams",
        counts: {
            teams: allTeams.length,
            projects: 0,
            tasks: 0,
            milestones: 0,
        },
        user: {
            initial: currentUser.full_name.charAt(0).toUpperCase(),
            name: currentUser.full_name,
            role: "Member",
        },
    });

    // populate breadcrumb org link
    const orgLink = document.getElementById("breadcrumb_org_link");
    orgLink.href = `/org.html?org_id=${orgId}`;

    if (currentTeamId) {
        await loadTeam(currentTeamId);
    }

    // ── New Project Modal ──
    const newProjectModal = document.getElementById("new_project_modal");
    const newProjectForm = document.getElementById("new_project_form");

    document.getElementById("new_project_btn").addEventListener("click", () => {
        newProjectModal.classList.remove("hidden");
    });
    document
        .getElementById("cancel_project_btn")
        .addEventListener("click", () => {
            newProjectModal.classList.add("hidden");
        });

    newProjectForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(newProjectForm);
        const payload = {
            name: formData.get("name"),
            desc: formData.get("desc") || null,
        };
        const res = await API.post(
            `/orgs/${orgId}/teams/${currentTeamId}/projects`,
            payload,
        );

        if (!res.ok) {
            console.log("Status:", res.status);
            console.log(await res.json());
        }

        if (res.ok) {
            newProjectModal.classList.add("hidden");
            newProjectForm.reset();
            await loadTeam(currentTeamId);
        }
    });

    // ── Add Member Modal ──
    const addMemberModal = document.getElementById("add_member_modal");
    const addMemberForm = document.getElementById("add_member_form");

    document.getElementById("add_member_btn").addEventListener("click", async () => {
        await populateTeamMemberCandidates();
        addMemberModal.classList.remove("hidden");
    });

    document
        .getElementById("cancel_member_btn")
        .addEventListener("click", () => {
            addMemberModal.classList.add("hidden");
        });

    addMemberForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(addMemberForm);
        const payload = {
            user_id: formData.get("user_id"),
            role: formData.get("role"),
        };
        const res = await API.post(
            `/orgs/${orgId}/teams/${currentTeamId}/members`,
            payload,
        );

        if (!res.ok) {
            console.log("Status:", res.status);
            console.log(await res.json());
        }

        if (res.ok) {
            addMemberModal.classList.add("hidden");
            addMemberForm.reset();
            await loadTeam(currentTeamId);
        }
    });

    // ── Edit Team Modal ──
    const editTeamModal = document.getElementById("edit_team_modal");
    const editTeamForm = document.getElementById("edit_team_form");

    document.getElementById("edit_team_btn").addEventListener("click", () => {
        const team = allTeams.find((t) => t.id === currentTeamId);
        document.getElementById("edit_name").value = team.name;
        document.getElementById("edit_desc").value = team.desc ?? "";
        editTeamModal.classList.remove("hidden");
    });

    document.getElementById("cancel_edit_btn").addEventListener("click", () => {
        editTeamModal.classList.add("hidden");
    });

    editTeamForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(editTeamForm);
        const payload = {
            name: formData.get("name"),
            slug: formData.get("slug"),
            desc: formData.get("desc") || null,
        };
        const res = await API.patch(
            `/orgs/${orgId}/teams/${currentTeamId}`,
            payload,
        );

        if (!res.ok) {
            console.log("Status:", res.status);
            console.log(await res.json());
        }

        if (res.ok) {
            editTeamModal.classList.add("hidden");
            allTeams = await getTeams(orgId);
            await loadTeam(currentTeamId);
        }
    });

    // ── Delete Team Modal ──
    const deleteTeamModal = document.getElementById("delete_team_modal");

    document.getElementById("delete_team_btn").addEventListener("click", () => {
        deleteTeamModal.classList.remove("hidden");
    });

    document
        .getElementById("cancel_delete_btn")
        .addEventListener("click", () => {
            deleteTeamModal.classList.add("hidden");
        });

    document
        .getElementById("confirm_delete_btn")
        .addEventListener("click", async () => {
            const res = await API.delete(
                `/orgs/${orgId}/teams/${currentTeamId}`,
            );

            if (!res.ok) {
                console.log("Status:", res.status);
            }

            if (res.ok) {
                window.location.href = `/org.html?org_id=${orgId}`;
            }
        });
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
        user: {
            initial: currentUser.full_name.charAt(0).toUpperCase(),
            name: currentUser.full_name,
            role: "Member",
        },
    });

    // populate switcher + header
    document.getElementById("breadcrumb_org_link").textContent =
        currentOrg.name;
    document.getElementById("switcher_team_name").textContent = team.name;
    document.getElementById("member_count").textContent =
        members.length !== 0 ? `${members.length} members` : "";
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
    await renderOrgMembers(members);
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

    const displayItems = projects.slice(0, 5);
    list.innerHTML = displayItems
        .map(
            (p) => `
        <a class="project_item" href="/projects.html?org_id=${orgId}&team_id=${teamId}&proj_id=${p.id}">
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

async function renderOrgMembers(members) {
    const list = document.getElementById("members_list");

    if (members.length === 0) {
        list.innerHTML = `<p class="empty_state">No members found.</p>`;
        return;
    }

    const items = await Promise.all(
        members.slice(0, 5).map(async (m) => {
            const user = await getUserInfo(m.user_id);

            return `
                <div class="member_item">
                    <div class="member_avatar">
                        ${user.full_name.slice(0, 2).toUpperCase()}
                    </div>
                    <div class="member_info">
                        <div class="member_name">${user.full_name}</div>
                    </div>
                    <span class="role_badge role_${m.role}">${m.role}</span>
                </div>
            `;
        }),
    );

    list.innerHTML = items.join("");
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

async function populateTeamMemberCandidates() {
    const select = document.getElementById("team_user_select");

    select.innerHTML = `
        <option value="">
            Select a user...
        </option>
    `;

    const users = await getTeamMemberCandidates(orgId, currentTeamId);

    users.forEach((user) => {
        const option = document.createElement("option");

        option.value = user.id;
        option.textContent = user.full_name;

        select.appendChild(option);
    });
}

switcherBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    dropdown.classList.contains("hidden") ? openSwitcher() : closeSwitcher();
});

// close when clicking outside
document.addEventListener("click", () => closeSwitcher());

init();
