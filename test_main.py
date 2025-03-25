# test_main.py
import pytest
from main import app


@pytest.fixture
def client():
    """
    Pytest fixture that creates a Flask test client from the 'app' in main.py.
    """
    with app.test_client() as client:
        yield client


def test_root_endpoint(client):
    """
    Test the GET '/' endpoint to ensure it returns
    the greeting and a 200 status code.
    """
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hello from my Password Validator!" in resp.data


# Not that this test only makes sense for the starter code,
# in practice we would not test for a 501 status code!

def test_check_password_validation(client):
    resp = client.post("/v1/checkPassword", json={"password": "whatever"})
    assert resp.status_code == 200
    data = resp.get_json()
    expected_errors = [
        "Password must contain at least 2 uppercase letters.",
        "Password must contain at least 2 digits.",
        "Password must contain at least 1 special character (!@#$%^&*)."
    ]
    for error in expected_errors:
        assert error in data.get("reason")
    assert data.get("valid") is False

def test_check_password_no_upper(client):
    resp = client.post("/v1/checkPassword", json={"password": "abcd12!@"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["valid"] is False
    assert "Password must contain at least 2 uppercase letters." in data["reason"]
  
def test_missing_password_field(client):
    resp = client.post("/v1/checkPassword", json={})
    data = resp.get_json()
    assert resp.status_code == 200
    assert "Password must be at least 8 characters long." in data["reason"]

def test_invalid_password_missing_special_char(client):
    password = "ABcd1234"
    resp = client.post("/v1/checkPassword", json={"password": password})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["valid"] is False
    assert "Password must contain at least 1 special character (!@#$%^&*)." in data["reason"]


