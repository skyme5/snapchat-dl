"""The Main Snapchat Downloader Class."""
import concurrent.futures
import os

import requests
from loguru import logger

from snapchat_dl.downloader import download_url
from snapchat_dl.utils import NoStoriesAvailable
from snapchat_dl.utils import strf_time


class SnapchatDL:
    def __init__(
        self, directory_prefix=".", max_workers=2, limit_story=-1, quiet=False,
    ):
        self.directory_prefix = os.path.abspath(os.path.normpath(directory_prefix))
        self.max_workers = max_workers
        self.limit_story = limit_story
        self.quiet = quiet
        self.endpoint = "https://storysharing.snapchat.com/v1/fetch/{}"
        "?request_origin=ORIGIN_WEB_PLAYER"
        self.reaponse_ok = requests.codes.get("ok")

    def stories_response(self, username):
        """Download user stories.

        Args:
            username (str): Snapchat `username`

        Returns: (requests.Response): response
        """
        api_url = self.endpoint.format(username)
        response = requests.get(api_url)

        return response

    def media_type(self, media_type):
        """Return file extension for Media Type.

        Args:
            media_type (str): Snapchat Snap Media Type

        Returns:
            str: File Extension for `media_type`, one of the
                 `IMAGE`, `VIDEO`, `VIDEO_NO_SOUND`
        """
        if media_type == "IMAGE":
            return ".jpg"
        if media_type == "VIDEO":
            return ".mp4"
        if media_type == "VIDEO_NO_SOUND":
            return ".mp4"

    def download(self, username):
        """Download Snapchat Story for `username`.

        Args:
            username (str): Snapchat `username`

        Returns:
            [bool]: story downloader
        """
        response = self.stories_response(username)
        if response.status_code != 200:
            if self.quiet is False:
                logger.info("\033[91m{} has no stories\033[0m".format(username))
            raise NoStoriesAvailable

        stories = response.json().get("story").get("snaps")

        if self.limit_story > -1:
            stories = stories[0 : self.limit_story]

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers)
        try:
            for media in stories:
                media_url = media["media"]["mediaUrl"]
                timestamp = int(media["captureTimeSecs"])
                date_str = strf_time(timestamp, "%Y-%m-%d")
                file_ext = self.media_type(media["media"]["type"])

                dir_name = os.path.join(self.directory_prefix, username, date_str)
                filename = strf_time(timestamp, "%Y-%m-%d_%H-%M-%S {} {}{}").format(
                    media.get("id"), username, file_ext
                )
                output = os.path.join(dir_name, filename)
                executor.submit(download_url, media_url, output)
        except KeyboardInterrupt:
            executor.shutdown(wait=False)

        logger.info("[+] {} has {} stories".format(username, len(stories)))
