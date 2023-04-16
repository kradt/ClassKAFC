
def test_cabinet_home_page_without_login(client):
    with client:
        response = client.get("/me", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data


def test_cabinet_page_with_login(client, login):
    response = client.get("/me", follow_redirects=True)
    assert response.status_code == 200
    assert bytes("Введіть Ім'я яке студенти будуть бачити при відправленні завдання", "utf-8") in response.data


def test_send_task_with_login(app, client, login, lesson):

    response = client.post("/me/send-task",
                           data={"title": "Hello world",
                                 "description": "Bye world",
                                 "group": "351", "lesson": lesson},
                           follow_redirects=True)

    print(response)
    assert response.request.full_path == "/me/?from_task=True"
    assert response.status_code == 200


def test_update_user_information(client, login):
    name = "Alex"
    lesson = "OOP"
    response = client.post("/me/update_user", data={"name": name, "lesson": lesson}, follow_redirects=True)
    from flask_login import current_user
    with client.application.app_context():
        assert current_user.name == name
        assert lesson in [i.name for i in current_user.lessons]
    assert response.status_code == 200
    assert bytes(name, "utf-8") in response.data
    assert bytes(lesson, "utf-8") in response.data
