import unittest
from mbuster import app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_routes_index(self):
        response = self.app.get("/index", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    