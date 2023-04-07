from kafc.database import models


def test_request_example(client):
    response = client.get("/me", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data



