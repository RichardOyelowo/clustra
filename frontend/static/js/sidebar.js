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

function navItem(item, label, count, config, isActive, icon_name) {
    let enabled, href, reason;

    switch (item) {
        case "organization":
            enabled = true;
            href = `/org.html?org_id=${config.orgId}`;
            break;
        case "teams":
            enabled = true;
            href = `/teams.html?org_id=${config.orgId}&section=teams`;
            break;
        case "projects":
            enabled = true;
            href = `/projects.html?org_id=${config.orgId}`;
            break;
        case "tasks":
            enabled = true;
            href = `/tasks.html?org_id=${config.orgId}`;
            break;

        case "milestones":
            enabled = true;
            href = `/milestones.html?org_id=${config.orgId}`;
            break;

        case "labels":
            enabled = true;
            href = `/labels.html?org_id=${config.orgId}`;
            break;
    }

    const countHTML =
        count !== undefined ? `<span class="nav_badge">${count}</span>` : "";

    if (!enabled) {
        return `<span class="nav_item disabled" title="${reason}"><span>${label}</span>${countHTML}</span>`;
    }
    return `<a href="${href}" class="nav_item ${isActive ? "active" : ""}">
                <span class="material-symbols-outlined nav_icon">${icon_name}</span>
                <span>${label}</span>${countHTML}
            </a>`;
}

export function renderSidebar(config) {
    if (!document.getElementById("material-symbols")) {
        const link = document.createElement("link");
        link.id = "material-symbols";
        link.rel = "stylesheet";
        link.href =
            "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined";
        document.head.appendChild(link);
    }

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
                ${navItem("organization", "Organization", undefined, config, config.activePage === "org", "corporate_fare")}
                ${navItem("teams", "Teams", config.counts.teams, config, config.activePage === "teams", "groups")}
                ${navItem("projects", "Projects", config.counts.projects, config, config.activePage === "projects", "account_tree")}
                ${navItem("tasks", "Tasks", config.counts.tasks, config, config.activePage === "tasks", "task_alt")}
                ${navItem("milestones", "Milestones", config.counts.milestones, config, config.activePage === "milestones", "flag")}
                ${navItem("labels", "Labels", undefined, config, config.activePage === "labels", "label")}
                <a href="/activity.html?org_id=${config.orgId}" class="nav_item ${config.activePage === "activity" ? "active" : ""}">
                    <span class="material-symbols-outlined nav_icon">analytics</span>
                    <span>Activity</span>
                </a>
            </nav>

            <div class="sidebar_bottom">
                <span class="nav_section">Settings</span>
                <a href="/settings.html?org_id=${config.orgId}" class="nav_item ${config.activePage === "settings" ? "active" : ""}">
                    <span class="material-symbols-outlined nav_icon">settings</span>
                    <span>Settings</span>
                </a>
                <a href="#" class="nav_item">
                    <span class="material-symbols-outlined nav_icon">contact_support</span>
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
