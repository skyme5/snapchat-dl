"""The Main Snapchat Downloader Class."""
import concurrent.futures
import os
import re

import requests
from loguru import logger

from snapchat_dl.downloader import download_url
from snapchat_dl.utils import NoStoriesAvailable
from snapchat_dl.utils import strf_time


class SnapchatDL:
    """Interact with Snapchat API to download story."""

    def __init__(
        self,
        directory_prefix=".",
        max_workers=2,
        limit_story=-1,
        sleep_interval=1,
        quiet=False,
    ):
        self.directory_prefix = os.path.abspath(os.path.normpath(directory_prefix))
        self.max_workers = max_workers
        self.limit_story = limit_story
        self.sleep_interval = sleep_interval
        self.quiet = quiet
        self.endpoint = "https://search.snapchat.com/lookupStory?id={}"
        self.reaponse_ok = requests.codes.get("ok")

    def _api_fetch_story(self, username):
        """Download user stories.

        Args:
            username (str): Snapchat `username`

        Returns: (requests.Response): response
        """
        api_url = self.endpoint.format(username)
        response = requests.get(api_url)

        return response

    def download(self, username):
        """Download Snapchat Story for `username`.

        Args:
            username (str): Snapchat `username`

        Returns:
            [bool]: story downloader
        """
        response = self._api_fetch_story(username)
        if response.status_code != 200:
            if self.quiet is False:
                logger.info("\033[91m{} has no stories\033[0m".format(username))
            raise NoStoriesAvailable

        stories = response.json().get("snapList")
        if self.limit_story > -1:
            stories = stories[0 : self.limit_story]

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers)
        try:
            for media in stories:
                snap_id = media["snapId"]
                media_url = media["snapUrls"]["mediaUrl"]
                overlay_url = media["snapUrls"]["overlayUrl"]
                timestamp = int(media["timestampInSec"])
                date_str = strf_time(timestamp, "%Y-%m-%d")

                dir_name = os.path.join(self.directory_prefix, username, date_str)

                filename = strf_time(timestamp, "%Y-%m-%d_%H-%M-%S {} {}").format(
                    snap_id, username
                )

                media_output = os.path.join(dir_name, filename)
                executor.submit(
                    download_url, media_url, media_output, self.sleep_interval
                )

                if len(overlay_url) > 0:
                    overlay_output = os.path.join(dir_name, filename + "_ol")
                    executor.submit(
                        download_url, overlay_url, overlay_output, self.sleep_interval
                    )

        except KeyboardInterrupt:
            executor.shutdown(wait=False)

        logger.info("[+] {} has {} stories".format(username, len(stories)))
