"""Tests for `snapchat_dl` package."""
import os
import shutil
import unittest

from requests.exceptions import HTTPError

from snapchat_dl.downloader import download_url


def teardown_module(module):
    shutil.rmtree(".test-data")


class Test_downloader(unittest.TestCase):
    """Tests for `snapchat_dl.downloader.download_url` package."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_url = "https://filesamples.com/samples/video/mp4/sample_640x360.mp4"
        self.test_url404 = "https://google.com/error.html"

    def test_download_url(self):
        """Test snapchat_dl download_url."""
        download_url(self.test_url, ".test-data/test_dl_23.mp4", sleep_interval=0)

    def test_empty_download(self):
        """Test snapchat_dl download_url."""
        open(".test-data/test_dl_23.mp4", "w").close()
        download_url(self.test_url, ".test-data/test_dl_23.mp4", sleep_interval=0)

    def test_download_url_raise(self):
        """Test snapchat_dl download_url with invalid url."""
        with self.assertRaises(HTTPError):
            download_url(
                self.test_url404, ".test-data/test_dl_23.mp4", sleep_interval=0
            )
