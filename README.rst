===================================
Snapchat Public Stories Downloader.
===================================


.. image:: https://img.shields.io/pypi/v/snapchat-dl.svg
        :target: https://pypi.python.org/pypi/snapchat-dl

.. image:: https://img.shields.io/travis/skyme5/snapchat-dl.svg?branch=master
        :target: https://travis-ci.com/skyme5/snapchat-dl
        :alt: Build Status

.. image:: https://codecov.io/gh/skyme5/snapchat-dl/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/skyme5/snapchat-dl
        :alt: Code Coverage

.. image:: https://readthedocs.org/projects/snapchat-dl/badge/?version=latest
        :target: https://snapchat-dl.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
        :target: https://opensource.org/licenses/MIT
        :alt: License: MIT

.. image:: http://hits.dwyl.com/skyme5/snapchat-dl.svg
        :target: http://hits.dwyl.com/skyme5/snapchat-dl
        :alt: HitCount


Usage
-----

..  code-block:: none

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


Features
--------

* Download public stories from Snapchat.
* Ability to scan clipboard for story urls.
* Documentation: https://snapchat-dl.readthedocs.io.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
