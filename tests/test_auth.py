from kafc.database import models


def test_register_user(client):
    login = "test"
    password = "A9090997a"

    with client:
        response = client.post("/auth/sign-up",
                               data={"login": login, "password": password, "repeat_password": password},
                               follow_redirects=True)
        user = models.User.query.filter_by(username=login).first()
    assert user is not None
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


def test_user_login(login):
    assert login.request.path == "/me/"
    assert login.status_code == 200


def test_cabinet_home_page_without_login(client):
    with client:
        response = client.get("/me", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data


def test_cabinet_page_with_login(client, login):
    response = client.get("/me", follow_redirects=True)
    assert response.status_code == 200
    assert bytes("Введіть Ім'я яке студенти будуть бачити при відправленні завдання", "utf-8") in response.data

def test_send_task_with_login(client, login, lesson):
    response = client.post("/me/send-task",
                           data={"title": "Hello world",
                                 "description": "Bye world",
                                 "group": "351", "lesson": lesson},
                           follow_redirects=True)

    print(response)
    assert response.request.full_path == "/me/?from_task=True"
    assert response.status_code == 200