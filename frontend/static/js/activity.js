import { requireAuth } from "./auth.js";
import { renderSidebar } from "./sidebar.js";
import { getOrg, getTeams } from "./services.js";
import API from "./api.js";

requireAuth();

const params = new URLSearchParams(window.location.search);
const orgId = params.get("org_id");

let currentOrg = null;
let allTeams = [];
let allActivities = [];

async function init() {
    const [org, teams] = await Promise.all([getOrg(orgId), getTeams(orgId)]);

    if (!org) {
        console.error("failed to load org");
        return;
    }

    currentOrg = org;
    allTeams = teams;

    await loadActivity();
}

async function loadActivity() {
    const activityRes = await API.get(`/orgs/${orgId}/activity`);
    allActivities = activityRes.ok ? await activityRes.json() : [];

    renderSidebar({
        orgId,
        orgName: currentOrg.name,
        teamId: null,
        projectId: null,
        activePage: "activity",
        counts: {
            teams: allTeams.length,
            projects: 0,
            tasks: 0,
            milestones: 0,
        },
        user: { initial: "R", name: "Richard", role: "Org Admin" },
    });

    document.getElementById("breadcrumb_org_link").href =
        `/org.html?org_id=${orgId}`;
    document.getElementById("breadcrumb_org_link").textContent =
        currentOrg.name;

    renderFeed(allActivities);
}

function renderFeed(activities) {
    const feed = document.getElementById("activity_feed");

    if (activities.length === 0) {
        feed.innerHTML = `<p class="empty_state">No activity yet.</p>`;
        return;
    }

    feed.innerHTML = activities
        .map(
            (a) => `
        <div class="activity_item">
            <div class="activity_icon_wrap">
                <div class="activity_icon ${a.action}">
                    ${a.action === "created" ? "✦" : a.action === "updated" ? "✎" : "✕"}
                </div>
            </div>
            <div class="activity_body">
                <div class="activity_text">
                    <strong>${a.action}</strong> :
                    <span class="activity_model"> ${a.model_type.toLowerCase().replace("_", " ")}</span>
                </div>
                <div class="activity_meta">
                    <span class="activity_user">${a.user_id.slice(0, 8)}...</span>
                    <span class="activity_time">${new Date(a.created_at).toLocaleString()}</span>
                </div>
            </div>
        </div>
    `,
        )
        .join("");
}

// ── filters ──
document
    .getElementById("filter_action")
    .addEventListener("change", applyFilters);
document
    .getElementById("filter_model")
    .addEventListener("change", applyFilters);

function applyFilters() {
    const actionFilter = document.getElementById("filter_action").value;
    const modelFilter = document.getElementById("filter_model").value;

    let filtered = allActivities;

    if (filtered) {
        if (actionFilter)
            filtered = filtered.filter((a) => a.action === actionFilter);
        if (modelFilter)
            filtered = filtered.filter((a) => a.model_type === modelFilter);
    }
    renderFeed(filtered);
}

init();
