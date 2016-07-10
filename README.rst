|Build Status| |Coverage Status| 

====
Pete
====


*He's just happy to be here*


Very much a work in progress. A task runner that will check on things,
and report things. Spiritually similar to
`IFTTT <https://ifttt.com/>`__.

Example
=======

::

    >>> from pete.runner import Runner
    >>> from pete.examples import StringBroadcaster, TimeChecker
    >>> 
    >>> runner = Runner(
    ...     tasks=[TimeChecker()],
    ...     broadcasters=[StringBroadcaster()],
    ...     timeout=10)
    >>> runner.main()
    It is now 00:00:56
    It is now 00:01:06
    ...

Plans
=====

-  Broadcasters

   -  Email
   -  Slack
   -  HTML
   -  RSS

-  Tasks

   -  MBTA delays
   -  Weather in the white mountains
   -  Why is the flag at half mast

.. |Build Status| image:: https://travis-ci.org/ColCarroll/pete.svg?branch=master
   :target: https://travis-ci.org/ColCarroll/pete
.. |Coverage Status| image:: https://coveralls.io/repos/github/ColCarroll/pete/badge.svg?branch=master 
   :target: https://coveralls.io/github/ColCarroll/pete?branch=master
