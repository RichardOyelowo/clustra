import uuid


async def login_user(client, email, password):
    response = await client.post("/login", data={
        "username": email,
        "password": password,
    })
    assert response.status_code == 200, response.json()
    client.headers.update({"Authorization": f"Bearer {response.json()['access_token']}"})


async def create_logged_in_user(client, prefix):
    suffix = uuid.uuid4().hex[:12]
    safe_prefix = prefix[:30]
    email = f"{safe_prefix}_{suffix}@clustra.com"
    username = f"{safe_prefix}_{suffix}"
    password = "richpass123"

    response = await client.post("/signup", json={
        "email": email,
        "username": username,
        "plain_password": password,
    })
    assert response.status_code == 200, response.json()

    await login_user(client, email, password)
    return response.json()


async def test_get_current_user(client):
    user = await create_logged_in_user(client, "test_get_current_user")

    response = await client.get("/user/me")
    assert response.status_code == 200, response.json()
    assert response.json()["id"] == user["id"]
    assert response.json()["email"] == user["email"]
    assert response.json()["username"] == user["username"]
    assert response.json()["is_active"] is True


async def test_update_user(client):
    user = await create_logged_in_user(client, "test_update_user")
    suffix = uuid.uuid4().hex

    response = await client.patch(
        f"/user/{user['id']}",
        json={
            "email": f"updated_user_{suffix}@clustra.com",
            "username": f"updated_user_{suffix}",
        },
    )
    assert response.status_code == 200, response.json()
    assert response.json()["email"] == f"updated_user_{suffix}@clustra.com"
    assert response.json()["username"] == f"updated_user_{suffix}"


async def test_delete_user(client):
    user = await create_logged_in_user(client, "test_delete_user")

    response = await client.delete(f"/user/{user['id']}")
    assert response.status_code == 200, response.json()
    assert response.json()["status"] == "success"


async def test_update_other_user_forbidden(client):
    await create_logged_in_user(client, "test_update_other_user_owner")
    suffix = uuid.uuid4().hex[:12]
    other_user = await client.post("/signup", json={
        "email": f"test_update_other_user_{suffix}@clustra.com",
        "username": f"test_update_other_user_{suffix}",
        "plain_password": "richpass123",
    })
    assert other_user.status_code == 200, other_user.json()

    response = await client.patch(
        f"/user/{other_user.json()['id']}",
        json={"username": f"blocked_update_{suffix}"},
    )
    assert response.status_code == 403, response.json()


async def test_delete_other_user_forbidden(client):
    await create_logged_in_user(client, "test_delete_other_user_owner")
    suffix = uuid.uuid4().hex[:12]
    other_user = await client.post("/signup", json={
        "email": f"test_delete_other_user_{suffix}@clustra.com",
        "username": f"test_delete_other_user_{suffix}",
        "plain_password": "richpass123",
    })
    assert other_user.status_code == 200, other_user.json()

    response = await client.delete(f"/user/{other_user.json()['id']}")
    assert response.status_code == 403, response.json()


async def test_get_current_user_unauthenticated(client):
    response = await client.get("/user/me")
    assert response.status_code == 401
