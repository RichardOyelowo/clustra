import { requireAuth } from "./auth.js";
import { renderSidebar } from "./sidebar.js";
import { getOrg, getTeams, getProjects } from "./services.js";
import API from "./api.js";

requireAuth();

const params = new URLSearchParams(window.location.search);
const orgId = params.get("org_id");

let currentOrg = null;
let currentTeam = null;
let currentProject = null;
let allTeams = [];
let allProjects = [];
let allTasks = [];

async function init() {
    const [org, teams] = await Promise.all([getOrg(orgId), getTeams(orgId)]);

    if (!org) {
        console.error("failed to load org or no teams");
        return;
    }

    currentOrg = org;
    allTeams = teams;

    if (allTeams.length === 0) {
        renderSidebar({
            orgId,
            orgName: currentOrg.name,
            teamId: null,
            projectId: null,
            activePage: "project",
            counts: { teams: 0, projects: 0, tasks: 0, milestones: 0 },
            user: { initial: "R", name: "Richard", role: "Team Lead" },
        });

        document.getElementById("breadcrumb_org_link").href =
            `/org.html?org_id=${orgId}`;
        document.getElementById("breadcrumb_org_link").textContent =
            currentOrg.name;
        return;
    }

    currentTeam = teams[0];
    allProjects = await getProjects(orgId, currentTeam.id);

    if (allProjects.length === 0) {
        console.error("no projects in this team");
        return;
    }

    currentProject = allProjects[0];

    await loadTasks();
}

async function loadTasks() {
    const tasksRes = await API.get(
        `/orgs/${orgId}/teams/${currentTeam.id}/projects/${currentProject.id}/tasks`,
    );
    allTasks = tasksRes.ok ? await tasksRes.json() : [];

    renderSidebar({
        orgId,
        orgName: currentOrg.name,
        teamId: currentTeam.id,
        projectId: currentProject.id,
        activePage: "tasks",
        counts: {
            teams: allTeams.length,
            projects: allProjects.length,
            tasks: allTasks.length,
            milestones: 0,
        },
        user: { initial: "R", name: "Richard", role: "Team Lead" },
    });

    // populate breadcrumb — same pattern as project.js
    document.getElementById("breadcrumb_org_link").href =
        `/org.html?org_id=${orgId}`;
    document.getElementById("breadcrumb_org_link").textContent =
        currentOrg.name;

    document.getElementById("breadcrumb_team_link").href =
        `/teams.html?org_id=${orgId}&team_id=${currentTeam.id}`;
    document.getElementById("breadcrumb_team_link").textContent =
        currentTeam.name;

    document.getElementById("breadcrumb_project_link").href =
        `/project.html?org_id=${orgId}&team_id=${currentTeam.id}&proj_id=${currentProject.id}`;
    document.getElementById("breadcrumb_project_link").textContent =
        currentProject.name;

    renderTable(allTasks);
}

function renderTable(tasks) {
    const tbody = document.getElementById("tasks_tbody");

    if (tasks.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="empty_state">No tasks yet.</td></tr>`;
        return;
    }

    tbody.innerHTML = tasks
        .map(
            (task) => `
        <tr data-task-id="${task.id}">
            <td class="task_id_cell">CLU-${task.id.slice(0, 4)}</td>
            <td class="task_title_cell">${task.title}</td>
            <td><span class="status_badge status_${task.status}">${task.status}</span></td>
            <td><span class="priority_badge priority_${task.priority}"><span class="priority_dot"></span>${task.priority}</span></td>
            <td class="due_cell">${task.due_date ? new Date(task.due_date).toLocaleDateString() : "—"}</td>
            <td class="assignee_cell">${task.assignee_id ? task.assignee_id.slice(0, 8) + "..." : "—"}</td>
            <td><button class="action_btn" data-delete-id="${task.id}">Delete</button></td>
        </tr>
    `,
        )
        .join("");

    // wire up delete buttons
    tbody.querySelectorAll("[data-delete-id]").forEach((btn) => {
        btn.addEventListener("click", async () => {
            const taskId = btn.dataset.deleteId;
            await API.delete(
                `/orgs/${orgId}/teams/${currentTeam.id}/projects/${currentProject.id}/tasks/${taskId}`,
            );
            await loadTasks();
        });
    });
}

// ── filters ──
document
    .getElementById("filter_status")
    .addEventListener("change", applyFilters);
document
    .getElementById("filter_priority")
    .addEventListener("change", applyFilters);

function applyFilters() {
    const statusFilter = document.getElementById("filter_status").value;
    const priorityFilter = document.getElementById("filter_priority").value;

    let filtered = allTasks;

    if (filtered.length > 0) {
        if (statusFilter)
            filtered = filtered.filter((t) => t.status === statusFilter);
        if (priorityFilter)
            filtered = filtered.filter((t) => t.priority === priorityFilter);
    }

    renderTable(filtered);
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
        await loadTasks();
    }
});

init();
