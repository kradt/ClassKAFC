from kafc.database import models


def test_request_example(client):
    response = client.get("/me", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data


def test_registration(client, app):
    response = client.post(
        "/auth/sign-up",
        data={"login": "test@test.com", "password": "A9090997a", "repeat_password": "A9090997a"},
        follow_redirects=True)

    print(response)
    assert response.status_code == 200
    with app.app_context():
        assert models.User.query.count() == 1
        assert models.User.query.first().username == "test@test.com"
