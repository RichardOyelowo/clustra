# Clustra — Decisions, Edge Cases, and Build Context

This document covers every meaningful decision made during the Clustra build, why it was made, edge cases encountered, and how they were resolved. Written as reference for the README, portfolio context, and future development.

---

## Architecture Decisions

### Hierarchy: Org -> Team -> Project -> Task

The hierarchy was locked early. Labels and milestones belong to projects, not teams or orgs. Activity is logged at the org level and covers every model type. This mirrors how Linear and Jira actually structure data — ownership is clear at every level and there is no ambiguity about where something belongs.

### Membership Layering

Original approach: users could be added directly to teams without being org members first. This was wrong architecturally and was fixed mid-build.

Correct approach: org membership is a prerequisite for team membership. The candidate endpoint for adding team members returns org members minus existing team members, not all system users. This means removing someone from an org correctly invalidates their team membership at the database level through cascade deletes.

The architecture in plain terms:
```
System Users
    |
    v
Organization Members
    |
    v
Team Members (subset of org members)
```

### Role Separation

Org roles (Owner, Admin, Member) and team roles (Lead, Contributor, Viewer) are independent. Someone can be an Org Admin but a Viewer on a specific team. Role checks run at the service layer using centralized permission utilities, not scattered across routes. This was a deliberate decision to make permission logic auditable in one place.

Org admins bypass team membership checks on read-only routes. All other operations check both org and team membership independently.

### Automatic Team Lead on Creation

When a user creates a team they are automatically added as a TeamMember with the Lead role. This prevents the edge case of a team existing with no lead and no one able to manage it.

### Activity Logging

Every create, update, and delete logs an activity entry. The log uses `db.flush()` not `db.commit()` at the point of logging, so if the main operation fails the activity entry does not persist independently. The commit happens once at the end of the service method. This was a deliberate decision to keep activity logging atomic with the operation it describes.

### Cross-Tenant Isolation

Every database query is constructed with the authenticated user's ID as a hard filter at the ORM level. Cross-tenant data access is not possible by design. Controller-level checks alone were considered insufficient — the filter exists at the query level regardless of what the route handler does.

---

## Backend Edge Cases and Fixes

### Cascade Deletes

Cascade deletes were configured as SET NULL for created_by and assignee_id foreign keys, and CASCADE for membership and ownership relationships. This means deleting a user does not orphan their tasks but does remove their team and org memberships.

### ProjectCreate Schema

The team_id field was removed from ProjectCreate because it comes from the URL path parameter, not the request body. Leaving it in the schema would allow clients to pass a different team_id in the body than the one in the URL, creating a mismatch. The fix was removing the field from the schema entirely.

### OrganizationMember Timestamp

OrganizationMember and TeamMember models did not originally inherit from TimeStamp. This caused a ResponseValidationError when BaseResponse was updated to include created_at and updated_at. The fix was adding TimeStamp to those models and running a migration with server_default=sa.text('now()') so existing rows got a valid timestamp instead of failing a NOT NULL constraint.

### Username Removed

Username was removed from the User model entirely. Clustra is a project management tool, not a social platform. Full name is used for display everywhere. Since display names are not used to affect database logic or enforce uniqueness, duplicate names are acceptable.

### UserPublicResponse Schema

A separate UserPublicResponse schema was created with only id and full_name. This is what gets returned from the user info endpoint and the candidates endpoint. The full UserResponse is only used for the authenticated user's own profile.

---

## Frontend Decisions

### Vanilla JS, No Framework

The frontend was built in vanilla JavaScript with ES Modules. No React, no Vue, no Tailwind, no Bootstrap. This was intentional — the goal was to understand what the browser gives you before reaching for abstractions. Clustra is used as the learning vehicle for JS before moving to TypeScript in v2.

### Single Shared Sidebar

The sidebar is a single renderSidebar(config) function that injects HTML into a #sidebar_mount div on every page. It is not duplicated across HTML files. This means changing one nav item updates every page.

The sidebar collapses to icons only when not hovered and expands on hover using a pure CSS width transition. Labels fade in using opacity transition on the :hover selector.

### Icon Rail with Material Symbols

Material Symbols are injected once via a dynamically created link tag inside renderSidebar. The link is only added if it does not already exist. Icons are always visible in collapsed state. Labels and badges are hidden with opacity: 0 and revealed on hover using .sidebar:hover descendant selectors. The material-symbols-outlined class is excluded from the opacity rule using :not() so icons stay visible.

### Progressive Sidebar Rendering

Every page renders the sidebar with whatever context is available at that point — even if teams or projects do not exist yet. The sidebar shows disabled states with tooltips explaining what needs to be created first. This prevents blank sidebars on first use and makes the empty state useful rather than just broken-looking.

### Page Init Pattern

Every page follows the same init structure:
1. Fetch org, teams, and current user in parallel with Promise.all
2. Default to first team or match team_id from URL if present
3. Fetch projects for selected team
4. Render sidebar with available context
5. Populate breadcrumb
6. Fetch and render page content

