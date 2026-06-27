import uuid


async def test_collection_routes_redirect_trailing_slash(auth_client):
    org = await auth_client.post(
        "/orgs",
        json={
            "name": "test_collection_routes_redirect_trailing_slash",
            "slug": f"test_collection_routes_redirect_trailing_slash_{uuid.uuid4().hex}",
            "desc": "this should be a successful org creation",
        },
    )
    assert org.status_code == 200, org.json()
    team = await auth_client.post(
        f"/orgs/{org.json()['id']}/teams",
        json={
            "name": "test_collection_routes_redirect_trailing_slash_team",
            "slug": f"test_collection_routes_redirect_trailing_slash_team_{uuid.uuid4().hex}",
            "desc": "this should be a successful team creation",
        },
    )
    assert team.status_code == 200, team.json()
    project = await auth_client.post(
        f"/orgs/{org.json()['id']}/teams/{team.json()['id']}/projects",
        json={
            "name": "test_collection_routes_redirect_trailing_slash_project",
            "desc": "this should be a successful project creation",
            "team_id": team.json()["id"],
        },
    )
    assert project.status_code == 200, project.json()

    urls = [
        "/orgs/",
        f"/orgs/{org.json()['id']}/teams/",
        f"/orgs/{org.json()['id']}/teams/{team.json()['id']}/projects/",
        f"/orgs/{org.json()['id']}/teams/{team.json()['id']}/projects/{project.json()['id']}/tasks/",
        f"/orgs/{org.json()['id']}/teams/{team.json()['id']}/projects/{project.json()['id']}/labels/",
        f"/orgs/{org.json()['id']}/teams/{team.json()['id']}/projects/{project.json()['id']}/milestones/",
    ]

    for url in urls:
        response = await auth_client.get(url)
        assert response.status_code == 307
