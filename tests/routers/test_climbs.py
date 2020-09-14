from fastapi import status

from cotacol.security import generate_access_token


def test_geojson(client, climb):
    response = client.get("/v1/climbs/cotacol.geojson")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers.get("content-type") == "application/geo+json"


def test_list_climbs(client, climb):
    response = client.get("/v1/climbs/")
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1
    assert data[0]["id"] == climb.id


def test_get_climb(client, climb):
    response = client.get(f"/v1/climbs/{climb.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == climb.id


def test_get_climb_no_cotacol(client):
    response = client.get("/v1/climbs/1001/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_climb(client, climb, staff_user):
    access_token, _, _ = generate_access_token(staff_user)
    response = client.patch(
        f"/v1/climbs/{climb.id}/", json={"name": "Kop"}, headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == climb.id
    assert data["name"] == "Kop"


def test_update_climb_unauthorized(client, climb):
    response = client.patch(f"/v1/climbs/{climb.id}/", json={"name": "Kop"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
