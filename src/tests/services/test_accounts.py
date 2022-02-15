from unittest import TestCase

from starlette.testclient import TestClient
from services.accounts import *
from app import app as web_app
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

    def test_generate_code(self):
        self.assertEqual(SendMessageWhenCreateUser.generate_code(), 100000)
