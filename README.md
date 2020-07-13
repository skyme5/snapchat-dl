<p>
  <div align="center">
  <h1>
    Snapchat Public Stories Downloader.<br /> <br />
    <a href="https://pypi.python.org/pypi/snapchat-dl">
      <img
        src="https://img.shields.io/pypi/v/snapchat-dl.svg"
        alt="Python Package"
      />
    </a>
    <a href="https://pypi.python.org/pypi/snapchat-dl">
      <img
        src="https://img.shields.io/github/workflow/status/skyme5/snapchat-dl/build"
        alt="CI"
      />
    </a>
    <a href="https://codecov.io/gh/skyme5/snapchat-dl">
      <img
        src="https://img.shields.io/codecov/c/github/skyme5/snapchat-dl"
        alt="Code Coverage"
      />
    </a>
    <a href="https://codecov.io/gh/skyme5/snapchat-dl">
      <img
        src="https://img.shields.io/pypi/pyversions/snapchat-dl"
        alt="Python Versions"
      />
    </a>
    <a href="https://github.com/psf/black">
      <img
        src="https://img.shields.io/badge/code%20style-black-000000.svg"
        alt="The Uncompromising Code Formatter"
      />
    </a>
    <a href="https://github.com/skyme5/snapchat-dl">
      <img
        src="https://img.shields.io/pypi/dm/snapchat-dl"
        alt="Monthly Downloads"
      />
    </a>
    <a href="https://opensource.org/licenses/MIT">
      <img
        src="https://img.shields.io/badge/License-MIT-blue.svg"
        alt="License: MIT"
      />
    </a>
  </h1>
  </div>
</p>


### Installation

Install using pip,

```bash
pip install snapchat-dl
```

Install from GitHub,

```bash
pip install git+git://github.com/skyme5/snapchat-dl
```

### Usage

```text

usage: snapchat-dl [-h] [-c] [-i BATCH_FILENAME] [-P DIRECTORY_PREFIX]
                   [-l NUM_STORY] [-j MAX_WORKERS] [-s] [-u] [-t INTERVAL]
                   [-q]
                   [username [username ...]]

positional arguments:
  username              Atleast one or more usernames to download stories for.

optional arguments:
  -h, --help            show this help message and exit
  -c, --scan-clipboard  Scan clipboard for story links with the format of
                        'https://story.snapchat.com/s/<username>'
  -i BATCH_FILENAME, --batch-file BATCH_FILENAME
                        Read usernames from file
  -P DIRECTORY_PREFIX, --directory-prefix DIRECTORY_PREFIX
                        Directory Prefix for downloading stories
  -l NUM_STORY, --limit-story-count NUM_STORY
                        Set maximum number of stories to download.
  -j MAX_WORKERS, --max-concurrent-downloads MAX_WORKERS
                        Set maximum number of parallel downloads.
  -s, --scan-from-prefix
                        Scan usernames (as directory name) from prefix
                        directory.
  -u, --check-for-update
                        Periodically check for new stories.
  -t INTERVAL, --update-interval INTERVAL
                        Set the update interval for new story in seconds.
                        (Default: 10m)
  -q, --quiet           Do not print anything to the console. (errors are
                        still logged)


```
