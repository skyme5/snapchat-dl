"""The Main Snapchat Downloader Class."""

import concurrent.futures
import json
import os
import re

import requests
from loguru import logger

from snapchat_dl.downloader import download_url
from snapchat_dl.utils import APIResponseError
from snapchat_dl.utils import dump_response
from snapchat_dl.utils import MEDIA_TYPE
from snapchat_dl.utils import NoStoriesFound
from snapchat_dl.utils import strf_time
from snapchat_dl.utils import UserNotFoundError


class SnapchatDL:
    """Interact with Snapchat API to download story."""

    def __init__(
        self,
        directory_prefix=".",
        max_workers=2,
        limit_story=-1,
        sleep_interval=1,
        quiet=False,
        dump_json=False,
    ):
        self.directory_prefix = os.path.abspath(os.path.normpath(directory_prefix))
        self.max_workers = max_workers
        self.limit_story = limit_story
        self.sleep_interval = sleep_interval
        self.quiet = quiet
        self.dump_json = dump_json
        self.endpoint_web = "https://www.snapchat.com/add/{}/"
        self.regexp_web_json = (
            r'<script\s*id="__NEXT_DATA__"\s*type="application\/json">([^<]+)<\/script>'
        )
        self.reaponse_ok = requests.codes.get("ok")

    def _api_response(self, username):
        web_url = self.endpoint_web.format(username)
        return requests.get(
            web_url,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            },
        ).text

    def _web_fetch_story(self, username):
        """Download user stories from Web.

        Args:
            username (str): Snapchat `username`

        Raises:
            APIResponseError: API Error

        Returns:
            (dict, dict): user_info, stories
        """
        response = self._api_response(username)
        response_json_raw = re.findall(self.regexp_web_json, response)

        try:
            response_json = json.loads(response_json_raw[0])

            def util_web_user_info(content: dict):
                if "userProfile" in content["props"]["pageProps"]:
                    user_profile = content["props"]["pageProps"]["userProfile"]
                    field_id = user_profile["$case"]
                    return user_profile[field_id]
                else:
                    raise UserNotFoundError

            def util_web_story(content: dict):
                if "story" in content["props"]["pageProps"]:
                    return content["props"]["pageProps"]["story"]["snapList"]
                return list()

            def util_web_extract(content: dict):
                if "curatedHighlights" in content["props"]["pageProps"]:
                    return content["props"]["pageProps"]["curatedHighlights"]
                return list()

            user_info = util_web_user_info(response_json)
            stories = util_web_story(response_json)
            curatedHighlights = util_web_extract(response_json)
            spotHighlights = util_web_extract(response_json)
            return stories, user_info, curatedHighlights, spotHighlights
        except (IndexError, KeyError, ValueError):
            raise APIResponseError

    def download(self, username):
        """Download Snapchat Story for `username`.

        Args:
            username (str): Snapchat `username`

        Returns:
            [bool]: story downloader
        """
        stories, snap_user, *_ = self._web_fetch_story(username)

        if len(stories) == 0:
            if self.quiet is False:
                logger.info("\033[91m{}\033[0m has no stories".format(username))

            raise NoStoriesFound

        if self.limit_story > -1:
            stories = stories[0 : self.limit_story]

        logger.info("[+] {} has {} stories".format(username, len(stories)))

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers)
        try:
            for media in stories:
                snap_id = media["snapId"]["value"]
                media_url = media["snapUrls"]["mediaUrl"]
                media_type = media["snapMediaType"]
                timestamp = int(media["timestampInSec"]["value"])
                date_str = strf_time(timestamp, "%Y-%m-%d")

                dir_name = os.path.join(self.directory_prefix, username, date_str)

                filename = strf_time(timestamp, "%Y-%m-%d_%H-%M-%S {} {}.{}").format(
                    snap_id, username, MEDIA_TYPE[media_type]
                )

                if self.dump_json:
                    filename_json = os.path.join(dir_name, filename + ".json")
                    media_json = dict(media)
                    media_json["snapUser"] = snap_user
                    dump_response(media_json, filename_json)

                media_output = os.path.join(dir_name, filename)
                executor.submit(
                    download_url, media_url, media_output, self.sleep_interval
                )

        except KeyboardInterrupt:
            executor.shutdown(wait=False)

        logger.info("[✔] {} stories downloaded".format(username, len(stories)))
