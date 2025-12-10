import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config.update({"TESTING": True, "WTF_CSRF_ENABLED": False})
    with app.test_client() as client:
        yield client


def test_main_resume_page(client):
    resp = client.get("/resume")
    assert resp.status_code == 200
    assert "Ігор Бабійчук" in resp.get_data(as_text=True)


def test_users_login_get(client):
    resp = client.get("/users/login")
    assert resp.status_code == 200


def test_login_and_profile_redirect(client):
    # Wrong credentials -> back to login with flash
    resp = client.post("/users/login", data={"username": "bad", "password": "bad"}, follow_redirects=True)
    assert resp.status_code == 200

    # Correct credentials -> profile
    resp = client.post(
        "/users/login",
        data={"username": "admin", "password": "admin123"},
        follow_redirects=True,
    )
    body = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert "Профіль користувача" in body
