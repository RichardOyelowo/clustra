async def test_signup_success(client):
    response = await client.post(
        "/signup",
        json={
            "email": "testsignup@clustra.com",
            "full_name": "signuptest",
            "plain_password": "richpass123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testsignup@clustra.com"
    assert data["full_name"] == "signuptest"


async def test_signup_duplicate_email(client):
    user = await client.post(
        "/signup",
        json={
            "email": "testduplicate@clustra.com",
            "full_name": "signuptest01",
            "plain_password": "richpass123",
        },
    )
    duplicate_user = await client.post(
        "/signup",
        json={
            "email": "testduplicate@clustra.com",
            "full_name": "signuptest02",
            "plain_password": "richard",
        },
    )
    assert user.status_code == 200
    assert duplicate_user.status_code == 409


async def test_login_sucess(client):
    response = await client.post(
        "/signup",
        json={
            "email": "testlogin@clustra.com",
            "full_name": "signuptest03",
            "plain_password": "richpass123",
        },
    )
    assert response.status_code == 200
    user = response.json()

    response = await client.post(
        "/login", data={"username": user["email"], "password": "richpass123"}
    )
    assert response.status_code == 200, response.json()
    token = response.json()["access_token"]
    assert isinstance(token, str)


async def test_login_wrong_password(client):
    response = await client.post(
        "/signup",
        json={
            "email": "testlogin1@clustra.com",
            "full_name": "signuptest04",
            "plain_password": "richpass123",
        },
    )
    assert response.status_code == 200
    user = response.json()

    response = await client.post(
        "/login", data={"username": user["email"], "password": "richpass"}
    )
    assert response.status_code == 401


async def test_login_no_account(client):
    response = await client.post(
        "/login", data={"username": "testlogin2@clustra.com", "password": "richpass123"}
    )
    assert response.status_code == 401 # changed on frontend: prevent XSS attackers

