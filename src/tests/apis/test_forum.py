import ast

import requests
import json
from app import app as web_app
from unittest import TestCase
from fastapi.testclient import TestClient
from core.database import get_session, Session, Base
from models.forum import Forum
from ..test_db import override_get_db, TestingSessionLocal, engine

web_app.dependency_overrides[get_session] = override_get_db
client = TestClient(web_app)

conn = TestingSessionLocal()
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


class APITestForum(TestCase):
    def setUp(self) -> None:
        self.client = requests
        self.url = "http://127.0.0.1:8000/"
        self.payload = 'username=1712.02111@manas.edu.kg&password=strinasdasg'
        self.forum_query = Forum(title='test title', description='test description', is_anonymous=True)
        self.create_forum = conn.add(self.forum_query)
        self.create_forum.commit()
        print(self.create_forum)

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
        data = b'{"detail":[{"loc":["query","forum_id"],"msg":"field required","type":"value_error.missing"},' \
               b'{"loc":["body","image"],"msg":"Expected UploadFile, received: <class \'str\'>","type":"value_error"}]}'

        with open('images/test_images/Screenshot from 2021-11-09 17-38-05.png', 'rb') as img:
            token = self.test_auth()
            response = self.client.post(self.url + "forum/upload-image/", data={'image': img, 'forum_id': 1},
                                        headers={"Authorization": "Bearer " + token['access_token']})
            self.assertEqual(data, response.content)
            # print(query)
            # # self.assertEqual(200, response.status_code)
