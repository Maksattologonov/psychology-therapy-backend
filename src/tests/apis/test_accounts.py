import os

from fastapi.testclient import TestClient
from app import app as web_app
from unittest import TestCase
from ..test_db import get_session, override_get_db


class APITestCase(TestCase):
    def setUp(self) -> None:
        web_app.dependency_overrides[get_session] = override_get_db
        self.client = TestClient(web_app)
        self.data = {
            "name": "striasdange",
            "last_name": "stasdasringe",
            "anonymous_name": "strinsadge",
            "email": "1712.02111@manas.edu.kg",
            "password": "strinasdasg"
        }

    def test_register(self):
        response = self.client.post('/auth/sign-up', json=self.data)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post('/auth/sign-in', json=self.data)
        self.assertEqual(response.status_code, 200)
        print(response.content)
        return response.content

    # def test_user(self):
    #     access_token = self.test_login()
    #     print(type(access_token))
    #     response = self.client.get('/auth/user', json=self.data,
    #                                headers={'Authorization': 'Bearer ' + str(access_token)})
    #     self.assertEqual(response.status_code, 200)

    def delete_db(self):
        os.remove('./test.db')
