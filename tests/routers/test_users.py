from fastapi import status

from cotacol.security import generate_access_token


def test_get_user(client, staff_user):
    access_token, _, _ = generate_access_token(staff_user)
    response = client.get("/v1/users/me/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "staff"


def test_update_user(client, staff_user):
    access_token, _, _ = generate_access_token(staff_user)
    response = client.patch(
        "/v1/users/me/", json={"bookmarks": [34, 35]}, headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["bookmarks"] == [34, 35]
