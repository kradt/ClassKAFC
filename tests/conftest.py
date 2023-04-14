import pytest

from kafc import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def login(client):
    login = "test"
    password = "A9090997a"

    with client:
        response = client.post("/auth/login",
                               data={"login": login, "password": password},
                               follow_redirects=True)
        yield response
    with client:
        client.post("/auth/logout")