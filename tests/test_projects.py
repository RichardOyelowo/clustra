import uuid


async def create_project_parent(auth_client, prefix):
    org_response = await auth_client.post(
        "/orgs",
        json={
            "name": f"{prefix}_org",
            "slug": f"{prefix}_org_{uuid.uuid4().hex}",
            "desc": "this should be a successful org creation",
        },
    )
    assert org_response.status_code == 200, org_response.json()
    org = org_response.json()

    team_response = await auth_client.post(
        f"/orgs/{org['id']}/teams",
        json={
            "name": f"{prefix}_team",
            "slug": f"{prefix}_team_{uuid.uuid4().hex}",
            "desc": "this should be a successful team creation",
        },
    )
    assert team_response.status_code == 200, team_response.json()
    return org, team_response.json()


async def create_project(auth_client, org_id, team_id, prefix):
    response = await auth_client.post(
        f"/orgs/{org_id}/teams/{team_id}/projects",
        json={
            "name": f"{prefix}_project",
            "desc": "this should be a successful project creation",
            "team_id": team_id,
        },
    )
    assert response.status_code == 200, response.json()
    return response.json()


async def test_create_project(auth_client):
    org, team = await create_project_parent(auth_client, "test_create_project")
    project = await create_project(
        auth_client, org["id"], team["id"], "test_create_project"
    )
    assert project["name"] == "test_create_project_project"
    assert project["team_id"] == team["id"]


async def test_get_projects(auth_client):
    org, team = await create_project_parent(auth_client, "test_get_projects")
    project = await create_project(
        auth_client, org["id"], team["id"], "test_get_projects"
    )

    response = await auth_client.get(f"/orgs/{org['id']}/teams/{team['id']}/projects")
    assert response.status_code == 200, response.json()
    assert response.json()[0]["id"] == project["id"]


async def test_get_project(auth_client):
    org, team = await create_project_parent(auth_client, "test_get_project")
    project = await create_project(
        auth_client, org["id"], team["id"], "test_get_project"
    )

    response = await auth_client.get(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}"
    )
    assert response.status_code == 200, response.json()
    assert response.json()["id"] == project["id"]
    assert response.json()["name"] == project["name"]


async def test_update_project(auth_client):
    org, team = await create_project_parent(auth_client, "test_update_project")
    project = await create_project(
        auth_client, org["id"], team["id"], "test_update_project"
    )

    response = await auth_client.patch(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}",
        json={
            "name": "test_update_project_updated",
            "desc": "this is the updated project desc",
            "status": "active",
        },
    )
    assert response.status_code == 200, response.json()
    assert response.json()["name"] == "test_update_project_updated"
    assert response.json()["status"] == "active"


async def test_delete_project(auth_client):
    org, team = await create_project_parent(auth_client, "test_delete_project")
    project = await create_project(
        auth_client, org["id"], team["id"], "test_delete_project"
    )

    response = await auth_client.delete(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}"
    )
    assert response.status_code == 200, response.json()
