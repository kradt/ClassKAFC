import pytest

from kafc import create_app
from kafc.database import db, models


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    })
    app.config["CELERY"].update({
        'task_always_eager': True
    })

    yield app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="session")
def user() -> dict:
    return {"login": "test", "password": "A9090997a"}


@pytest.fixture(scope="module")
def register(client, user):
    with client:
        response = client.post("/auth/sign-up",
                               data={"login": user["login"], "password": user["password"], "repeat_password": user["password"]},
                               follow_redirects=True)
    
    yield response

    with client.application.app_context():
        usr = db.session.query(models.User).filter_by(username=user["login"]).first()
        usr.lessons = []
        db.session.delete(usr)
        db.session.commit()


@pytest.fixture(scope="module")
def login(client, register, user):
    with client:
        response = client.post("/auth/login",
                               data={"login": user["login"], "password": user["password"]},
                               follow_redirects=True)
    yield response
    with client:
        client.get("/auth/logout")


@pytest.fixture(scope="function")
def lesson(client, login):
    lesson = "math"
    client.post("/me/update_user", data={"lesson": lesson})
    yield lesson
    client.post("/me/remove-lesson", data={"lesson": lesson})
