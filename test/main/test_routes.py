import unittest

import requests_mock

from app import create_app


class MainBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test").test_client()
        self.domain = "http://localhost"

    def test_healthcheck_live(self):
        rv = self.app.get("/healthcheck/live/")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("ok", rv.text)

    def test_trailing_slash_redirects(self):
        rv = self.app.get("/healthcheck/live")
        self.assertEqual(rv.status_code, 308)
        self.assertEqual(rv.location, f"{self.domain}/healthcheck/live/")

    def test_homepage(self):
        rv = self.app.get("/request-a-service-record/")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(
            '<h1 class="tna-heading-xl">Request a Service Record</h1>', rv.text
        )
