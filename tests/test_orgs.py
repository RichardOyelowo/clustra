import uuid


async def test_create_org(auth_client):
    response = await auth_client.post(
        "/orgs",
        json={
            "name": "test_org",
            "slug": "test_create_org",
            "desc": "this should be a successful org creation",
        },
    )
    assert response.status_code == 200, response.json()
    assert response.json()["name"] == "test_org"
    assert response.json()["slug"] == "test_create_org"
    assert isinstance(response.json()["desc"], str)


async def test_get_user_orgs(auth_client):
    response = await auth_client.post(
        "/orgs",
        json={
            "name": "test_get_user_orgs",
            "slug": "test_get_user_orgs_slug",
            "desc": "this should be a successful org creation"
        },
    )
    assert response.status_code == 200, response.json()

    orgs_response = await auth_client.get("/orgs")
    assert orgs_response.status_code == 200, orgs_response.json()
    assert orgs_response.json()[1]["id"] == response.json()["id"]


async def test_get_user_orgs_empty(client):
    # fresh client with no orgs
    await client.post("/signup", json={
        "email": "emptyorgs@clustra.com",
        "username": "emptyorgs",
        "plain_password": "testpass123"
    })
    response = await client.post("/login", data={
        "username": "emptyorgs@clustra.com",
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    
    orgs = await client.get("/orgs")
    assert orgs.status_code == 200
    assert len(orgs.json()) == 0
 

async def test_create_org_duplicate_slug(auth_client):
    response = await auth_client.post(
        "/orgs",
        json={
            "name": "test_org_2",
            "slug": "test_create_org",
            "desc": "this should fail because the 'slug' matches previous org",
        },
    )
    assert response.status_code == 409


async def test_get_org(auth_client):
    response = await auth_client.post(
        "/orgs",
        json={
            "name": "test_get_org",
            "slug": "test_get_org_slug",
            "desc": "this should be a successful org creation",
        },
    )
    assert response.status_code == 200, response.json()

    # calls to get the org object
    org_response = await auth_client.get(f"/orgs/{response.json()['id']}")
    assert org_response.status_code == 200, org_response.json()
    body = org_response.json()

    assert body["id"] == response.json()["id"]
    assert body["name"] == "test_get_org"
    assert body["slug"] == "test_get_org_slug"
    assert body["desc"] == "this should be a successful org creation"


async def test_org_not_found(auth_client):
    response = await auth_client.get(f"/orgs/{uuid.uuid4()}")
    assert response.status_code == 403


async def test_update_org(auth_client):
    response = await auth_client.post(
        "/orgs",
        json={
            "name": "test_update_org",
            "slug": "test_update_org_slug",
            "desc": "this should be a successful org creation",
        },
    )
    org = await auth_client.patch(
        f"/orgs/{response.json()['id']}",
        json={
            "name": "test_update_org_updated",
            "desc": "this is the updated desc",
        },
    )
    assert response.status_code == 200, response.json()
    assert org.status_code == 200, org.json()
    assert org.json()["name"] == "test_update_org_updated"
    assert org.json()["desc"] == "this is the updated desc"

async def test_delete_org(auth_client):
    response = await auth_client.post(
        "/orgs",
        json={
            "name": "test_delete_org",
            "slug": "test_delete_org_slug",
            "desc": "this should be a successful org creation",
        },
    )
    deletion = await auth_client.delete(f'/orgs/{response.json()["id"]}')
    assert deletion.status_code == 200


async def create_user(auth_client, prefix):
    suffix = uuid.uuid4().hex[:12]
    safe_prefix = prefix[:30]
    response = await auth_client.post("/signup", json={
        "email": f"{safe_prefix}_{suffix}@clustra.com",
        "username": f"{safe_prefix}_{suffix}",
        "plain_password": "richpass123",
    })
    assert response.status_code == 200, response.json()
    return response.json()


async def test_add_org_member(auth_client):
    org = await auth_client.post(
        "/orgs",
        json={
            "name": "test_add_org_member",
            "slug": f"test_add_org_member_{uuid.uuid4().hex}",
            "desc": "this should be a successful org creation",
        },
    )
    assert org.status_code == 200, org.json()
    user = await create_user(auth_client, "test_add_org_member")

    response = await auth_client.post(
        f"/orgs/{org.json()['id']}/members",
        json={"user_id": user["id"], "role": "member"},
    )
    assert response.status_code == 200, response.json()
    assert response.json()["user_id"] == user["id"]
    assert response.json()["role"] == "member"


async def test_get_org_members(auth_client):
    org = await auth_client.post(
        "/orgs",
        json={
            "name": "test_get_org_members",
            "slug": f"test_get_org_members_{uuid.uuid4().hex}",
            "desc": "this should be a successful org creation",
        },
    )
    assert org.status_code == 200, org.json()
    user = await create_user(auth_client, "test_get_org_members")
    member = await auth_client.post(
        f"/orgs/{org.json()['id']}/members",
        json={"user_id": user["id"], "role": "member"},
    )
    assert member.status_code == 200, member.json()

    response = await auth_client.get(f"/orgs/{org.json()['id']}/members")
    assert response.status_code == 200, response.json()
    assert member.json()["id"] in [item["id"] for item in response.json()]


async def test_get_org_member(auth_client):
    org = await auth_client.post(
        "/orgs",
        json={
            "name": "test_get_org_member",
            "slug": f"test_get_org_member_{uuid.uuid4().hex}",
            "desc": "this should be a successful org creation",
        },
    )
    assert org.status_code == 200, org.json()
    user = await create_user(auth_client, "test_get_org_member")
    member = await auth_client.post(
        f"/orgs/{org.json()['id']}/members",
        json={"user_id": user["id"], "role": "member"},
    )
    assert member.status_code == 200, member.json()

    response = await auth_client.get(
        f"/orgs/{org.json()['id']}/members/{member.json()['id']}"
    )
    assert response.status_code == 200, response.json()
    assert response.json()["id"] == member.json()["id"]


async def test_remove_org_member(auth_client):
    org = await auth_client.post(
        "/orgs",
        json={
            "name": "test_remove_org_member",
            "slug": f"test_remove_org_member_{uuid.uuid4().hex}",
            "desc": "this should be a successful org creation",
        },
    )
    assert org.status_code == 200, org.json()
    user = await create_user(auth_client, "test_remove_org_member")
    member = await auth_client.post(
        f"/orgs/{org.json()['id']}/members",
        json={"user_id": user["id"], "role": "member"},
    )
    assert member.status_code == 200, member.json()

    response = await auth_client.delete(
        f"/orgs/{org.json()['id']}/members/{member.json()['id']}"
    )
    assert response.status_code == 200, response.json()


async def test_add_org_member_duplicate(auth_client):
    org = await auth_client.post(
        "/orgs",
        json={
            "name": "test_add_org_member_duplicate",
            "slug": f"test_add_org_member_duplicate_{uuid.uuid4().hex}",
            "desc": "this should be a successful org creation",
        },
    )
    assert org.status_code == 200, org.json()
    user = await create_user(auth_client, "test_add_org_member_duplicate")
    first_member = await auth_client.post(
        f"/orgs/{org.json()['id']}/members",
        json={"user_id": user["id"], "role": "member"},
    )
    assert first_member.status_code == 200, first_member.json()

    duplicate_member = await auth_client.post(
        f"/orgs/{org.json()['id']}/members",
        json={"user_id": user["id"], "role": "member"},
    )
    assert duplicate_member.status_code == 409
