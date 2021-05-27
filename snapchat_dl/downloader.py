"""File Downlaoder for snapchat_dl."""
import os
import time

import requests
from loguru import logger


def download_url(url: str, dest: str, sleep_interval: int):
    """Download URL to destionation path.

    Args:
        url (str): url to download
        dest (str): absolute path to destination

    Raises:
        response.raise_for_status: if response is 4** or 50*
        FileExistsError: if file is already downloaded
    """
    if len(os.path.dirname(dest)) > 0:
        os.makedirs(os.path.dirname(dest), exist_ok=True)

    """Rate limiting."""
    time.sleep(sleep_interval)

    response = requests.get(url, stream=True, timeout=10)
    if response.status_code != requests.codes.get("ok"):
        raise response.raise_for_status()

    dest_ext = response.headers.get("content-type").split("/").pop()
    dest_file = dest + "." + dest_ext

    if os.path.isfile(dest_file) and os.path.getsize(dest_file) == response.headers.get(
        "content-length"
    ):
        raise FileExistsError

    if os.path.isfile(dest_file) and os.path.getsize(dest_file) == 0:
        os.remove(dest_file)
    try:
        with open(dest_file, "xb") as handle:
            try:
                for data in response.iter_content(chunk_size=4194304):
                    handle.write(data)
                handle.close()
            except requests.exceptions.RequestException as e:
                logger.error(e)
    except:
        FileExistsError
