import uuid


async def test_get_current_user(auth_client):
    response = await auth_client.get("/user/me")
    assert response.status_code == 200, response.json()
    assert response.json()["email"] == "testuser@clustra.com"
    assert response.json()["username"] == "testuser"
    assert response.json()["is_active"] is True


async def test_update_user(auth_client):
    suffix = uuid.uuid4().hex
    user_response = await auth_client.post(
        "/signup",
        json={
            "email": f"update_user_{suffix}@clustra.com",
            "username": f"update_user_{suffix}",
            "plain_password": "richpass123",
        },
    )
    assert user_response.status_code == 200, user_response.json()

    response = await auth_client.patch(
        f"/user/{user_response.json()['id']}",
        json={
            "email": f"updated_user_{suffix}@clustra.com",
            "username": f"updated_user_{suffix}",
        },
    )
    assert response.status_code == 200, response.json()
    assert response.json()["email"] == f"updated_user_{suffix}@clustra.com"
    assert response.json()["username"] == f"updated_user_{suffix}"


async def test_delete_user(auth_client):
    suffix = uuid.uuid4().hex
    user_response = await auth_client.post(
        "/signup",
        json={
            "email": f"delete_user_{suffix}@clustra.com",
            "username": f"delete_user_{suffix}",
            "plain_password": "richpass123",
        },
    )
    assert user_response.status_code == 200, user_response.json()

    response = await auth_client.delete(f"/user/{user_response.json()['id']}")
    assert response.status_code == 200, response.json()
    assert response.json()["status"] == "success"
