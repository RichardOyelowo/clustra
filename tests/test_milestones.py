import uuid


async def create_milestone_parent(auth_client, prefix):
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


async def create_milestone(auth_client, org_id, team_id, proj_id, prefix):
    response = await auth_client.post(
        f"/orgs/{org_id}/teams/{team_id}/projects/{proj_id}/milestones",
        json={
            "title": f"{prefix}_milestone",
            "status": "pending",
        },
    )
    assert response.status_code == 200, response.json()
    return response.json()


async def test_create_milestone(auth_client):
    org, team, project = await create_milestone_parent(
        auth_client, "test_create_milestone"
    )
    milestone = await create_milestone(
        auth_client, org["id"], team["id"], project["id"], "test_create_milestone"
    )
    assert milestone["title"] == "test_create_milestone_milestone"
    assert milestone["proj_id"] == project["id"]


async def test_get_milestones(auth_client):
    org, team, project = await create_milestone_parent(
        auth_client, "test_get_milestones"
    )
    milestone = await create_milestone(
        auth_client, org["id"], team["id"], project["id"], "test_get_milestones"
    )

    response = await auth_client.get(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/milestones"
    )
    assert response.status_code == 200, response.json()
    assert response.json()[0]["id"] == milestone["id"]


async def test_get_milestone(auth_client):
    org, team, project = await create_milestone_parent(
        auth_client, "test_get_milestone"
    )
    milestone = await create_milestone(
        auth_client, org["id"], team["id"], project["id"], "test_get_milestone"
    )

    response = await auth_client.get(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/milestones/{milestone['id']}"
    )
    assert response.status_code == 200, response.json()
    assert response.json()["id"] == milestone["id"]
    assert response.json()["title"] == milestone["title"]


async def test_update_milestone(auth_client):
    org, team, project = await create_milestone_parent(
        auth_client, "test_update_milestone"
    )
    milestone = await create_milestone(
        auth_client, org["id"], team["id"], project["id"], "test_update_milestone"
    )

    response = await auth_client.patch(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/milestones/{milestone['id']}",
        json={
            "title": "test_update_milestone_updated",
            "status": "started",
        },
    )
    assert response.status_code == 200, response.json()
    assert response.json()["title"] == "test_update_milestone_updated"
    assert response.json()["status"] == "started"


async def test_delete_milestone(auth_client):
    org, team, project = await create_milestone_parent(
        auth_client, "test_delete_milestone"
    )
    milestone = await create_milestone(
        auth_client, org["id"], team["id"], project["id"], "test_delete_milestone"
    )

    response = await auth_client.delete(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/milestones/{milestone['id']}"
    )
    assert response.status_code == 200, response.json()
