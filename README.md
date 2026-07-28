# Clustra

> Multi-tenant project management API and frontend built with FastAPI, PostgreSQL, async SQLAlchemy, and role-based access control. The frontend is vanilla JavaScript with ES Modules — no framework, no component library, no build step.

## Table of Contents

- [What It Is](#what-it-is)
- [Hierarchy](#hierarchy)
- [Stack](#stack)
- [Backend Architecture](#backend-architecture)
- [Auth](#auth)
- [Roles and Permissions](#roles-and-permissions)
- [Membership](#membership)
- [Tenant Isolation](#tenant-isolation)
- [Activity Logging](#activity-logging)
- [Cascade Deletes](#cascade-deletes)
- [Frontend Architecture](#frontend-architecture)
- [Sidebar](#sidebar)
- [Page Init Pattern](#page-init-pattern)
- [services.js](#servicesjs)
- [Delete Confirmation](#delete-confirmation)
- [Member Candidates](#member-candidates)
- [Project and Team Switcher](#project-and-team-switcher)
- [Row Limits](#row-limits)
- [Local Development](#local-development)
- [Docker](#docker)
- [Running Tests](#running-tests)
- [Current Status](#current-status)
- [Known Gaps](#known-gaps)

---

## What It Is

Clustra is a project management platform built around strict tenant isolation and clear service boundaries. Every resource belongs to an organization. Every permission check happens before data is read or written. The backend was built to be correct under real use, not just functional in a demo.

The frontend is vanilla JavaScript — no React, no Vue, no Tailwind. This was a deliberate choice to understand what the browser actually gives you before reaching for abstractions. It connects directly to the FastAPI backend with no intermediary.

---

## Hierarchy

```
Organization
    └── Team
            └── Project
                    ├── Task
                    ├── Label
                    └── Milestone
```

Activity is logged at the organization level and covers every resource type. Labels and milestones are scoped to projects, not teams or orgs. You cannot create a project without a team, and you cannot create a task without a project.

---

## Stack

**Backend**
- Python 3.12
- FastAPI
- async SQLAlchemy + asyncpg
- PostgreSQL
- Pydantic v2
- Alembic (migrations)
- gatevault (JWT auth — `pip install richard-gatevault`)
- Docker
- pytest-asyncio (47 tests passing)

**Frontend**
- Vanilla JavaScript with ES Modules
- Material Symbols Outlined (Google icon font)
- No framework, no bundler, no build step

---

## Backend Architecture

```
app/
  models/       SQLAlchemy ORM models
  schemas/      Pydantic request and response schemas
  routers/      FastAPI route handlers
  services/     business logic and database operations
  utils/
    permissions.py     role check utilities used across all services
    activity.py        log_activity() helper
    normalization.py   payload normalization before writes
  database.py   async session factory
  main.py       application entrypoint, static file serving, router registration
tests/          async integration tests
alembic/        database migrations
```

Routers handle HTTP only — path params, request validation, response serialization. Every route delegates immediately to a service method. Services own all business logic, permission checks, and database operations. This separation means the HTTP layer is thin and the logic layer is testable without an HTTP client.

Permission utilities in `app/utils/permissions.py` are centralized. Role checks are not written inline in service methods — they call `check_org_membership()` or `check_team_membership()` with the required role set. This keeps permission logic auditable in one place.

---

## Auth

Auth uses gatevault, a framework-agnostic Python authentication library published on PyPI. Token verification and user payload injection into protected routes happen through gatevault's dependency injection pattern — routes declare `current_user=Depends(validate_user)` and receive the decoded user object automatically.

The auth layer and RBAC layer are fully decoupled. gatevault handles token lifecycle. The service layer handles role checks. Neither knows about the other.

Access tokens expire in 15 minutes. Refresh token flow is deferred to v2.

---

## Roles and Permissions

**Organization roles:** Owner, Admin, Member

**Team roles:** Lead, Contributor, Viewer

Role sets are defined in `app/utils/permissions.py`:

```python
ORG_ANY_ROLES = {Owner, Admin, Member}
ORG_ADMIN_ROLES = {Owner, Admin}
ORG_OWNER_ROLES = {Owner}

TEAM_VIEW_ROLES = {Lead, Contributor, Viewer}
TEAM_CONTRIBUTION_ROLES = {Lead, Contributor}
TEAM_LEAD_ROLES = {Lead}
```

Every service method that reads or writes data calls the appropriate check before doing anything else. Org admins bypass team membership checks on read-only routes. All write operations require the correct team role regardless of org role.

When a user creates a team they are automatically added as a TeamMember with the Lead role. This prevents teams from existing with no one able to manage them.

---

## Membership

Org membership is a prerequisite for team membership. A user cannot belong to a team without first belonging to that team's organization. This is enforced at the service layer and at the database level through the membership hierarchy.

The original design allowed adding users directly to teams without checking org membership first. This was corrected mid-build. The team member candidate endpoint now returns org members minus existing team members — not all system users. This means every user who can be added to a team is guaranteed to already be an org member.

Removing a user from an org cascades correctly through their team memberships via configured cascade deletes.

---

## Tenant Isolation

Every database query is built with the authenticated user's ID as a hard filter at the ORM level. Org-scoped queries check that the requesting user is a member of that org before returning anything. Team-scoped queries check both org membership and team membership.

Cross-tenant data access is not possible by design. It is not prevented only by route-level checks that could be bypassed — the filter exists at the query construction level regardless of how the route is called.

---

## Activity Logging

Every create, update, and delete across all resource types writes an activity entry. The activity record stores:

- `user_id` — who took the action
- `action` — created, updated, or deleted
- `model_type` — which resource type (organizations, teams, projects, tasks, labels, milestones, organization_members, team_members)
- `model_id` — the ID of the affected record
- `org_id` — which organization this activity belongs to
- `created_at` — timestamp

Activity logging uses `db.flush()` not `db.commit()` at the point of logging. If the main operation fails, the activity entry does not persist independently. The commit happens once at the end of the service method so the activity log and the data change are always atomic.

---

## Cascade Deletes

Deleting an organization cascades through all teams, projects, tasks, labels, milestones, and membership records in that org.

Deleting a team cascades through its projects, tasks, labels, milestones, and team memberships.

`created_by` and `assignee_id` foreign keys are configured as SET NULL rather than CASCADE. Deleting a user removes their org and team memberships but does not delete the tasks or resources they created or were assigned to.

---

## Frontend Architecture

```
frontend/
  static/
    css/
      styles.css        shared design tokens, reset, navbar, modal, form, button styles
      sidebar.css       shared sidebar component styles
      {page}.css        page-specific styles — each imports styles.css and sidebar.css
    js/
      api.js            HTTP client — GET/POST/PATCH/DELETE, auto-attaches Bearer token
      auth.js           requireAuth() and logout()
      sidebar.js        renderSidebar(config) — builds and injects sidebar HTML
      services.js       data fetching helpers with error handling and user caching
      {page}.js         page logic
  {page}.html
```

Pages: `login`, `signup`, `orgs`, `org`, `teams`, `projects`, `tasks`, `milestones`, `labels`, `activity`, `settings`

FastAPI serves the frontend through a `StaticFiles` mount for `/static` and a catch-all route that serves HTML files from the `frontend/` directory. No separate frontend server is needed.

### api.js

`API.get()`, `API.post()`, `API.patch()`, and `API.delete()` all attach the Bearer token from localStorage automatically. `API.delete()` calls `window.confirm()` before making the request (see [Delete Confirmation](#delete-confirmation)).

### auth.js

`requireAuth()` checks for a token in localStorage and redirects to `/login.html` if none is found. `logout()` clears the token and redirects to `/login.html`. Every protected page calls `requireAuth()` at the top of its module before anything else runs.

---

## Sidebar

The sidebar is a single shared component. `renderSidebar(config)` builds the full sidebar HTML string and injects it into `#sidebar_mount` — a div that exists on every page except login, signup, and orgs. Nothing is duplicated across HTML files.

The config shape:

```js
{
    orgId,
    orgName,
    teamId,       // null if no team is in scope
    projectId,    // null if no project is in scope
    activePage,   // 'org' | 'teams' | 'projects' | 'tasks' | 'milestones' | 'labels' | 'activity' | 'settings'
    counts: { teams, projects, tasks, milestones },
    user: { initial, name, role }
}
```

**Collapse behavior:** the sidebar collapses to icon-only when not hovered and expands on hover using a pure CSS `width` transition on `.sidebar`. Labels, text, and badges use `opacity: 0` in the default state and `opacity: 1` on `.sidebar:hover` descendant selectors. Icons use Material Symbols Outlined and are excluded from the opacity rule using `:not(.material-symbols-outlined)` so they stay visible in the collapsed state.

**Nav item states:** items that require context that does not exist yet show as disabled with a `title` tooltip. Items that require a `teamId` (Projects) are disabled with "Create a team first" when `config.teamId` is null. Items that require a `projectId` (Tasks, Milestones, Labels) are disabled with "Create a project first" when `config.projectId` is null. Once context exists, links carry the full IDs needed to load the page correctly.

Material Symbols are injected via a dynamically created `<link>` tag inside `renderSidebar`. The link is only added if it does not already exist in the document head.

Logout is wired to the user row at the bottom of the sidebar after `mount.innerHTML` is set — it cannot be attached before because the element does not exist in the DOM until that point.

---

## Page Init Pattern

Every page follows the same initialization structure:

```js
requireAuth()

const params = new URLSearchParams(window.location.search)
const orgId = params.get('org_id')

async function init() {
    // 1. fetch org, teams, and current user in parallel
    const [org, teams, user] = await Promise.all([getOrg(orgId), getTeams(orgId), getUser()])

    if (!org) return

    // 2. default to first team or match team_id from URL
    currentTeam = teams.find(t => t.id === params.get('team_id')) ?? teams[0] ?? null

    // 3. fetch projects for selected team if one exists
    if (currentTeam) {
        allProjects = await getProjects(orgId, currentTeam.id)
        currentProject = allProjects[0] ?? null
    }

    // 4. always render sidebar with whatever context is available
    renderSidebar({ orgId, orgName: org.name, teamId: currentTeam?.id ?? null, ... })

    // 5. populate breadcrumb
    // 6. fetch and render page content
}

init()
```

The sidebar always renders even when teams or projects do not exist yet. Empty states on each page include a link to where the missing item can be created. This means no page ever shows a blank sidebar — even a first-time user with no teams sees the sidebar correctly.

---

## services.js

Shared data fetching helpers with built-in error logging. All functions return a sensible default (`null` or `[]`) on failure so pages can check for empty data without catching exceptions.

```js
getOrg(orgId)                           // GET /orgs/{orgId}
getTeams(orgId)                         // GET /orgs/{orgId}/teams
getProjects(orgId, teamId)              // GET /orgs/{orgId}/teams/{teamId}/projects
getOrgMembers(orgId)                    // GET /orgs/{orgId}/members
getTeamMembers(orgId, teamId)           // GET /orgs/{orgId}/teams/{teamId}/members
getTeamMemberCandidates(orgId, teamId)  // GET /orgs/{orgId}/teams/{teamId}/members/candidates
getUser()                               // GET /user/me
getUserInfo(userId)                     // GET /user/{userId} — cached
```

`getUserInfo()` caches results in a module-level object:

```js
const userCache = {}

export async function getUserInfo(userId) {
    if (userCache[userId]) return userCache[userId]
    const res = await API.get(`/user/${userId}`)
    if (!res.ok) return null
    const user = await res.json()
    userCache[userId] = user
    return user
}
```

This matters for activity feeds and member lists where the same user ID appears many times. Without caching, 10 activity items from the same user would fire 10 identical API requests.

---

## Delete Confirmation

`API.delete()` calls `window.confirm()` before making the request:

```js
async delete(url) {
    if (!confirm('Are you sure? This action cannot be undone.')) {
        return new Response(null, { status: 499, statusText: 'User Cancelled' })
    }
    const response = await fetch(url, { method: 'DELETE', headers: this.authHeaders() })
    return response
}
```

If the user cancels, a synthetic 499 response is returned. All calling code checks `res.ok` before proceeding. Confirmation logic lives in one place — not duplicated across every delete handler on every page.

---

## Member Candidates

When adding a member to a team, the modal populates a dropdown of eligible users rather than asking for a raw UUID. The candidates endpoint at `GET /orgs/{org_id}/teams/{team_id}/members/candidates` returns org members who are not already on the selected team.

The dropdown is populated on modal open, not on page load, to avoid fetching data that might never be used:

```js
document.getElementById('add_member_btn').addEventListener('click', async () => {
    await populateTeamMemberCandidates()
    addMemberModal.classList.remove('hidden')
})
```

A similar candidates pattern exists at the org level for adding org members — returning all system users who are not yet in the org.

---

## Project and Team Switcher

The teams page and project page include a breadcrumb switcher dropdown. Clicking the current team or project name in the breadcrumb opens a dropdown listing all available teams or projects. Selecting a different item re-fetches and re-renders the relevant content without a full page reload.

The URL updates silently using `history.replaceState` when a selection is made so the page remains bookmarkable and the back button behaves correctly.

---

## Row Limits

Overview tables and lists on dashboard pages cap at 5 items. This applies to the teams table on the org page, the projects list on the teams page, and the members list on the teams page. Full lists are available on each resource's dedicated page. The cap keeps dashboards readable without requiring pagination for v1.

---

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your database URL and secret key.

Run migrations:

```bash
alembic upgrade head
```

Start the server:

```bash
uvicorn app.main:app --reload
```

Open `http://localhost:8000` in your browser. The frontend is served directly by FastAPI.

---

## Docker

```bash
docker compose up
```

The Dockerfile uses `python:3.12-slim`. The startup script runs `alembic upgrade head` before starting uvicorn so schema state is always synchronized when the container starts.

---

## Running Tests

```bash
pytest
```

47 tests passing. Tests cover organization CRUD, team CRUD, project CRUD, task CRUD, label and milestone operations, membership management, cascade deletes, activity logging, and permission boundary enforcement. Tests use `pytest-asyncio` with an async SQLAlchemy test session that rolls back after each test.

---

## Current Status

**Backend:** complete. All models, schemas, services, routers, permissions, activity logging, migrations, and tests are done and passing.

**Frontend:** functional. All pages connect to real API data. Full CRUD works across organizations, teams, projects, tasks, milestones, and labels. The frontend is intentionally unpolished in places — it was built to be correct before it was built to be beautiful. A redesign toward a richer dashboard layout is planned for v2 alongside a TypeScript migration.

---

## Known Gaps

These are real limitations that exist intentionally and are documented for v2:

**Refresh token flow.** The access token expires in 15 minutes. The frontend does not silently refresh it — re-login is required after inactivity. The fix requires a refresh endpoint and a 401 interceptor in `api.js` that retries failed requests after refreshing.

**Task assignee UI.** The `assignee_id` field exists in the model and schema. The frontend displays the assigned user's name on task cards if present but there is no picker UI for assigning a user when creating or editing a task.

**Activity descriptions.** The activity feed shows action type and model type but not a human-readable description of what specifically changed. The `ActivityResponse` schema does not currently include a description field.

---

*Built for the love of development by Richard Oyelowo*
