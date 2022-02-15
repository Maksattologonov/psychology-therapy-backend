import ast

import requests
import json
from fastapi.testclient import TestClient
from app import app as web_app
from unittest import TestCase
from ..test_db import get_session, override_get_db


class APITestForum(TestCase):
    def setUp(self) -> None:
        web_app.dependency_overrides[get_session] = override_get_db
        self.client = requests
        self.url = "http://127.0.0.1:8000/"
        self.payload = 'username=1712.02111@manas.edu.kg&password=strinasdasg'

    def test_auth(self):
        response = self.client.post(url=self.url + "auth/sign-in", data=self.payload, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        self.assertEqual(response.status_code, 200)
        token = response.content.decode('utf-8')
        return ast.literal_eval(token)

    def test_forum_create(self):
        data = {
            "title": "string",
            "description": "string",
            "is_anonymous": "true"
        }
        token = self.test_auth()
        response = self.client.post(self.url + "forum/create-forum/", json=data,
                                    headers={"Authorization": "Bearer " + token['access_token']})
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(201, response.status_code)
        self.assertEqual(type(data), type(content))
        self.assertEqual(len(data), len(content))

    def test_upload_files(self):
        with open('images/test_images/Screenshot from 2021-11-09 17-38-05.png') as img:
            token = self.test_auth()
            response = self.client.post(self.url + "forum/upload-image/", data={'image': img, 'forum_id': 1},
                                        headers={"Authorization": "Bearer " + token['access_token']})
            print(response.content)
