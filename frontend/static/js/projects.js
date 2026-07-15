import { requireAuth } from "./auth.js";
import { renderSidebar } from "./sidebar.js";
import { getOrg, getTeams, getProjects, getUser } from "./services.js";
import API from "./api.js";

requireAuth();

const params = new URLSearchParams(window.location.search);
const orgId = params.get("org_id");

let currentOrg = null;
let currentUser = null;
let currentTeam = null;
let currentProject = null;
let allTeams = [];
let allProjects = [];

async function init() {
    const teamIdParam = params.get("team_id");
    const projIdParam = params.get("proj_id");

    const [org, teams, user] = await Promise.all([
        getOrg(orgId),
        getTeams(orgId),
        getUser(),
    ]);

    if (!org) {
        console.error("failed to load org");
        return;
    }

    currentOrg = org;
    allTeams = teams;
    currentUser = user;

    currentTeam = teamIdParam
        ? (teams.find((t) => t.id === teamIdParam) ?? teams[0] ?? null)
        : (teams[0] ?? null);

    document.getElementById("breadcrumb_org_link").href =
        `/org.html?org_id=${orgId}`;
    document.getElementById("breadcrumb_org_link").textContent =
        currentOrg.name;

    if (currentTeam) {
        allProjects = await getProjects(orgId, currentTeam.id);

        currentProject = projIdParam
            ? (allProjects.find((p) => p.id === projIdParam) ??
              allProjects[0] ??
              null)
            : (allProjects[0] ?? null);

        document.getElementById("breadcrumb_team_link").href =
            `/teams.html?org_id=${orgId}&team_id=${currentTeam.id}`;
        document.getElementById("breadcrumb_team_link").textContent =
            currentTeam.name;

        if (currentProject) {
            document.getElementById("project_switcher").href =
                `/projects.html?org_id=${orgId}&team_id=${currentTeam.id}&proj_id=${currentProject.id}`;
            document.getElementById("switcher_project_name").textContent =
                currentProject.name;
        } else {
            document.getElementById("project_switcher").href =
                `/projects.html?org_id=${orgId}&team_id=${currentTeam.id}`;
        }
    }

    renderSidebar({
        orgId,
        orgName: currentOrg.name,
        teamId: currentTeam?.id ?? null,
        projectId: currentProject?.id ?? null,
        activePage: "projects",
        counts: {
            teams: allTeams.length,
            projects: allProjects.length,
            tasks: 0,
            milestones: 0,
        },
        user: {
            initial: currentUser.full_name.charAt(0).toUpperCase(),
            name: currentUser.full_name,
            role: "Member",
        },
    });

    if (!currentTeam) {
        document.getElementById("kanban_board").innerHTML =
            `<p class="empty_state">No teams in this organization yet. <a class="btn_outline" href="/org.html?org_id=${orgId}">Create one</a></p>`;
        return; // stop here — nothing left to load
    }

    if (!currentProject) {
        document.getElementById("kanban_board").innerHTML =
            `<p class="empty_state">No projects yet. <a href="/teams.html?org_id=${orgId}&team_id=${currentTeam.id}">Get started</a></p>`;
        return; // stop here — loadProject() needs a project
    }

    await loadProject();
}

async function loadProject() {
    const tasksRes = await API.get(
        `/orgs/${orgId}/teams/${currentTeam.id}/projects/${currentProject.id}/tasks`,
    );
    const tasks = tasksRes.ok ? await tasksRes.json() : [];

    if (allProjects.length === 0) {
        document.getElementById("kanban_board").innerHTML =
            `<p class="empty_state">No projects in this team yet. <a href="/teams.html?org_id=${orgId}&team_id=${currentTeam.id}">Create one</a></p>`;
        return;
    }

    renderProjectSwitcher();
    renderKanban(tasks);
}

function renderProjectSwitcher() {
    const dropdown = document.getElementById("switcher_dropdown");
    dropdown.innerHTML = allProjects
        .map(
            (p) => `
        <button 
            class="switcher_item ${p.id === currentProject.id ? "active" : ""}"
            data-project-id="${p.id}">
            <span class="switcher_dot"></span>
            <span>${p.name}</span>
        </button>
    `,
        )
        .join("");

    dropdown.querySelectorAll(".switcher_item").forEach((btn) => {
        btn.addEventListener("click", async () => {
            const projId = btn.dataset.projectId;
            currentProject = allProjects.find((p) => p.id === projId);
            closeSwitcher();
            await loadProject();
        });
    });
}

function renderKanban(tasks) {
    // Step 8: group tasks by status
    const statuses = ["pending", "active", "completed", "archived"];

    statuses.forEach((status) => {
        const columnTasks = tasks.filter((t) => t.status === status);
        const container = document.getElementById(`cards_${status}`);
        const countEl = document.getElementById(`count_${status}`);

        countEl.textContent = columnTasks.length;

        if (columnTasks.length === 0) {
            container.innerHTML = `<p class="empty_col">No tasks</p>`;
            return;
        }

        container.innerHTML = columnTasks
            .map(
                (task) => `
            <div class="task_card" data-task-id="${task.id}">
                <span class="task_id">CLU-${task.id.slice(0, 4)}</span>
                <span class="task_title">${task.title}</span>
                <div class="task_meta">
                    <span class="task_due">${task.due_date ? new Date(task.due_date).toLocaleDateString() : ""}</span>
                    <span class="priority_dot priority_${task.priority}"></span>
                </div>
            </div>
        `,
            )
            .join("");
    });
}

// ── new task modal ──
const newTaskModal = document.getElementById("new_task_modal");
const newTaskForm = document.getElementById("new_task_form");

document.getElementById("new_task_btn").addEventListener("click", () => {
    newTaskModal.classList.remove("hidden");
});
document.getElementById("cancel_task_btn").addEventListener("click", () => {
    newTaskModal.classList.add("hidden");
});

newTaskForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(newTaskForm);

    const payload = {
        title: formData.get("title"),
        desc: formData.get("desc") || null,
        priority: formData.get("priority"),
        due_date: formData.get("due_date") || null,
    };

    const taskRes = await API.post(
        `/orgs/${orgId}/teams/${currentTeam.id}/projects/${currentProject.id}/tasks`,
        payload,
    );

    if (taskRes.ok) {
        newTaskModal.classList.add("hidden");
        newTaskForm.reset();
        loadProject();
    }
});

// ── switcher open/close ──
const switcherBtn = document.getElementById("switcher_btn");
const switcher = document.getElementById("project_switcher");
const dropdown = document.getElementById("switcher_dropdown");

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
document.addEventListener("click", () => closeSwitcher());

init();
