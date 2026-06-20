// config shape:
// {
//     orgId, orgName,
//     teamId,     // null until a team is selected
//     projectId,  // null until a project is selected
//     activePage, // 'org' | 'teams' | 'team' | 'project' | 'tasks' | 'milestones' | 'labels' | 'activity' | 'settings'
//     counts: { teams, projects, tasks, milestones },
//     user: { initial, name, role }
// }

import { logout } from "./auth.js";

function navItem(item, label, count, config, isActive) {
    let enabled, href, reason;

    switch (item) {
        case "organization":
            enabled = true;
            href = `/org.html/org_id=${config.orgId}`;
            break;

        case "teams":
            enabled = true;
            href = `/org.html?org_id=${config.orgId}&team_id=${config.teamId}`;
            break;

        case "projects":
            if (!config.teamId) {
                enabled = false;
                reason = "Select a team first";
            } else {
                enabled = true;
                href = `/team.html?org_id=${config.orgId}&team_id=${config.teamId}&proj_id=${config.projectId}`;
            }
            break;

        case "tasks":
        case "milestones":
        case "labels":
            if (!config.projectId) {
                enabled = false;
                reason = "Select a project first";
            } else {
                enabled = true;
                href = `/project.html?org=${config.orgId}&team_id=${config.teamId}&proj_id=${config.projectId}`;
            }
            break;
    }
    const countHTML =
        count !== undefined ? `<span class="nav_badge">${count}</span>` : "";

    if (!enabled) {
        return `<span class="nav_item disabled" title="${reason}"><span>${label}</span>${countHTML}</span>`;
    }
    return `<a href="${href}" class="nav_item ${isActive ? "active" : ""}"><span>${label}</span>${countHTML}</a>`;
}

export function renderSidebar(config) {
    const mount = document.getElementById("sidebar_mount");

    mount.innerHTML = `
        <aside class="sidebar">
            <div class="sidebar_brand">
                <div class="brand_icon"></div>
                <div class="brand_text">
                    <span class="brand_name">Clustra</span>
                    <span class="brand_sub">${config.orgName ?? ""}</span>
                </div>
            </div>
            
            <nav class="sidebar_nav">
                <span class="nav_section">Workspace</span>
                ${navItem("organization", "Organization", undefined, config, config.activePage === "org")}
                ${navItem("teams", "Teams", config.counts.teams, config, config.activePage === "teams")}
                ${navItem("projects", "Projects", config.counts.projects, config, config.activePage === "projects")}
                ${navItem("tasks", "Tasks", config.counts.tasks, config, config.activePage === "tasks")}
                ${navItem("milestones", "Milestones", config.counts.milestones, config, config.activePage === "milestones")}
                ${navItem("labels", "Labels", undefined, config, config.activePage === "labels")}
                <a href="/activity.html?id=${config.orgId}" class="nav_item ${config.activePage === "activity" ? "active" : ""}">
                    <span>Activity</span>
                </a>
            </nav>

            <div class="sidebar_bottom">
                <span class="nav_section">Settings</span>
                <a href="/settings.html?org_id=${config.orgId}" class="nav_item ${config.activePage === "settings" ? "active" : ""}">
                    <span>Settings</span>
                </a>
                <a href="#" class="nav_item">
                    <span>Support</span>
                </a>
                <div class="user_row" id="sidebar_logout">
                    <div class="avatar">${config.user.initial}</div>
                    <div class="user_info">
                        <span class="user_name">${config.user.name}</span>
                        <span class="user_role">${config.user.role}</span>
                    </div>
                </div>
            </div>
        </aside>
    `;

    // wire up logout AFTER innerHTML is set
    document.getElementById("sidebar_logout").addEventListener("click", logout);
}
