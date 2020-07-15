"""Console script for snapchat_dl."""
import argparse
import os
import sys


def parse_arguments():
    """Console script for snapchat_dl."""
    parser = argparse.ArgumentParser(prog="snapchat-dl")

    parser.add_argument(
        "username",
        action="store",
        nargs="*",
        help="Atleast one or more usernames to download stories for.",
    )

    any_one_group = parser.add_mutually_exclusive_group()
    any_one_group.add_argument(
        "-c",
        "--scan-clipboard",
        action="store_true",
        help="Scan clipboard for story links"
        " with the format of 'https://story.snapchat.com/s/<username>'",
        dest="scan_clipboard",
    )

    any_one_group.add_argument(
        "-u",
        "--check-for-update",
        action="store_true",
        help="Periodically check for new stories.",
        dest="check_update",
    )

    parser.add_argument(
        "-i",
        "--batch-file",
        action="store",
        default=None,
        help="Read usernames from file",
        metavar="BATCH_FILENAME",
        dest="batch_file",
    )

    parser.add_argument(
        "-P",
        "--directory-prefix",
        action="store",
        default=os.path.abspath(os.getcwd()),
        help="Directory Prefix for downloading stories",
        metavar="DIRECTORY_PREFIX",
        dest="save_prefix",
    )

    parser.add_argument(
        "-s",
        "--scan-from-prefix",
        action="store_true",
        help="Scan usernames (as directory name) from prefix directory.",
        dest="scan_prefix",
    )

    parser.add_argument(
        "-l",
        "--limit-story-count",
        action="store",
        default=-1,
        help="Set maximum number of stories to download.",
        metavar="NUM_STORY",
        dest="limit_story",
        type=int,
    )

    parser.add_argument(
        "-j",
        "--max-concurrent-downloads",
        action="store",
        default=2,
        help="Set maximum number of parallel downloads.",
        metavar="MAX_WORKERS",
        dest="max_workers",
        type=int,
    )

    parser.add_argument(
        "-t",
        "--update-interval",
        action="store",
        default=60 * 10,
        help="Set the update interval for new story in seconds. (Default: 10m)",
        metavar="INTERVAL",
        dest="interval",
        type=int,
    )

    parser.add_argument(
        "--sleep-interval",
        action="store",
        default=1,
        help="Sleep between downloads in seconds. (Default: 1s)",
        metavar="INTERVAL",
        dest="sleep_interval",
        type=int,
    )

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Do not print anything to the console. (errors are still logged)",
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()
