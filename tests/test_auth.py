from fastapi.testclient import TestClient
from src.main import app

client=TestClient(app)


def test_register():
    response=client.post("auth/register",json={"email":"xx@gmail.com","role":"employee","password":"pass1234"})
    assert response.status_code==200
    assert response.json()["msg"] == "New User Registered Successfully"

def test_login():
    response=client.post("auth/login",json={"email":"xx@gmail.com","password":"pass1234"})
    assert response.status_code==200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"