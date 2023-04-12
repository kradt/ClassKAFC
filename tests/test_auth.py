from kafc.database import models


def test_request_example(client):
    response = client.get("/me", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data

def test_register_user(client):
    login = "test"
    password = "A9090997a"

    with client:
        response = client.post("/auth/sign-up",
                               data={"login": login, "password": password, "repeat_password": password},
                               follow_redirects=True)
        user = models.User.query.filter_by(username=login).first()
    assert user != None
    assert user.username == login
    assert response.status_code == 200


def test_user_already_exist(client):
    login = "test"
    password = "A9090997a"

    with client:
        response = client.post("/auth/sign-up",
                               data={"login": login, "password": password, "repeat_password": password},
                               follow_redirects=True)
    assert bytes("Користувач з таким username уже існує", "utf-8") in response.data
    assert response.status_code == 200



