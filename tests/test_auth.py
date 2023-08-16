from kafc.database import db, models


def test_register_user(client, user):
    with client:
        response = client.post("/auth/sign-up",
                               data={"login": user["login"], "password": user["password"], "repeat_password": user["password"]},
                               follow_redirects=True)
    with client.application.app_context():
        db_user = db.session.query(models.User).filter_by(username=user["login"]).first()
    assert db_user is not None
    assert db_user.username == user["login"]
    assert response.status_code == 200


def test_user_already_exist(client, register, user):
    with client:
        response = client.post("/auth/sign-up",
                               data={"login": user["login"], "password": user["password"], "repeat_password": user["password"]},
                               follow_redirects=True)
    assert bytes("Користувач з таким username уже існує", "utf-8") in response.data
    assert response.status_code == 200


def test_user_login(login):
    assert login.request.path == "/me/"
    assert login.status_code == 200
