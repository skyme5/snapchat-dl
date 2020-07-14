"""Tests for `snapchat_dl` package."""
import os
import unittest

from requests.exceptions import HTTPError

from snapchat_dl.downloader import download_url


class Test_downloader(unittest.TestCase):
    """Tests for `snapchat_dl.downloader.download_url` package."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_url = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"
        self.test_url404 = "https://google.com/error.html"
        self.username = "invalidusername"

    @classmethod
    def tearDownClass(cls):
        """Tear down test fixtures."""
        for file in ["test_dl_23.mp4", "test_dl_23.txt"]:
            if os.path.isfile(file):
                os.remove(file)

    def test_download_url(self):
        """Test snapchat_dl download_url."""
        open("test_dl_23.mp4", "a").close
        download_url(self.test_url, "test_dl_23.mp4")

    def test_download_url_file_exists(self):
        """Test snapchat_dl download_url with file downloaded."""
        with self.assertRaises(FileExistsError):
            download_url(self.test_url, "test_dl_23.mp4")

    def test_download_url_raise(self):
        """Test snapchat_dl download_url with invalid url."""
        with self.assertRaises(HTTPError):
            download_url(self.test_url404, "test_dl_23.txt")
