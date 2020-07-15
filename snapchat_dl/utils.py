"""Utility functions for snapchat_dl."""
import os
import re
from argparse import Namespace
from datetime import datetime

from loguru import logger


class NoStoriesAvailable(Exception):
    """Exception when there are no stories."""

    pass


def strf_time(timestamp, format_str):
    """Format unix timestamp to custom format.

    Args:
        timestamp (int): unix timestamp
        format_str (str): valid python date time format

    Returns:
        str: timestamp formatted to custom format.
    """
    return datetime.utcfromtimestamp(timestamp).strftime(format_str)


def valid_username(username):
    """Validate Username.

    Args:
        username (str): Snapchat Username

    Returns:
        bool: True if username is valid.
    """
    match = re.match(r"(?P<username>^[\w\.\_]{3,}$)", username)
    if match is None:
        return False

    return match and match.groupdict()["username"] == username


def search_usernames(string: str) -> list:
    """Return list of usernames found in a string.

    Args:
        string (str): string to search for usernames

    Returns:
        list: usernames found in string
    """
    return [
        username
        for username in re.findall(
            r"https://story.snapchat.com/s/([\w_\.]{3,})", string
        )
        if valid_username(username)
    ]


def use_batch_file(args: Namespace) -> list:
    """Return list of usernames from file args.batch_file.

    Args:
        args (Namespace): argparse Namespace

    Raises:
        os.error: raises if batch_file not found

    Returns:
        list: usernames read from batch_file
    """
    usernames = list()
    if args.batch_file is not None:
        if os.path.isfile(args.batch_file) is False:
            raise Exception(
                logger.error("Invalid Batch File at {}".format(args.batch_file))
            )

        with open(args.batch_file, "r") as f:
            for u in f.read().split("\n"):
                username = u.strip()
                if valid_username(username) and username not in usernames:
                    usernames.append(username)

    return usernames


def use_prefix_dir(args: Namespace):
    """Return dirnames as username from file args.scan_prefix.

    Args:
        args (Namespace): argparse Namespace

    Returns:
        list: usernames read from scan_prefix
    """
    usernames = list()
    if args.scan_prefix:
        for username in [
            o
            for o in os.listdir(args.save_prefix)
            if os.path.isdir(os.path.join(args.save_prefix, o))
        ]:
            if username not in usernames and valid_username(username):
                usernames.append(username)

        if args.quiet is False:
            logger.info(
                "Added {} usernames from {}".format(len(usernames), args.save_prefix)
            )

    return usernames
