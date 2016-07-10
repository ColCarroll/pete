[![Build Status](https://travis-ci.org/ColCarroll/pete.svg?branch=master)](https://travis-ci.org/ColCarroll/pete)
[![Coverage Status](https://coveralls.io/repos/github/ColCarroll/pete/badge.svg?branch=master)](https://coveralls.io/github/ColCarroll/pete?branch=master)
Pete
====
*He's just happy to be here*
----------------------------

Very much a work in progress.  A task runner that will check on things, and
report things.  Spiritually similar to [IFTTT](https://ifttt.com/).

Example
-------
```
>>> from runner import Runner
>>> from broadcasters import StringBroadcaster
>>> from tasks import TimeChecker
>>> 
>>> runner = Runner(
...     tasks=[TimeChecker()],
...     broadcasters=[StringBroadcaster()],
...     timeout=10)
>>> runner.main()
It is now 00:00:56
It is now 00:01:06
...
```

Plans
-----

* Broadcasters
    * Email
    * Slack
    * HTML
    * RSS

* Tasks
    * MBTA delays
    * Weather in the white mountains
    * Why is the flag at half mast
