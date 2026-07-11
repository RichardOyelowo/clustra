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
    const [org, teams, user] = await Promise.all([getOrg(orgId), getTeams(orgId), getUser()]);

    if (!org) {
        console.error("failed to load org");
        return;
    }

    currentOrg = org;
    allTeams = teams;
    currentUser = user;

    if (allTeams.length === 0) {
        renderSidebar({
            orgId,
            orgName: currentOrg.name,
            teamId: null,
            projectId: null,
            activePage: "projects",
            counts: { teams: 0, projects: 0, tasks: 0, milestones: 0 },
            user: { 
                initial: currentUser.username.charAt(0).toUpperCase(), 
                name: currentUser.username,
                role: "Member" 
            },
        });

        document.getElementById("breadcrumb_org_link").href =
            `/org.html?org_id=${orgId}`;
        document.getElementById("breadcrumb_org_link").textContent =
            currentOrg.name;

        document.getElementById("kanban_board").innerHTML =
            `<p class="empty_state">No teams In this organization yet. <a class="btn_outline" href="/org.html?org_id=${orgId}">Create one</a></p>`;
        return;
    }

    currentTeam = teams[0];
    allProjects = await getProjects(orgId, currentTeam.id);

    if (allProjects.length === 0) {
        document.getElementById("kanban_board").innerHTML =
            '<p class="empty_state">No projects in this team yet. <a href="/teams.html?org_id=${orgId}&team_id=${currentTeam.id}">Create one</a></p>';
        return;
    }

    currentProject = allProjects[0];
    await loadProject();
}

async function loadProject() {
    const tasksRes = await API.get(
        `/orgs/${orgId}/teams/${currentTeam.id}/projects/${currentProject.id}/tasks`,
    );
    const tasks = tasksRes.ok ? await tasksRes.json() : [];

    // render sidebar + breadcrumb now that we have team context too
    renderSidebar({
        orgId,
        orgName: currentOrg.name,
        teamId: currentTeam.id,
        projectId: currentProject.id,
        activePage: "projects",
        counts: {
            teams: allTeams.length,
            projects: allProjects.length,
            tasks: 0,
            milestones: 0,
        },
        user: { 
            initial: currentUser.username.charAt(0).toUpperCase(), 
            name: currentUser.username,
            role: "Member" 
        },
    });

    document.getElementById("breadcrumb_org_link").href =
        `/org.html?org_id=${orgId}`;
    document.getElementById("breadcrumb_org_link").textContent =
        currentOrg.name;

    document.getElementById("breadcrumb_team_link").href =
        `/teams.html?org_id=${orgId}&team_id=${currentTeam.id}`;
    document.getElementById("breadcrumb_team_link").textContent =
        currentTeam.name;

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
