import uuid


async def create_label_parent(auth_client, prefix):
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


async def create_label(auth_client, org_id, team_id, proj_id, prefix):
    response = await auth_client.post(
        f"/orgs/{org_id}/teams/{team_id}/projects/{proj_id}/labels",
        json={
            "name": f"{prefix}_label",
            "color": "#ffffff",
        },
    )
    assert response.status_code == 200, response.json()
    return response.json()


async def create_task(auth_client, org_id, team_id, proj_id, prefix):
    response = await auth_client.post(
        f"/orgs/{org_id}/teams/{team_id}/projects/{proj_id}/tasks",
        json={
            "name": f"{prefix}_task",
            "desc": "this should be a successful task creation",
        },
    )
    assert response.status_code == 200, response.json()
    return response.json()


async def test_create_label(auth_client):
    org, team, project = await create_label_parent(auth_client, "test_create_label")
    label = await create_label(
        auth_client, org["id"], team["id"], project["id"], "test_create_label"
    )
    assert label["name"] == "test_create_label_label"
    assert label["proj_id"] == project["id"]


async def test_get_labels(auth_client):
    org, team, project = await create_label_parent(auth_client, "test_get_labels")
    label = await create_label(
        auth_client, org["id"], team["id"], project["id"], "test_get_labels"
    )

    response = await auth_client.get(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/labels"
    )
    assert response.status_code == 200, response.json()
    assert response.json()[0]["id"] == label["id"]


async def test_get_label(auth_client):
    org, team, project = await create_label_parent(auth_client, "test_get_label")
    label = await create_label(
        auth_client, org["id"], team["id"], project["id"], "test_get_label"
    )

    response = await auth_client.get(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/labels/{label['id']}"
    )
    assert response.status_code == 200, response.json()
    assert response.json()["id"] == label["id"]
    assert response.json()["name"] == label["name"]


async def test_update_label(auth_client):
    org, team, project = await create_label_parent(auth_client, "test_update_label")
    label = await create_label(
        auth_client, org["id"], team["id"], project["id"], "test_update_label"
    )

    response = await auth_client.patch(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/labels/{label['id']}",
        json={
            "name": "test_update_label_updated",
            "color": "#222222",
        },
    )
    assert response.status_code == 200, response.json()
    assert response.json()["name"] == "test_update_label_updated"
    assert response.json()["color"] == "#222222"


async def test_delete_label(auth_client):
    org, team, project = await create_label_parent(auth_client, "test_delete_label")
    label = await create_label(
        auth_client, org["id"], team["id"], project["id"], "test_delete_label"
    )

    response = await auth_client.delete(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/labels/{label['id']}"
    )
    assert response.status_code == 200, response.json()


async def test_create_task_label(auth_client):
    org, team, project = await create_label_parent(
        auth_client, "test_create_task_label"
    )
    label = await create_label(
        auth_client, org["id"], team["id"], project["id"], "test_create_task_label"
    )
    task = await create_task(
        auth_client, org["id"], team["id"], project["id"], "test_create_task_label"
    )

    response = await auth_client.post(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/labels/{label['id']}/task_label",
        json={"task_id": task["id"]},
    )
    assert response.status_code == 200, response.json()
    assert response.json()["label_id"] == label["id"]
    assert response.json()["task_id"] == task["id"]


async def test_get_task_labels(auth_client):
    org, team, project = await create_label_parent(auth_client, "test_get_task_labels")
    label = await create_label(
        auth_client, org["id"], team["id"], project["id"], "test_get_task_labels"
    )
    task = await create_task(
        auth_client, org["id"], team["id"], project["id"], "test_get_task_labels"
    )
    task_label = await auth_client.post(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/labels/{label['id']}/task_label",
        json={"task_id": task["id"]},
    )
    assert task_label.status_code == 200, task_label.json()

    response = await auth_client.get(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/labels/{label['id']}/task_label"
    )
    assert response.status_code == 200, response.json()
    assert response.json()[0]["id"] == task_label.json()["id"]


async def test_get_task_label(auth_client):
    org, team, project = await create_label_parent(auth_client, "test_get_task_label")
    label = await create_label(
        auth_client, org["id"], team["id"], project["id"], "test_get_task_label"
    )
    task = await create_task(
        auth_client, org["id"], team["id"], project["id"], "test_get_task_label"
    )
    task_label = await auth_client.post(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/labels/{label['id']}/task_label",
        json={"task_id": task["id"]},
    )
    assert task_label.status_code == 200, task_label.json()

    response = await auth_client.get(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/labels/{label['id']}/task_label/{task_label.json()['id']}"
    )
    assert response.status_code == 200, response.json()
    assert response.json()["id"] == task_label.json()["id"]


async def test_delete_task_label(auth_client):
    org, team, project = await create_label_parent(
        auth_client, "test_delete_task_label"
    )
    label = await create_label(
        auth_client, org["id"], team["id"], project["id"], "test_delete_task_label"
    )
    task = await create_task(
        auth_client, org["id"], team["id"], project["id"], "test_delete_task_label"
    )
    task_label = await auth_client.post(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/labels/{label['id']}/task_label",
        json={"task_id": task["id"]},
    )
    assert task_label.status_code == 200, task_label.json()

    response = await auth_client.delete(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/labels/{label['id']}/task_label/{task_label.json()['id']}"
    )
    assert response.status_code == 200, response.json()


async def test_create_task_label_wrong_project_not_found(auth_client):
    org, team, project = await create_label_parent(
        auth_client, "test_create_task_label_wrong_project"
    )
    other_project = await auth_client.post(
        f"/orgs/{org['id']}/teams/{team['id']}/projects",
        json={
            "name": f"test_create_task_label_wrong_project_{uuid.uuid4().hex}",
            "desc": "this should be a successful project creation",
            "team_id": team["id"],
        },
    )
    assert other_project.status_code == 200, other_project.json()
    label = await create_label(
        auth_client, org["id"], team["id"], project["id"], "test_create_task_label_wrong_project"
    )
    task = await create_task(
        auth_client, org["id"], team["id"], project["id"], "test_create_task_label_wrong_project"
    )

    response = await auth_client.post(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{other_project.json()['id']}/labels/{label['id']}/task_label",
        json={"task_id": task["id"]},
    )
    assert response.status_code == 404, response.json()
