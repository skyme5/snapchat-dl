"""The Main Snapchat Downloader Class."""
import concurrent.futures
import os
import re
from datetime import datetime

import requests
from colorama import Fore
from colorama import init
from tqdm import tqdm


class SnapchatDL:
    def __init__(self, directory_prefix=".", max_workers=2, limit_story=-1):
        init(autoreset=True)
        self.directory_prefix = directory_prefix
        self.max_workers = max_workers
        self.limit_story = limit_story
        self.endpoint = "https://storysharing.snapchat.com/v1/fetch/{}"
        "?request_origin=ORIGIN_WEB_PLAYER"
        self.reaponse_ok = requests.codes.get("ok")

    def get_stories(self, username):
        """Download user stories and check if `username`
           has stories available for download.

        Args:
            username (str): Snapchat username

        Returns:
            [dict]: {
                "stories_available": True,
                "data": data,
            }
        """
        api_url = self.endpoint.format(username)
        response = requests.get(api_url)

        if response.status_code != 200:
            return {"stories_available": False}
        data = response.json()

        return {"stories_available": True, "data": data}

    def valid_username(self, username):
        match = re.match(r"(?P<username>^[\w\.\_]+$)", username)
        if match is None:
            return False
        return match and match.groupdict()["username"] == username

    def media_type(self, media_type):
        """Return file extension for Media Type.

        Args:
            media_type (str): Snapchat Snap Media Type

        Returns:
            str: File Extension to use for `media_name`
        """
        if media_type == "IMAGE":
            return ".jpg"
        if media_type == "VIDEO":
            return ".mp4"
        if media_type == "VIDEO_NO_SOUND":
            return ".mp4"

    def strf_time(self, timestamp, format_str):
        return datetime.utcfromtimestamp(timestamp).strftime(format_str)

    def download_url(self, url: str, dest: str):
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest), exist_ok=True)

        if os.path.isfile(dest) and os.path.getsize(dest) == 0:
            os.remove(dest)

        with open(dest, "xb") as handle:
            response = requests.get(url, stream=True, timeout=10)
            if response.status_code != self.reaponse_ok:
                raise response.raise_for_status()

            if os.path.getsize(dest) == response.headers["Content-length"]:
                raise FileExistsError

            try:
                for data in response.iter_content(chunk_size=4194304):
                    handle.write(data)
                handle.close()
            except requests.exceptions.RequestException as e:
                print(Fore.RED + str(e))
                os.remove(dest)

    def download(self, username):
        """Download Snapchat Story for `username`.

        Args:
            username (str): Snapchat username

        Returns:
            [bool]: story downloader
        """
        if self.valid_username(username) is False:
            raise Exception("invalid username")

        response = self.get_stories(username)

        if response["stories_available"] is False:
            print("\033[91m[-] {} has no stories\033[0m".format(username))
            return False

        data = response["data"]
        stories = data.get("story").get("snaps")

        if self.limit_story > -1:
            stories = stories[0 : self.limit_story]
            limited_info = " of " + str(len(stories))
        else:
            limited_info = str()

        bar = tqdm(
            total=len(stories),
            desc=username,
            bar_format="{desc} |"
            + Fore.YELLOW
            + "{bar}"
            + Fore.RESET
            + "| {n_fmt}/{total_fmt}"
            + limited_info,
        )
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            for media in stories:
                media_url = media["media"]["mediaUrl"]
                timestamp = int(media["captureTimeSecs"])
                date_str = self.strf_time(timestamp, "%Y-%m-%d")
                file_ext = self.media_type(media["media"]["type"])

                dir_name = os.path.join(self.directory_prefix, username, date_str)
                filename = self.strf_time(
                    timestamp, "%Y-%m-%d_%H-%M-%S {} {}{}"
                ).format(media.get("id"), username, file_ext)
                output = os.path.join(dir_name, filename)

                def update_bar(fn):
                    bar.update()

                try:
                    future = executor.submit(self.download_url, media_url, output)
                    future.add_done_callback(update_bar)
                except FileExistsError:
                    pass

        return True
