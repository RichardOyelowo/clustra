import { renderSidebar } from "./sidebar.js";
import { requireAuth, logout } from "./auth.js";
import { getUser, getUserInfo } from "./services.js";
import API from "./api.js";

await requireAuth();

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

function renderTeams(teams) {
    const tbody = document.getElementById("teams_tbody");

    if (teams.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" class="empty_state">No teams yet. Create one to get started.</td></tr>`;
        return;
    }

    const displayItems = teams.slice(0, 5)
    tbody.innerHTML = displayItems
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

async function renderOrgMembers(orgMembers) {
    const tbody = document.getElementById("members_tbody");

    if (orgMembers.length === 0) {
        tbody.innerHTML = `
            <tr><td colspan="4" class="empty_state">No members found.</td></tr>
        `;
        return;
    }

    const rows = await Promise.all(
        orgMembers.slice(0, 5).map(async (member) => {
            const user = await getUserInfo(member.user_id);

            return `
                <tr>
                    <td class="mono">${user.full_name}</td>
                    <td><span class="role_badge role_${member.role}">${member.role}</span></td>
                    <td>${new Date(member.joined_at).toLocaleDateString()}</td>
                    <td><button class="remove_btn">Remove</button></td>
                </tr>
            `;
        })
    );

    tbody.innerHTML = rows.join("");
}

async function renderActivity(activities) {
    const list = document.getElementById("activity_list");

    if (activities.length === 0) {
        list.innerHTML = `<p class="empty_state">No recent activity.</p>`;
        return;
    }

    const icons = {
        created: "✦",
        updated: "✎",
        deleted: "✕",
    };

    const items = await Promise.all(
        activities.slice(0, 5).map(async (a) => {
            const user = await getUserInfo(a.user_id);

            return `
                <div class="activity_item">
                    <div class="activity_icon">${icons[a.action] ?? "⚡"}</div>
                    <div class="activity_body">
                        <div class="activity_text">
                            <strong>${a.action}</strong>
                            ${a.model_type.toLowerCase().replace("_", " ")}
                        </div>
                        <div class="activity_meta">
                            ${user.full_name} · ${new Date(a.created_at).toLocaleDateString()}
                        </div>
                    </div>
                </div>
            `;
        })
    );

    list.innerHTML = items.join("");
}

async function loadTeams() {
    const teamsRes = await API.get(`/orgs/${orgId}/teams/`);
    const teams = teamsRes.ok ? await teamsRes.json() : [];
    document.getElementById("stat_teams").textContent = teams.length;
    renderTeams(teams);
}

async function init() {
    const org = await loadOrgs();
    const user = await getUser();

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
            initial: user.full_name.charAt(0).toUpperCase(),
            name: user.full_name,
            role: "Member",
        },
    });

    const [orgMembersRes, activityRes] = await Promise.all([
        API.get(`/orgs/${orgId}/members`),
        API.get(`/orgs/${orgId}/activity`),
    ]);

    const orgMembers = orgMembersRes.ok ? await orgMembersRes.json() : [];
    const activities = activityRes.ok ? await activityRes.json() : [];
    const owner = await getUserInfo(org.owner_id);

    document.getElementById("stat_members").textContent = orgMembers.length;

    document.getElementById("info_name").textContent = org.name;
    document.getElementById("info_slug").textContent = org.slug;
    document.getElementById("info_owner").textContent = owner.full_name;
    document.getElementById("info_desc").textContent = org.desc ?? "—";

    await loadTeams();
    await renderOrgMembers(orgMembers);
    await renderActivity(activities);

    document.getElementById("org_name_title").textContent = org.name;
    document.getElementById("breadcrumb_org_name").textContent = org.name;

    //teams modal
    const createTeamModal = document.getElementById("create_team_modal");
    const createTeamForm = document.getElementById("create_team_form");

    document.getElementById("create_team_btn").addEventListener("click", () => {
        createTeamModal.classList.remove("hidden");
    });
    document.getElementById("cancel_team_btn").addEventListener("click", () => {
        createTeamModal.classList.add("hidden");
    });

    createTeamForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(createTeamForm);
        const payload = {
            name: formData.get("name"),
            slug: formData.get("slug"),
            desc: formData.get("desc") || null,
        };
        const res = await API.post(`/orgs/${orgId}/teams/`, payload);
        if (!res.ok) {
            const err = await res.json();
            alert(err.detail ?? "Failed to create team.");
            return;
        }

        createTeamModal.classList.add("hidden");
        createTeamForm.reset();
        await loadTeams();
    });

    // Org members modal
    const addMemberModal = document.getElementById("add_member_modal");
    const addMemberForm = document.getElementById("add_member_form");

    document.getElementById("add_member_btn").addEventListener("click", () => {
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

        const res = await API.post(`/orgs/${orgId}/members`, payload);

        if (!res.ok) {
            const err = await res.json();
            alert(err.detail?.[0]?.msg ?? "Failed to add member.");
            return;
        }

        addMemberModal.classList.add("hidden");
        addMemberForm.reset();

        const membersRes = await API.get(`/orgs/${orgId}/members`);
        const members = membersRes.ok ? await membersRes.json() : [];
        document.getElementById("stat_members").textContent = members.length;
        renderOrgMembers(members);
    });

    // edit org modal
    const editOrgModal = document.getElementById("edit_org_modal");
    const editOrgForm = document.getElementById("edit_org_form");

    document.getElementById("edit_org_btn").addEventListener("click", () => {
        // pre-fill with current values
        document.getElementById("edit_org_name").value = org.name;
        document.getElementById("edit_org_slug").value = org.slug;
        document.getElementById("edit_org_desc").value = org.desc ?? "";
        editOrgModal.classList.remove("hidden");
    });

    document.getElementById("cancel_edit_btn").addEventListener("click", () => {
        editOrgModal.classList.add("hidden");
    });

    editOrgForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(editOrgForm);
        const payload = {
            name: formData.get("name"),
            slug: formData.get("slug"),
            desc: formData.get("desc") || null,
        };
        const res = await API.patch(`/orgs/${orgId}`, payload);
        if (res.ok) {
            const updated = await res.json();
            editOrgModal.classList.add("hidden");
            // update header and info card with new values
            document.getElementById("org_name_title").textContent =
                updated.name;
            document.getElementById("breadcrumb_org_name").textContent =
                updated.name;
            document.getElementById("info_name").textContent = updated.name;
            document.getElementById("info_slug").textContent = updated.slug;
            document.getElementById("info_desc").textContent =
                updated.desc ?? "—";
        }
    });

    // delete org modal
    const deleteOrgModal = document.getElementById("delete_org_modal");

    document.getElementById("delete_org_btn").addEventListener("click", () => {
        deleteOrgModal.classList.remove("hidden");
    });
    
    document
        .getElementById("cancel_delete_btn")
        .addEventListener("click", () => {
            deleteOrgModal.classList.add("hidden");
});

    document
        .getElementById("confirm_delete_btn")
        .addEventListener("click", async () => {
            const res = await API.delete(`/orgs/${orgId}`);
            if (!res?.ok) return;

            window.location.href = "/orgs.html";
        });
}

init();
