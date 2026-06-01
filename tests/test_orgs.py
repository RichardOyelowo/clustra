import uuid
import pytest


async def test_create_org(auth_client):
    response = await auth_client.post(
        "/org",
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


async def test_create_org_duplicate_slug(auth_client):
    response = await auth_client.post(
        "/org",
        json={
            "name": "test_org_2",
            "slug": "test_create_org",
            "desc": "this should fail because the 'slug' matches previous org",
        },
    )
    assert response.status_code == 409


async def test_get_org(auth_client):
    response = await auth_client.post(
        "/org",
        json={
            "name": "test_get_org",
            "slug": "test_get_org_slug",
            "desc": "this should be a successful org creation",
        },
    )
    assert response.status_code == 200, response.json()

    # calls to get the org object
    org_response = await auth_client.get(f"/org/{response.json()['id']}")
    assert org_response.status_code == 200, org_response.json()
    body = org_response.json()

    assert body["id"] == response.json()["id"]
    assert body["name"] == "test_get_org"
    assert body["slug"] == "test_get_org_slug"
    assert body["desc"] == "this should be a successful org creation"


async def test_org_not_found(auth_client):
    response = await auth_client.get(f"/org/{uuid.uuid4()}")
    assert response.status_code == 403


async def test_update_org(auth_client):
    response = await auth_client.post(
        "/org",
        json={
            "name": "test_update_org",
            "slug": "test_update_org_slug",
            "desc": "this should be a successful org creation",
        },
    )
    org = await auth_client.patch(
        f"/org/{response.json()['id']}",
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
        "/org",
        json={
            "name": "test_delete_org",
            "slug": "test_delete_org_slug",
            "desc": "this should be a successful org creation",
        },
    )
    deletion = await auth_client.delete(f'/org/{response.json()["id"]}')
    print(deletion.status_code, deletion.text)
    assert deletion.status_code == 200

