import uuid


async def create_activity_parent(auth_client, prefix):
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


async def test_get_org_activity(auth_client):
    org, team, project = await create_activity_parent(auth_client, "test_get_org_activity")

    response = await auth_client.get(f"/orgs/{org['id']}/activity")
    assert response.status_code == 200, response.json()
    assert isinstance(response.json(), list)
    assert project["id"] in [activity["model_id"] for activity in response.json()]


async def test_get_project_activity(auth_client):
    org, team, project = await create_activity_parent(auth_client, "test_get_project_activity")

    response = await auth_client.get(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{project['id']}/activity"
    )
    assert response.status_code == 200, response.json()
    assert isinstance(response.json(), list)
    assert response.json()[0]["model_id"] == project["id"]


async def test_get_project_activity_project_not_found(auth_client):
    org, team, project = await create_activity_parent(
        auth_client, "test_get_project_activity_project_not_found"
    )

    response = await auth_client.get(
        f"/orgs/{org['id']}/teams/{team['id']}/projects/{uuid.uuid4()}/activity"
    )
    assert response.status_code == 404, response.json()


async def test_get_org_activity_unauthenticated(client):
    response = await client.get(f"/orgs/{uuid.uuid4()}/activity")
    assert response.status_code == 401

