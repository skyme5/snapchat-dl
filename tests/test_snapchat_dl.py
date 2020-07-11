#!/usr/bin/env python
"""Tests for `snapchat_dl` package."""
import json
import os
import shutil
import unittest
from unittest import mock

from requests.exceptions import HTTPError

from snapchat_dl.snapchat_dl import NoStoriesAvailable
from snapchat_dl.snapchat_dl import SnapchatDL


class TestSnapchat_dl(unittest.TestCase):
    """Tests for `snapchat_dl` package."""

    def setUp(self):
        """Set up test fixtures."""
        self.snapchat_dl = SnapchatDL(limit_story=10)
        self.test_url = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"
        self.test_url404 = "https://google.com/error.html"
        self.username = "invalidusername"

    def tearDown(self):
        """Tear down test fixtures."""
        if os.path.isdir(self.username):
            shutil.rmtree(self.username)

    @classmethod
    def tearDownClass(cls):
        """Tear down test fixtures."""
        for file in ["23.mp4", "23.txt"]:
            if os.path.isfile(file):
                os.remove(file)

    def test_class_init(self):
        """Test snapchat_dl init."""
        self.assertTrue(self.snapchat_dl)

    def test_valid_username(self):
        """Test snapchat_dl Download with invalid username."""
        with self.assertRaises(Exception):
            self.snapchat_dl.download("2323 2323")

    def test_media_type(self):
        """Test snapchat_dl media_type."""
        self.assertEqual(self.snapchat_dl.media_type("IMAGE"), ".jpg")
        self.assertEqual(self.snapchat_dl.media_type("VIDEO"), ".mp4")
        self.assertEqual(self.snapchat_dl.media_type("VIDEO_NO_SOUND"), ".mp4")

    def test_strf_time(self):
        """Test snapchat_dl strf_time."""
        self.assertEqual(
            self.snapchat_dl.strf_time(978307200, "%Y-%m-%dT%H-%M-%S"),
            "2001-01-01T00-00-00",
        )

    def test_download_without_args(self):
        """Test snapchat_dl Download without args."""
        with self.assertRaises(Exception):
            self.snapchat_dl.download()

    def test_download_url(self):
        """Test snapchat_dl download_url."""
        open("23.mp4", "a").close()
        self.snapchat_dl.download_url(self.test_url, "23.mp4")

    def test_download_url_exists(self):
        """Test snapchat_dl download_url with invalid url."""
        with self.assertRaises(FileExistsError):
            self.snapchat_dl.download_url(self.test_url, "23.mp4")

    def test_download_url_raise(self):
        """Test snapchat_dl download_url with invalid url."""
        with self.assertRaises(HTTPError):
            self.snapchat_dl.download_url(self.test_url404, "23.txt")

    def test_get_stories_err(self):
        """Test snapchat_dl Download."""
        with self.assertRaises(NoStoriesAvailable):
            self.snapchat_dl.get_stories(self.username)

    def test_get_stories_no_stories(self):
        """Test snapchat_dl Stories are not available."""
        self.assertFalse(self.snapchat_dl.download("username"))

    @mock.patch("snapchat_dl.snapchat_dl.SnapchatDL.get_stories")
    def test_get_stories_ok(self, fake_get):
        """Test snapchat_dl Download."""
        with open("tests/mock_data/invalidusername.json", "r", encoding="utf8") as f:
            data = json.load(f)

        fake_get.return_value = data
        self.snapchat_dl.download(self.username)


if __name__ == "__main__":
    unittest.main()
