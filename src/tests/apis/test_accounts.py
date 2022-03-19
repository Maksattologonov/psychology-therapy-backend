import ast
import json
import os
import time

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


class APITestCase(TestCase):
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

    def test_message_to_email(self):
        response = self.client.post('/auth/send-email', json={"email": "1812.01011@manas.edu.kg",
                                                              "name": "Test",
                                                              "last_name": "Test"
                                                              })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'"Message sent successfully"')

    def test_login(self):
        response = self.client.post('/auth/sign-in',
                                    data={"username": "1812.01011@manas.edu.kg",
                                          "password": "test12345"},
                                    headers={"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(response.status_code, 200)

    def test_user(self):
        response = self.client.get('auth/user',
                                   headers={"Authorization": self.token,
                                            "accept": "application/json"})
        self.assertEqual(200, response.status_code)
