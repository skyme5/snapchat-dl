#!/usr/bin/env python
"""Tests for `snapchat_dl` package."""
import unittest
from argparse import Namespace

from snapchat_dl.utils import search_usernames
from snapchat_dl.utils import strf_time
from snapchat_dl.utils import use_batch_file
from snapchat_dl.utils import use_prefix_dir
from snapchat_dl.utils import valid_username


class Test_utils(unittest.TestCase):
    """Tests for `snapchat_dl` package."""

    def test_valid_username(self):
        """Test for invalid username."""
        self.assertFalse(valid_username("2323 2323"))

    def test_strf_time(self):
        """Test strf_time."""
        self.assertEqual(
            strf_time(978307200, "%Y-%m-%dT%H-%M-%S"),
            "2001-01-01T00-00-00",
        )

    def test_search_usernames(self):
        """Test usernames search in string."""
        string = """
            https://story.snapchat.com/s/in#invalidusername
            https://story.snapchat.com/s/username1
            https://story.snapchat.com/s/user.name2
            https://story.snapchat.com/s/user_name
            https://story.snapchat.com/@user_name
        """
        usernames = ["user.name2", "user_name", "username1"]
        self.assertListEqual(search_usernames(string), usernames)

    def test_use_batch_file(self):
        args = Namespace(batch_file="tests/mock_data/batch_file.txt")
        usernames = ["username1", "user.name2", "user_name"]
        self.assertListEqual(use_batch_file(args), usernames)

    def test_use_batch_file_err(self):
        args = Namespace(batch_file="tests/mock_data/batch_file_err.txt")
        with self.assertRaises(Exception):
            use_batch_file(args)

    def test_use_prefix_dir(self):
        args = Namespace(scan_prefix=True, save_prefix="tests/mock_data", quiet=False)
        usernames = ["user.1name", "user1"]
        self.assertListEqual(use_prefix_dir(args), usernames)