This pattern means pages are consistent, predictable, and handle empty states at every level.

### URL Params for Team and Project Context

URL params carry team_id and project_id. Pages read these on load and match against fetched data, falling back to the first item if the URL param is missing or not found. history.replaceState updates the URL silently when a default is applied so the URL stays bookmarkable.

### getUserInfo Caching

getUserInfo(userId) caches results in a module-level object in services.js. Repeated calls for the same user ID in the same page session return the cached value without hitting the API again. This matters most on activity feeds and member lists where the same user might appear many times.

### Delete Confirmation

API.delete() calls window.confirm() before making the request. If the user cancels, the method returns a synthetic Response with status 499. All calling code checks res.ok before proceeding. This keeps confirmation logic in one place rather than scattered across every delete handler. The 499 status was chosen because it is outside the range of standard HTTP responses so it cannot be confused with a real server response.

### Row Limits

Tables and lists cap at 5 items. This was applied to teams table on org page, projects list on teams page, members list on teams page, and activity feed on org page. The cap keeps the dashboard readable without requiring pagination for v1. A "View All" link was considered and removed — the dedicated page for each resource handles full lists.

### Member Candidates Dropdown

The add team member modal shows a dropdown of eligible users instead of asking for a UUID. The candidates endpoint returns org members minus existing team members. The dropdown is populated on modal open, not on page load, to avoid fetching data that might never be used. The HTML select element ID must match exactly what the JS expects — a mismatch caused a silent failure where the dropdown appeared empty.

### Tasks and Projects: name not title

The task and project models use name as the field, not title. This was caught during frontend wiring when the API returned name but the JS was reading task.title and rendering empty cells. The fix was aligning field names across the payload (what gets sent) and the render functions (what gets read from the response).

---

## Known Deferred Issues

These exist intentionally and are documented for v2:

**Refresh token flow.** The access token expires in 15 minutes. The frontend does not silently refresh it. Re-login is required after inactivity. The fix requires a refresh endpoint in gatevault and an interceptor in api.js that catches 401 responses, attempts a token refresh, and retries the original request.

**Label color field.** The color picker exists in the frontend form and CSS. The Label model does not have a color column yet. A migration is needed to add color: Mapped[str] with a default value.

**Task assignee UI.** The assignee_id field exists in the model and schema. The frontend shows the assigned user's name on the task card if present, but there is no UI to assign a user to a task during creation or editing.

**Org member candidates.** The team add member modal uses a proper dropdown. The org add member form still takes a user_id manually. An org-level candidates endpoint was considered but not built — it would return all system users who are not already org members.

**Activity descriptions.** The activity feed shows action type and model type but not a human-readable description of what changed. This is a backend schema limitation — the current ActivityResponse does not store a description field.

---

## Financial and Learning Context

This section covers decisions made about learning path and career direction during the Clustra build period.

### Why Vanilla JS Before TypeScript

TypeScript was deliberately deferred until after Clustra frontend was complete. The reasoning: TypeScript is JavaScript with a type system. Learning JS properly first through real DOM work, async patterns, and ES modules means TS concepts click faster and the type system feels like a tool rather than an obstacle. Clustra is the JS learning vehicle. The TypeScript GateProxy SDK is the TS learning vehicle.

### Why Go Next

After Clustra, the next project is GateProxy — a reverse proxy and API gateway in Go. The reason Go is next rather than TypeScript or C++ is positioning. FastAPI CRUD developer is a flooded job market. Backend infrastructure engineer with a working Go reverse proxy and real benchmarks is a much smaller candidate pool. Go was chosen over alternatives because it is the dominant language for infrastructure services, has excellent concurrency primitives, and the official tour is genuinely good for self-teaching.

### Learning Roadmap Order

Phase 0: Finish Clustra (done)
Phase 1: Go fundamentals + GateProxy (core features, tests, benchmarks, architecture docs)
Phase 2: DSA in C using Abdul Bari's course (overlaps with Phase 1)
Phase 3: TypeScript SDK for GateProxy
Phase 4: C++ Deep Dive + TinyStore or StoneKV
Background: Khan Academy math (Algebra through Linear Algebra and Calculus basics)

The math track runs quietly alongside everything else with no deadline. It feeds into an eventual AI/ML phase that sits beyond this roadmap.

### Product Idea: API Monitoring Tool

A lightweight API monitoring and uptime tool was identified as the most viable fast-revenue product given the current financial situation. The reasoning: largest proven audience among developer tools, proven willingness to pay ($9-19/month is an easy yes for a developer at a company), lowest trust barrier (monitoring does not touch user data), and buildable in 4 weeks with the existing stack (FastAPI, PostgreSQL, Railway). Core features: endpoint checks, latency tracking, incident logging, email alerts, Stripe billing with free and paid tiers. This was identified as having better revenue and traffic prospects than a webhook dashboard or API rate-limiting proxy, which were the other candidates considered.
