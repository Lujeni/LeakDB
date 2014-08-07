LeakDB
======
.. image:: https://pypip.in/download/LeakDB/badge.png
    :target: https://pypi.python.org/pypi/LeakDB/
    :alt: Downloads

.. image:: https://pypip.in/version/LeakDB/badge.png
    :target: https://pypi.python.org/pypi/LeakDB/
    :alt: Latest Version

Why ?
-----
For the fun \o/

Overview
--------
LeakDB is a very simple and fast key value store for Python.

All data is stored in memory and the persistence is defined by the user.
A max queue size can be defined for a auto-flush.


Installation
------------
This code has been run on Python 2.7.
You should install ``gevent`` through your system packages management.

::

  $ pip install LeakDB #and enjoy



API
---
.. code:: python

    >>> from leakdb import PersistentQueueStorage
    >>> leak = PersistentQueueStorage(filename='/tmp/foobar.db')

    # set the value of a key
    >>> leak.set('bar', {'foo': 'bar'})
    >>> leak.set('foo', 2, key_prefix='bar_')

    # increment a key
    >>> leak.incr(key='bar_foo', delta=5)
     7

    >>> leak.incr(key='foobar', initial_value=1000)
     1000

    # looks up multiple keys
    >>> leak.get_multi(keys=['bar', 'foobar'])
     {u'foobar': 1000, u'bar': {u'foo': u'bar'}}

    # ensure changes are sent to disk
    >>> print leak
     /tmp/foobar.db 12288 bytes :: 3 items in queue :: 3 items in storage memory

    >>> leak.flush(force=True)
     /tmp/foobar.db 12338 bytes :: 0 items in queue :: 3 items in storage memory

    >>> leak.close()

STORAGE
-------

- **DefaultStorage** :: The default storage, all API operations are implemented ``set`` ``set_multi`` ``incr`` ``decr`` ``get_multi`` ``delete``
- **QueueStorage** :: Use the ``DefaultStorage`` with a queue. You can override the ``QueueStorage.worker_process`` method and make what you want when the ``flush`` method is called.

.. code:: python

    from leakdb import QueueStorage

    class MyQueueStorage(QueueStorage):

        def worker_process(self, item):
            """ Default action execute by each worker.
                Must return a True statement to remove the item,
                otherwise the worker put the item into the queue.
            """
            logger.info('process item :: {}'.format(item))
            return True

- **PersistentStorage** :: Use the ``DefaultStorage``, otherwise **each** operation is stored through the ``shelve`` module.
- **PersistentQueueStorage** :: Use the ``QueueStorage`` and the ``PersistentStorage``.

.. code:: python

    # see also the API part
    from leakdb import PersistentQueueStorage

    storage = PersistentQueueStorage(filename="/tmp/foobar.db",  maxsize=1, workers=1)
    # the queue is auto-flush, each operations check the queue size
    storage.set('foo', 1)

TODO
----

- finish the transport layer through zeroMQ
- cleanup the code
- improves the unittests
- write a CLI
- benchmark each storage
