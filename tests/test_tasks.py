import uuid


async def create_task_parent(auth_client, prefix):
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
    team = team_response.json()

    project_response = await auth_client.post(
        f"/orgs/{org['id']}/teams/{team['id']}/projects",
        json={
            "name": f"{prefix}_project",
            "desc": "this should be a successful project creation",
            "team_id": team["id"],
        },
    )
    assert project_response.status_code == 200, project_response.json()
    return org, team, project_response.json()


async def create_task(auth_client, org_id, team_id, proj_id, prefix):
    response = await auth_client.post(
        f"/orgs/{org_id}/teams/{team_id}/projects/{proj_id}/tasks",
        json={
            "name": f"{prefix}_task",
            "desc": "this should be a successful task creation",
            "priority": "medium",
        },
    )
    assert response.status_code == 200, response.json()
    return response.json()


async def test_create_task(auth_client):
    org, team, project = await create_task_parent(auth_client, "test_create_task")
    task = await create_task(
        auth_client, org["id"], team["id"], project["id"], "test_create_task"
    )
    assert task["name"] == "test_create_task_task"
    assert task["priority"] == "medium"
    assert task["proj_id"] == project["id"]


async def test_get_tasks(auth_client):
    org, team, project = await create_task_parent(auth_client, "test_get_tasks")
    task = await create_task(
        auth_client, org["id"], team["id"], project["id"], "test_get_tasks"
    )

    response = await auth_client.get(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/tasks"
    )
    assert response.status_code == 200, response.json()
    assert response.json()[0]["id"] == task["id"]


async def test_get_task(auth_client):
    org, team, project = await create_task_parent(auth_client, "test_get_task")
    task = await create_task(
        auth_client, org["id"], team["id"], project["id"], "test_get_task"
    )

    response = await auth_client.get(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/tasks/{task['id']}"
    )
    assert response.status_code == 200, response.json()
    assert response.json()["id"] == task["id"]
    assert response.json()["name"] == task["name"]


async def test_update_task(auth_client):
    org, team, project = await create_task_parent(auth_client, "test_update_task")
    task = await create_task(
        auth_client, org["id"], team["id"], project["id"], "test_update_task"
    )

    response = await auth_client.patch(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/tasks/{task['id']}",
        json={
            "name": "test_update_task_updated",
            "status": "active",
            "priority": "critical",
        },
    )
    assert response.status_code == 200, response.json()
    assert response.json()["name"] == "test_update_task_updated"
    assert response.json()["status"] == "active"
    assert response.json()["priority"] == "critical"


async def test_delete_task(auth_client):
    org, team, project = await create_task_parent(auth_client, "test_delete_task")
    task = await create_task(
        auth_client, org["id"], team["id"], project["id"], "test_delete_task"
    )

    response = await auth_client.delete(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/tasks/{task['id']}"
    )
    assert response.status_code == 200, response.json()
