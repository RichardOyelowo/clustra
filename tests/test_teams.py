import uuid


async def create_org(auth_client, prefix):
    response = await auth_client.post(
        "/orgs",
        json={
            "name": f"{prefix}_org",
            "slug": f"{prefix}_org_{uuid.uuid4().hex}",
            "desc": "this should be a successful org creation",
        },
    )
    assert response.status_code == 200, response.json()
    return response.json()


async def create_team(auth_client, org_id, prefix):
    response = await auth_client.post(
        f"/orgs/{org_id}/teams",
        json={
            "name": f"{prefix}_team",
            "slug": f"{prefix}_team_{uuid.uuid4().hex}",
            "desc": "this should be a successful team creation",
        },
    )
    assert response.status_code == 200, response.json()
    return response.json()


async def test_create_team(auth_client):
    org = await create_org(auth_client, "test_create_team")
    team = await create_team(auth_client, org["id"], "test_create_team")
    assert team["name"] == "test_create_team_team"
    assert isinstance(team["desc"], str)


async def test_get_teams(auth_client):
    org = await create_org(auth_client, "test_get_teams")
    team = await create_team(auth_client, org["id"], "test_get_teams")

    response = await auth_client.get(f"/orgs/{org['id']}/teams")
    assert response.status_code == 200, response.json()
    assert response.json()[0]["id"] == team["id"]


async def test_get_team(auth_client):
    org = await create_org(auth_client, "test_get_team")
    team = await create_team(auth_client, org["id"], "test_get_team")

    response = await auth_client.get(f"/orgs/{org['id']}/teams/{team['id']}")
    assert response.status_code == 200, response.json()
    assert response.json()["id"] == team["id"]
    assert response.json()["name"] == team["name"]


async def test_update_team(auth_client):
    org = await create_org(auth_client, "test_update_team")
    team = await create_team(auth_client, org["id"], "test_update_team")

    response = await auth_client.patch(
        f"/orgs/{org['id']}/teams/{team['id']}",
        json={
            "name": "test_update_team_updated",
            "desc": "this is the updated team desc",
        },
    )
    assert response.status_code == 200, response.json()
    assert response.json()["name"] == "test_update_team_updated"
    assert response.json()["desc"] == "this is the updated team desc"


async def test_delete_team(auth_client):
    org = await create_org(auth_client, "test_delete_team")
    team = await create_team(auth_client, org["id"], "test_delete_team")

    response = await auth_client.delete(f"/orgs/{org['id']}/teams/{team['id']}")
    assert response.status_code == 200, response.json()


async def test_add_team_member(auth_client):
    org = await create_org(auth_client, "test_add_team_member")
    team = await create_team(auth_client, org["id"], "test_add_team_member")
    suffix = uuid.uuid4().hex
    user = await auth_client.post(
        "/signup",
        json={
            "email": f"team_member_{suffix}@clustra.com",
            "username": f"team_member_{suffix}",
            "plain_password": "richpass123",
        },
    )
    assert user.status_code == 200, user.json()

    response = await auth_client.post(
        f"/orgs/{org['id']}/teams/{team['id']}/members",
        json={
            "user_id": user.json()["id"],
            "role": "contributor",
        },
    )
    assert response.status_code == 200, response.json()
    assert response.json()["role"] == "contributor"


async def test_get_team_members(auth_client):
    org = await create_org(auth_client, "test_get_team_members")
    team = await create_team(auth_client, org["id"], "test_get_team_members")

    response = await auth_client.get(f"/orgs/{org['id']}/teams/{team['id']}/members")
    assert response.status_code == 200, response.json()
    assert isinstance(response.json(), list)


async def test_get_team_member(auth_client):
    org = await create_org(auth_client, "test_get_team_member")
    team = await create_team(auth_client, org["id"], "test_get_team_member")
    suffix = uuid.uuid4().hex
    user = await auth_client.post(
        "/signup",
        json={
            "email": f"get_team_member_{suffix}@clustra.com",
            "username": f"get_team_member_{suffix}",
            "plain_password": "richpass123",
        },
    )
    assert user.status_code == 200, user.json()
    member = await auth_client.post(
        f"/orgs/{org['id']}/teams/{team['id']}/members",
        json={"user_id": user.json()["id"], "role": "viewer"},
    )
    assert member.status_code == 200, member.json()

    response = await auth_client.get(
        f"/orgs/{org['id']}/teams/{team['id']}/members/{member.json()['id']}"
    )
    assert response.status_code == 200, response.json()
    assert response.json()["id"] == member.json()["id"]


async def test_remove_team_member(auth_client):
    org = await create_org(auth_client, "test_remove_team_member")
    team = await create_team(auth_client, org["id"], "test_remove_team_member")
    suffix = uuid.uuid4().hex
    user = await auth_client.post(
        "/signup",
        json={
            "email": f"remove_team_member_{suffix}@clustra.com",
            "username": f"remove_team_member_{suffix}",
            "plain_password": "richpass123",
        },
    )
    assert user.status_code == 200, user.json()
    member = await auth_client.post(
        f"/orgs/{org['id']}/teams/{team['id']}/members",
        json={"user_id": user.json()["id"], "role": "viewer"},
    )
    assert member.status_code == 200, member.json()

    response = await auth_client.delete(
        f"/orgs/{org['id']}/teams/{team['id']}/members/{member.json()['id']}"
    )
    assert response.status_code == 200, response.json()
