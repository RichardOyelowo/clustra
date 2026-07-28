import { requireAuth } from "./auth.js";
import { renderSidebar } from "./sidebar.js";
import { getOrg, getTeams, getUser } from "./services.js";
import API from "./api.js";

await requireAuth();

const params = new URLSearchParams(window.location.search);
const orgId = params.get("org_id");

let currentUser = null;
let currentOrg = null;
let allTeams = [];

async function init() {
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

    renderSidebar({
        orgId,
        orgName: currentOrg.name,
        teamId: null,
        projectId: null,
        activePage: "settings",
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

    document.getElementById("breadcrumb_org_link").href =
        `/org.html?org_id=${orgId}`;
    document.getElementById("breadcrumb_org_link").textContent =
        currentOrg.name;

    // pre-fill the settings form with current org data
    document.getElementById("setting_name").value = currentOrg.name;
    document.getElementById("setting_slug").value = currentOrg.slug;
    document.getElementById("setting_desc").value = currentOrg.desc ?? "";
}

// ── settings form submit ──
const settingsForm = document.getElementById("org_settings_form");
const feedback = document.getElementById("settings_feedback");

settingsForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(settingsForm);

    const payload = {
        name: formData.get("name"),
        slug: formData.get("slug"),
        desc: formData.get("desc") || null,
    };

    const response = await API.patch(`/orgs/${orgId}`, payload);

    if (response.ok) {
        feedback.textContent = "Saved";
        feedback.classList.remove("hidden", "error");
        currentOrg = await response.json();
    } else {
        feedback.textContent = "Failed to save changes";
        feedback.classList.remove("hidden");
        feedback.classList.add("error");
    }
});

// ── delete org modal ──
const deleteModal = document.getElementById("delete_org_modal");

document.getElementById("delete_org_btn").addEventListener("click", () => {
    deleteModal.classList.remove("hidden");
});
document.getElementById("cancel_delete_btn").addEventListener("click", () => {
    deleteModal.classList.add("hidden");
});

document
    .getElementById("confirm_delete_btn")
    .addEventListener("click", async () => {
        const orgDel = await API.delete(`/orgs/${orgId}`);

        if (!orgDel.ok) return;

        if (orgDel.ok) {
            window.location.href = "/orgs.html";
        }
    });

init();
