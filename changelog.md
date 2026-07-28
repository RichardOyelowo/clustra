# Changelog

All notable changes to Clustra are documented here.

## [1.0.0] - 2026-07-28

First tagged release. Multi-tenant project management API and frontend, complete backend, functional frontend, connected end to end.

### Core platform

- Organization, team, and project hierarchy with strict tenant isolation enforced at the query level, not just at the route
- Role based access control across two layers, organization roles (Owner, Admin, Member) and team roles (Lead, Contributor, Viewer), with role sets centralized in `app/utils/permissions.py`
- Full CRUD across organizations, teams, projects, tasks, labels, and milestones
- Activity logging on every create, update, and delete across all resource types, written atomically with the operation it logs
- Cascade deletes through the full hierarchy, with `created_by` and `assignee_id` set to null on user deletion rather than cascading data loss
- Member candidate endpoints at both the org and team level, so adding someone means picking from a real list instead of pasting a UUID

### Auth and the refresh token flow

- Auth handled through gatevault, access tokens short lived at 15 minutes, refresh tokens long lived at 7 days
- Refresh tokens moved to an httpOnly cookie scoped to `/auth`, no longer reachable by any JavaScript on the page
- Access tokens moved to an in-memory variable on the frontend, dropped entirely from localStorage
- `/auth/refresh` added, rotates both tokens on every call through gatevault's `OAuthHandler.async_refresh()`
- `/auth/logout` added, clears the refresh cookie server side
- `validate_user` now checks the token's `type` claim, a refresh token can no longer be used at a protected route
- `get_user_by_id` wired into `OAuthHandler` so a refresh call rejects a deleted or deactivated account instead of trusting a stale signature
- `api.js` centralizes the retry-on-401 logic, one failed request triggers one refresh and one retry, every page module just calls `await requireAuth()` and stays unaware tokens exist at all
- Fixed a real bug in gatevault where two tokens minted for the same user in the same second came out byte identical, since JWT signing is deterministic and nothing in the payload varied at that resolution. Fixed with a random `jti` claim on every token
- Fixed the login enumeration gap, missing account and wrong password used to return different status codes, both now collapse to a generic 401
- Fixed a `MissingGreenlet` crash on team creation, caused by a leftover debug query touching an expired attribute between `commit()` and `refresh()`
- Fixed the `username` field mismatch on login and signup forms, both were sending the email under the wrong form key
- Fixed `type="module"` missing from script tags that needed `import` and top level `await`

### Known gaps, deferred to v2

- Refresh token reuse detection. Rotation happens on every call, but nothing tracks token history, so a stolen refresh token replayed before the legitimate user's next refresh is not currently detectable
- Task assignee picker UI, the field and display exist, the picker for setting it does not
- Activity feed descriptions, action and model type are shown, a human readable description of the specific change is not
