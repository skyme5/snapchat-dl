#!/usr/bin/env python
"""Tests for `snapchat_dl` package."""
import json
import os
import shutil
import unittest
from unittest import mock

from snapchat_dl.snapchat_dl import SnapchatDL
from snapchat_dl.utils import NoStoriesAvailable


def teardown_module(module):
    os.system("rm -rf .test-data")


class TestSnapchat_dl(unittest.TestCase):
    """Tests for `snapchat_dl` package."""

    def setUp(self):
        """Set up test fixtures."""
        self.snapchat_dl = SnapchatDL(
            limit_story=10, quiet=True, directory_prefix=".test-data", dump_json=True,
        )
        self.test_url = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"
        self.test_url404 = "https://google.com/error.html"
        self.username = "invalidusername"

    def test_class_init(self):
        """Test snapchat_dl init."""
        self.assertTrue(self.snapchat_dl)

    def test_get_stories_no_stories(self):
        """Test snapchat_dl Stories are not available."""
        with self.assertRaises(NoStoriesAvailable):
            self.snapchat_dl.download("username")

    @mock.patch("snapchat_dl.snapchat_dl.SnapchatDL._api_fetch_story")
    def test_get_stories_ok(self, fake_get):
        """Test snapchat_dl Download."""

        class Mock_Response:
            status_code = 200

            def json(self) -> dict:
                with open(
                    "tests/mock_data/invalidusername.json", "r", encoding="utf8"
                ) as f:
                    return json.load(f)

        fake_get.return_value = Mock_Response()
        self.snapchat_dl.download(self.username)
