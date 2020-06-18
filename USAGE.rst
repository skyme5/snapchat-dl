usage: snapchat-dl [-h] [-c] [-i BATCH_FILENAME] [-P DIRECTORY_PREFIX]
                   [-l NUM_STORY] [-j MAX_WORKERS] [-s] [-u] [-t INTERVAL]
                   [usernames [usernames ...]]

positional arguments:
  usernames             Atleast one or more usernames to download stories for.

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
