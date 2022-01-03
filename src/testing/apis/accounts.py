from fastapi.testclient import TestClient

from app import app

client = TestClient(app=app)

data = {
    "name": "string13",
    "last_name": "string13",
    "anonymous_name": "string123",
    "email": "1712.01021@manas.edu.kg",
    "password": "string123"
}


def test_register():
    response = client.post('/auth/sign-up', json=data, )
    assert response.status_code == 200


data1 = {
    "email": "1712.01021@manas.edu.kg",
    "code": 615945
}


def activate_user():
    response = client.post('/auth/verified-account', json=data2,)
    assert response.status_code == 200


data2 = {
    "email": "1712.01021@manas.edu.kg",
    "password": "string123"
}


def test_login():
    response = client.post('/auth/sign-in', json=data2,)
    assert response.status_code == 200
