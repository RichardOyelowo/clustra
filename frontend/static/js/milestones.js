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

async function init() {
    const [org, teams] = await Promise.all([getOrg(orgId), getTeams(orgId)]);

    if (!org || teams.length === 0) {
        console.error("failed to load org or no teams");
        return;
    }

    currentOrg = org;
    allTeams = teams;
    currentTeam = teams[0];

    allProjects = await getProjects(orgId, currentTeam.id);

    if (allProjects.length === 0) {
        console.error("no projects in this team");
        return;
    }

    currentProject = allProjects[0];

    await loadMilestones();
}

async function loadMilestones() {
    const milestonesRes = await API.get(
        `/orgs/${orgId}/teams/${currentTeam.id}/projects/${currentProject.id}/milestones`,
    );
    const milestones = milestonesRes.ok ? await milestonesRes.json() : [];

    renderSidebar({
        orgId,
        orgName: currentOrg.name,
        teamId: currentTeam.id,
        projectId: currentProject.id,
        activePage: "milestones",
        counts: {
            teams: allTeams.length,
            projects: allProjects.length,
            tasks: 0,
            milestones: milestones.length,
        },
        user: { initial: "R", name: "Richard", role: "Team Lead" },
    });

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

    renderMilestones(milestones);
}

function renderMilestones(milestones) {
    const list = document.getElementById("milestones_list");

    if (milestones.length === 0) {
        list.innerHTML = `<p class="empty_state">No milestones yet. Create one to track project progress.</p>`;
        return;
    }

    list.innerHTML = milestones
        .map(
            (m) => `
        <div class="milestone_item" data-milestone-id="${m.id}">
            <div class="milestone_icon">🚩</div>
            <div class="milestone_body">
                <div class="milestone_title">${m.title}</div>
                <div class="milestone_desc">${m.desc ?? ""}</div>
                <div class="milestone_meta">
                    <span class="milestone_due">${m.due_date ? new Date(m.due_date).toLocaleDateString() : "No due date"}</span>
                </div>
            </div>
            <div class="milestone_actions">
                <button class="action_btn danger" data-delete-id="${m.id}">Delete</button>
            </div>
        </div>
    `,
        )
        .join("");

    list.querySelectorAll("[data-delete-id]").forEach((btn) => {
        btn.addEventListener("click", async () => {
            const milestoneId = btn.dataset.deleteId;
            await API.delete(
                `/orgs/${orgId}/teams/${currentTeam.id}/projects/${currentProject.id}/milestones/${milestoneId}`,
            );
            await loadMilestones();
        });
    });
}

// ── new milestone modal ──
const newMilestoneModal = document.getElementById("new_milestone_modal");
const newMilestoneForm = document.getElementById("new_milestone_form");

document.getElementById("new_milestone_btn").addEventListener("click", () => {
    newMilestoneModal.classList.remove("hidden");
});
document
    .getElementById("cancel_milestone_btn")
    .addEventListener("click", () => {
        newMilestoneModal.classList.add("hidden");
    });

newMilestoneForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(newMilestoneForm);

    const payload = {
        title: formData.get("title"),
        desc: formData.get("desc") || null,
        due_date: formData.get("due_date") || null,
    };

    const milesetoneRes = await API.post(
        `/orgs/${orgId}/teams/${currentTeam.id}/projects/${currentProject.id}/milestones`,
        payload,
    );

    if (milesetoneRes.ok) {
        newMilestoneModal.classList.add("hidden");
        newMilestoneForm.reset();
        await loadMilestones();
    }
});

init();
