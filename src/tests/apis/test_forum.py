import ast

import requests
import json
import pytest
from fastapi.testclient import TestClient
from app import app as web_app
from unittest import TestCase
from core.database import get_session, Base
from models.accounts import User, VerificationCode
from tests.test_db import override_get_db, engine, TestingSessionLocal

web_app.dependency_overrides[get_session] = override_get_db
client = TestClient(web_app)

conn = TestingSessionLocal()
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


class APITestForum(TestCase):
    def setUp(self) -> None:
        self.client = client
        self.data = {
            "name": "Test1",
            "last_name": "Test1",
            "anonymous_name": "Test1",
            "email": "1812.01011@manas.edu.kg",
            "password": "test12345"
        }
        response = self.client.post('/auth/sign-up', json=self.data)
        user = conn.query(User).filter_by(id=1).first()
        user.is_active = 1
        conn.commit()
        login = self.client.post('/auth/sign-in',
                                 data={"username": "1812.01011@manas.edu.kg",
                                       "password": "test12345"},
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
        self.token = "Bearer " + json.loads(login.content.decode('utf-8')).get('access_token')

    # def test_auth(self):
    #     response = self.client.post(url=self.url + "auth/sign-in", data=self.payload, headers={
    #         'Content-Type': 'application/x-www-form-urlencoded'
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     token = response.content.decode('utf-8')
    #     return ast.literal_eval(token)

    def test_forum_create(self):
        data = {
            "title": "string",
            "description": "string",
        }
        token = self.token
        response = self.client.post("catalog/forum/create/", data={
            'image': ('test.png', open('images/test_images/test.png'), 'rb', "image/jpeg")}, params=data,
                                    headers={"Authorization": token, "Content-Type": "multipart/form-data"})
        # content = json.loads(response.content.decode('utf-8'))
        print(response.content)
        self.assertEqual(201, response.status_code)
        # self.assertEqual(type(data), type(content))
        # self.assertEqual(len(data), len(content))

    # def test_upload_files(self):
    #     data = b'{"detail":[{"loc":["query","forum_id"],"msg":"field required","type":"value_error.missing"},' \
    #            b'{"loc":["body","image"],"msg":"Expected UploadFile, received: <class \'str\'>","type":"value_error"}]}'
    #
    #     with open('images/test_images/test.png', 'rb') as img:
    #         token = self.token
    #         response = self.client.post("forum/upload-image/", data={'image': img, 'forum_id': 1},
    #                                     headers={"Authorization": "Bearer " + token})
    #         self.assertEqual(data, response.content)
    #         # print(query)
    #         # # self.assertEqual(200, response.status_code)
